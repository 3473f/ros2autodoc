from ros2cli.node.strategy import NodeStrategy
from ros2cli.verb import VerbExtension

from ros2autodoc.api import check_for_node
from ros2autodoc.api import check_for_package
from ros2autodoc.api import document_node
from ros2autodoc.api import get_nodes

from os.path import exists, abspath, curdir

class GenerateVerb(VerbExtension):
    """
    Automatically generate documentation for a ROS2 node. 
    """

    def add_arguments(self, parser, cli_name):
        parser.add_argument(
            'package_name',
            help='Name of the package.')
        parser.add_argument(
            'nodes',
            metavar='node',
            nargs='*',
            help='Name of the nodes to be documented. If not specified, '
                 'all running nodes from the package will be documented')
        parser.add_argument(
            '--output-dir',
            default=abspath(curdir),
            help='The directory where documentation should be written.'
        )

    def main(self, *, args):
        if not check_for_package(args.package_name):
            return "Package '{}' could not be found.".format(args.package_name)

        if args.nodes:
            if not set(args.nodes).issubset(get_nodes(args.package_name)):
                return "Make sure that all nodes exist in the package."
            nodes = args.nodes
        else:
            nodes = get_nodes(args.package_name)
        
        with NodeStrategy(args) as node:
            for node_name in nodes:
                if not check_for_node(node, "/{}".format(node_name)):
                    print("Node '{}' is not running"
                            " and will be ignored.".format(node_name))
                    continue
                # Document the node
                print(node_name)
                document_node(node, args.package_name, node_name, args.output_dir)