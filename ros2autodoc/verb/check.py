import sys
from os.path import basename, isfile

from ros2cli.node.strategy import NodeStrategy
from ros2cli.verb import VerbExtension
from ros2pkg.api import get_executable_paths

from ros2autodoc.api import check_for_node, check_for_package, check_node_documentation
from ros2autodoc.api.node_runner import NodeRunner


class CheckVerb(VerbExtension):
    """Check if a ROS2 node API is documented."""

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
            help="absolute path of the documentation of the nodes.",
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

        # Create runner to start the nodes
        runner = NodeRunner()

        with NodeStrategy(args) as node:
            if args.launch_file:
                runner.start(args.package_name, launch_file=args.launch_file)

                for node_name in args.nodes:
                    if not check_for_node(node, f"/{node_name}"):
                        print(f"Node '{node_name}' is not running and will be ignored.")
                        continue
                    if not check_node_documentation(node, node_name, args.input_file):
                        runner.stop()
                        sys.exit(1)
                    print(f"Node '{node_name}' interfaces are correctly listed.")
                runner.stop()

            elif args.executables:
                for node_name, executable_name in zip(args.nodes, args.executables):
                    runner.start(args.package_name, executable_name)
                    if not check_for_node(node, f"/{node_name}"):
                        print(f"Node '{node_name}' is not running and will be ignored.")
                        runner.stop()
                        continue
                    if not check_node_documentation(node, node_name, args.input_file):
                        runner.stop()
                        sys.exit(1)
                    print(f"Node '{node_name}' interfaces are correctly listed.")
                    runner.stop()
