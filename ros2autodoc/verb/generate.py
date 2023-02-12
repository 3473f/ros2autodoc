from ros2cli.node.strategy import NodeStrategy
from ros2cli.verb import VerbExtension

class GenerateVerb(VerbExtension):
    """
    Automatically generate documentation for a ROS2 node. 
    """

    def add_arguments(self, parser, cli_name):
        parser.add_argument(
            'node',
            help="Name of the node to be documented."
        )

    def main(self, *, args):
        print('TODO')