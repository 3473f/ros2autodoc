# BSD 3-Clause License
#
# Copyright (c) 2023, Mohamed Abdelaziz
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#
#    * Neither the name of the the copyright holder nor the names of its
#      contributors may be used to endorse or promote products derived from
#      this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from os.path import abspath, curdir

from ros2cli.node.strategy import NodeStrategy
from ros2cli.verb import VerbExtension

from ros2autodoc.api import check_for_node, check_for_package, document_node, get_nodes


class GenerateVerb(VerbExtension):
    """Automatically generate documentation for a ROS2 node."""

    def add_arguments(self, parser, cli_name):
        parser.add_argument(
            "--package-name",
            help="name of the package to be documented. If not specified, "
            "the package documentation will be left out.",
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
        if args.package_name:
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
        else:
            if args.nodes:
                nodes = args.nodes

        with NodeStrategy(args) as node:
            for node_name in nodes:
                if not check_for_node(node, f"/{node_name}"):
                    print(f"Node '{node_name}' is not running and will be ignored.")
                    continue
                # document the node
                document_node(node, args.package_name, node_name, args.output_dir)
