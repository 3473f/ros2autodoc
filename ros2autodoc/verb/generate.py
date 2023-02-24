from os.path import abspath, curdir

from ros2cli.node.strategy import NodeStrategy
from ros2cli.verb import VerbExtension

from ros2autodoc.api import check_for_node, check_for_package, document_node, get_nodes


class GenerateVerb(VerbExtension):
    """Automatically generate documentation for a ROS2 node."""

    def add_arguments(self, parser, cli_name):
        parser.add_argument(
            "package_name", help="name of the package to be documented."
        )
        parser.add_argument(
            "nodes",
            metavar="node",
            nargs="*",
            help="name of the nodes to be documented. If not specified, "
            "all running nodes from the package will be documented.",
        )
        parser.add_argument(
            "--output-dir",
            default=abspath(curdir),
            help="the directory where documentation should be written.",
        )

    def main(self, *, args):
        if not check_for_package(args.package_name):
            return f"Package '{args.package_name}' could not be found."

        if args.nodes:
            # if not set(args.nodes).issubset(get_nodes(args.package_name)):
            #    return "Make sure that all nodes exist in the package."
            nodes = args.nodes
        else:
            nodes = get_nodes(
                args.package_name
            )  # executable name has to match node name

        with NodeStrategy(args) as node:
            for node_name in nodes:
                if not check_for_node(node, f"/{node_name}"):
                    print(f"Node '{node_name}' is not running and will be ignored.")
                    continue
                # document the node
                document_node(node, args.package_name, node_name, args.output_dir)
