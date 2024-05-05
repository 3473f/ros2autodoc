import os
import sys

# ROS2 node API
from ros2node.api import INFO_NONUNIQUE_WARNING_TEMPLATE, get_node_names

# ROS2 pkg API
from ros2pkg.api import get_executable_paths, get_package_names

from ros2autodoc.api.doc_parser import DocParser
from ros2autodoc.api.doc_writer import DocWriter
from ros2autodoc.api.node_interface_collector import NodeInterfaceCollector

TODO = "TODO: description"


def check_for_package(package_name):
    """Check if the given package is available."""
    if package_name not in get_package_names():
        return False
    return True


def check_for_node(node, node_name):
    """Check if the given node is available and running."""
    running_nodes = get_node_names(node=node, include_hidden_nodes=True)
    count = [n.full_name for n in running_nodes].count(node_name)
    if count > 1:
        print(
            INFO_NONUNIQUE_WARNING_TEMPLATE.format(
                num_nodes=count, node_name=node_name
            ),
            file=sys.stderr,
        )
        return False
    if count > 0:
        return True

    print(f"Unable to find node '{node_name}'.")
    return False


def get_nodes(package_name):
    """Get all the nodes in a given package."""
    paths = get_executable_paths(package_name=package_name)
    nodes = []
    for path in sorted(paths):
        nodes.append(os.path.basename(path))
    return nodes


def document_node(node, package_name, node_name, path, file_name="/README.md"):
    """Document the given node."""
    interface_collector = NodeInterfaceCollector(node, node_name)
    node_interface = interface_collector.get_interfaces()
    writer = DocWriter(package_name, node_name, node_interface)
    writer.write(path + file_name)


def update_documentation(node, node_name, file_path):
    """Update the documentation for the given node."""
    # Parse the document
    parser = DocParser(file_path)
    parser.parse()
    doc_interface = parser.get_node_interface(node_name)
    if not doc_interface:
        print(f"Node '{node_name}' was not found in the documentation.")
        return

    # Get the current node interface
    interface_collector = NodeInterfaceCollector(node, node_name)
    node_interface = interface_collector.get_interfaces()

    # Check if parameter names are the same
    if sorted(doc_interface["parameters"].keys()) == sorted(
        node_interface["parameters"].keys()
    ):
        for doc_param, node_param in zip(
            sorted(doc_interface["parameters"].keys()),
            sorted(node_interface["parameters"].keys()),
        ):
            # Check if the types are different
            if (
                doc_interface["parameters"][doc_param]["type"]
                != node_interface["parameters"][node_param]["type"]
            ):
                node_interface["parameters"][node_param]["type"] = doc_interface[
                    "parameters"
                ][doc_param]["type"]
            if (
                doc_interface["parameters"][doc_param]["description"]
                != node_interface["parameters"][node_param]["description"]
                and doc_interface["parameters"][doc_param]["description"] != TODO
            ):
                node_interface["parameters"][node_param]["description"] = doc_interface[
                    "parameters"
                ][doc_param]["description"]
    # If parameters are not the same
    else:
        pass