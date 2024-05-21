from os.path import abspath, basename, curdir

from ros2cli.node.strategy import NodeStrategy
from ros2cli.verb import VerbExtension
from ros2pkg.api import get_executable_paths

from ros2autodoc.api import check_for_node, check_for_package, document_node
from ros2autodoc.api.node_runner import NodeRunner


class GenerateVerb(VerbExtension):
    """Automatically generate documentation for a ROS2 node."""

    def add_arguments(self, parser, cli_name):
        parser.add_argument(
            "package_name",
            metavar="package_name",
            help="name of the package containing the nodes to be documented.",
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
            "--launch-file",
            default=None,
            metavar="launch_file",
            help="name of the launch file to start the nodes.",
        )
        parser.add_argument(
            "--output-dir",
            default=abspath(curdir),
            metavar="",
            help="the directory where documentation should be written. If not"
            " specified, the file will be saved to the current directory.",
        )
        parser.add_argument(
            "--seperate-files",
            action="store_true",
            help="when this option is set, the node documentation will "
            "be written to separate files and no package documentation will "
            "be generated.",
        )

    def main(self, *, args):
        # Check if package is available
        if args.package_name and not check_for_package(args.package_name):
            return f"Package '{args.package_name}' could not be found."

        # Check if all inputs were provided
        if not args.nodes and (not args.executables or not args.launch_file):
            return "At least one node and one executable or launch file are required."

        if args.executables:
            # Check if the number of nodes matches the executables
            if len(args.nodes) != len(args.executables):
                return_str = (
                    f"Number of nodes ({len(args.nodes)}) "
                    + f"does not match the number of executables ({len(args.executables)})."
                )
                return return_str

            # Check if the package contains all the executables
            paths = get_executable_paths(package_name=args.package_name)
            executables = [basename(path) for path in paths]
            missing_executables = [
                exe for exe in args.executables if exe not in executables
            ]
            if missing_executables:
                return f"Missing executables: {', '.join(missing_executables)}"

        # Ensure no trailing slash
        args.output_dir = args.output_dir.rstrip("/")

        # Create runner to start the nodes
        runner = NodeRunner()

        with NodeStrategy(args) as node:
            if args.launch_file:
                runner.start(args.package_name, launch_file=args.launch_file)

                for node_name in args.nodes:

                    if not check_for_node(node, f"/{node_name}"):
                        print(f"Node '{node_name}' is not running and will be ignored.")
                        continue
                    if args.seperate_files:
                        document_node(
                            node, None, node_name, f"{args.output_dir}/{node_name}.md"
                        )
                    else:
                        document_node(
                            node,
                            args.package_name,
                            node_name,
                            f"{args.output_dir}/README.md",
                        )
                       
                runner.stop()
            
            elif args.executables:
                for node_name, executable_name in zip(args.nodes, args.executables):

                    runner.start(args.package_name, executable_name=executable_name)

                    if not check_for_node(node, f"/{node_name}"):
                        print(f"Node '{node_name}' is not running and will be ignored.")
                        continue
                    if args.seperate_files:
                        document_node(
                            node, None, node_name, f"{args.output_dir}/{node_name}.md"
                        )
                    else:
                        document_node(
                            node,
                            args.package_name,
                            node_name,
                            f"{args.output_dir}/README.md",
                        )
                    runner.stop()
