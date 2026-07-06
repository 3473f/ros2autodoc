from os.path import basename, isfile

from ros2cli.node.strategy import NodeStrategy
from ros2cli.verb import VerbExtension
from ros2pkg.api import get_executable_paths

from ros2autodoc.api import check_for_node, check_for_package, update_node_interface
from ros2autodoc.api.doc_parser import DocParser
from ros2autodoc.api.doc_writer import write_documentation_file
from ros2autodoc.api.node_runner import NodeRunner


class UpdateVerb(VerbExtension):
    """Update the documentation of a ROS2 node."""

    def add_arguments(self, parser, cli_name):
        parser.add_argument(
            "package_name",
            metavar="package_name",
            help="name of the package containing the nodes to be documented.",
        )
        parser.add_argument(
            "--launch-file",
            default=None,
            metavar="launch_file",
            help="name of the launch file to start the nodes.",
        )
        parser.add_argument(
            "--nodes",
            metavar="node",
            nargs="*",
            help="name of the nodes to be documented.",
        )
        parser.add_argument(
            "--executables",
            metavar="executables",
            nargs="*",
            help="name of the executables for the nodes to be documented.",
        )
        parser.add_argument(
            "input_file",
            help="absolute path of the README.md file to be updated.",
        )

    def main(self, *, args):
        # Check if the file is available
        if not isfile(args.input_file):
            return f"File: '{args.input_file}' could not be found."

        # Check if package is available
        if args.package_name and not check_for_package(args.package_name):
            return f"Package '{args.package_name}' could not be found."

        # Check if all inputs were provided
        if not args.nodes and (not args.executables or not args.launch_file):
            return "At least one node and one executable or launch file are required."

        if args.executables:
            # Check if the number of nodes matches the executables
            if len(args.nodes) != len(args.executables):
                return "Number of nodes doesn't match the number of executables."

            # Check if the package contains all the executables
            paths = get_executable_paths(package_name=args.package_name)
            executables = [basename(path) for path in paths]
            missing_executables = [
                exe for exe in args.executables if exe not in executables
            ]
            if missing_executables:
                return f"Missing executables: {', '.join(missing_executables)}"

        # Parse the documentation once for the whole run
        parser = DocParser(args.input_file)
        parser.parse()

        with NodeStrategy(args) as node:
            if args.launch_file:
                with NodeRunner() as runner:
                    runner.start(args.package_name, launch_file=args.launch_file)

                    for node_name in args.nodes:
                        if not check_for_node(node, f"/{node_name}"):
                            print(f"Node '{node_name}' is not running and will be ignored.")
                            continue
                        self._update_node(parser, node, node_name)

            elif args.executables:
                for node_name, executable_name in zip(args.nodes, args.executables):
                    with NodeRunner() as runner:
                        runner.start(args.package_name, executable_name=executable_name)

                        if not check_for_node(node, f"/{node_name}"):
                            print(f"Node '{node_name}' is not running and will be ignored.")
                            continue
                        self._update_node(parser, node, node_name)

        write_documentation_file(
            args.input_file, args.package_name, parser.text_to_keep, parser.nodes
        )

    def _update_node(self, parser, node, node_name):
        doc_interface = parser.get_node_interface(node_name)
        if doc_interface is None:
            print(f"Node '{node_name}' was not found in the documentation.")
            return
        update_node_interface(node, node_name, doc_interface)
