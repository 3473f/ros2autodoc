import os
import sys

# ROS2 node API
from ros2node.api import INFO_NONUNIQUE_WARNING_TEMPLATE, get_node_names

# ROS2 pkg API
from ros2pkg.api import get_executable_paths, get_package_names

from ros2autodoc.api.doc_parser import DocParser
from ros2autodoc.api.doc_writer import DocWriter
from ros2autodoc.api.node_interface_collector import NodeInterfaceCollector


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


def update_documentation(node, file_path):
    """Update the documentation for the given node."""
    parser = DocParser(file_path)
    if node not in parser.get_node_names():
        print(f"Node {node} not found in document {file_path}")
        return


def _get_parameters(node, node_name):
    name_to_type_map = {}
    name_to_description_map = {}
    parameter_names = call_list_parameters(node=node, node_name=node_name)
    sorted_names = sorted(parameter_names)
    resp = call_describe_parameters(
        node=node, node_name=node_name, parameter_names=sorted_names
    )
    for descriptor in resp.descriptors:
        name_to_type_map[descriptor.name] = get_parameter_type_string(descriptor.type)
        name_to_description_map[descriptor.name] = descriptor.description
    return sorted_names, name_to_type_map, name_to_description_map
