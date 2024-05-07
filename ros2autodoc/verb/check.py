import sys
from os.path import isfile

from ros2cli.node.strategy import NodeStrategy
from ros2cli.verb import VerbExtension

from ros2autodoc.api import check_for_node, check_node_documentation


class CheckVerb(VerbExtension):
    """Check if a ROS2 node API is documented."""

    def add_arguments(self, parser, cli_name):
        parser.add_argument(
            "nodes",
            metavar="node",
            nargs="*",
            help="name of the nodes to be checked.",
        )

        parser.add_argument(
            "input_file",
            help="absolute path of the documentation of the nodes.",
        )

    def main(self, *, args):
        if not isfile(args.input_file):
            return f"File: '{args.input_file}' could not be found."

        with NodeStrategy(args) as node:
            for node_name in args.nodes:
                if not check_for_node(node, f"/{node_name}"):
                    print(f"Node '{node_name}' is not running and will be ignored.")
                    continue
                if not check_node_documentation(node, node_name, args.input_file):
                    sys.exit(1)
                print(f"Node '{node_name}' interfaces are correctly listed.")
