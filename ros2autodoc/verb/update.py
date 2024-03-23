from os.path import isfile

from ros2cli.node.strategy import NodeStrategy
from ros2cli.verb import VerbExtension

from ros2autodoc.api import check_for_node, update_documentation


class UpdateVerb(VerbExtension):
    """Update the documentation of a ROS2 node."""

    def add_arguments(self, parser, cli_name):
        parser.add_argument(
            "nodes",
            metavar="node",
            nargs="*",
            help="name of the nodes to be documented. If not specified, "
            "all running nodes from the package will be documented.",
        )
        parser.add_argument(
            "input_file",
            help="absolute path of the README.md file to be updated.",
        )

    def main(self, *, args):
        if not isfile(args.input_file):
            return f"File: '{args.input_file}' could not be found."

        with NodeStrategy(args) as node:
            for node_name in args.nodes:
                if not check_for_node(node, f"/{node_name}"):
                    print(f"Node '{node_name}' is not running and will be ignored.")
                    continue
                update_documentation(node, args.input_file)
