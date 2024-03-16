from os.path import isfile

from ros2cli.node.strategy import NodeStrategy
from ros2cli.verb import VerbExtension

from ros2autodoc.api import check_for_node


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
            "input-file",
            metavar="",
            nargs=1,
            help="absolute path of the README.md file to be updated.",
            required=True,
        )

    def main(self, *, args):
        """
        This should:
        1. Parse the current file and store it in a data structure
        2. Read the current node interface and store it in a similar data structure
        3. Compare and add/remove accordingly
        4. Write the output to the README file
        """
        if not isfile(args.input_file):
            return f"File: '{args.input_file}' could not be found."

        with NodeStrategy(args) as node:
            for node_name in args.nodes:
                if not check_for_node(node, f"/{node_name}"):
                    print(f"Node '{node_name}' is not running and will be ignored.")
                    continue
