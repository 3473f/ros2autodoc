from multiprocessing import Process
from os.path import abspath, curdir

from ros2cli.node.strategy import NodeStrategy
from ros2cli.verb import VerbExtension

from ros2autodoc.api import check_for_node, check_for_package, document_node
from ros2autodoc.api.node_runner import NodeRunner


class GenerateVerb(VerbExtension):
    """Automatically generate documentation for a ROS2 node."""

    def add_arguments(self, parser, cli_name):
        parser.add_argument(
            "package_name",
            metavar="package_name",
            help="name of the package to be documented. If not specified, "
            "the package documentation will be left out.",
        )
        parser.add_argument(
            "--nodes",
            metavar="node",
            nargs="*",
            help="name of the nodes to be documented. If not specified, "
            "all running nodes from the package will be documented.",
        )
        parser.add_argument(
            "--executables",
            metavar="executables",
            nargs="*",
            help="name of the executables to be documented. If not specified, "
            "all executables from the package will be documented.",
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

    def run_executable(self, runner, package_name, executable_name):
        runner.run(package_name, executable_name)

    def main(self, *, args):
        if args.package_name and not check_for_package(args.package_name):
            return f"Package '{args.package_name}' could not be found."

        if len(args.nodes) != len(args.executables):
            return_str = (
                f"Number of nodes ({len(args.nodes)})"
                + f"does not match the number of executables ({len(args.executables)})."
            )
            return return_str

        # Ensure no trailing slash
        args.output_dir = args.output_dir.rstrip("/")

        runner = NodeRunner()

        with NodeStrategy(args) as node:
            for node_name, executable_name in zip(args.nodes, args.executables):
                run_process = Process(
                    target=self.run_executable,
                    args=(runner, args.package_name, executable_name),
                )
                run_process.start()

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
                run_process.kill()  # this is not enough
