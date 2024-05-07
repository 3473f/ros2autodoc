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


def check_node_documentation(node, node_name, file_path):
    """Check if a node is properly documented."""
    interface_collector = NodeInterfaceCollector(node, node_name)
    node_interface = interface_collector.get_interfaces()

    parser = DocParser(file_path)
    parser.parse()
    doc_interface = parser.get_node_interface(node_name)

    if doc_interface is None:
        print("Node documentation not found.")
        return False

    # Check parameters
    if not check_interface("parameters", doc_interface, node_interface):
        return False
    # Check subscribers
    if not check_interface("subscribers", doc_interface, node_interface):
        return False
    # Check publishers
    if not check_interface("publishers", doc_interface, node_interface):
        return False
    # Check services
    if not check_interface("services", doc_interface, node_interface):
        return False
    # Check actions
    if not check_interface("actions", doc_interface, node_interface):
        return False

    return True


def check_interface(interface_type, doc_interface, node_interface):
    """Check if an interface type is properly documented."""
    if not doc_interface[interface_type] and node_interface[interface_type]:
        return True

    if sorted(doc_interface[interface_type].keys()) != sorted(
        node_interface[interface_type].keys()
    ):
        print(f"{interface_type.capitalize()} do not match.")
        return False
    else:
        for doc_item, node_item in zip(
            sorted(doc_interface[interface_type].keys()),
            sorted(node_interface[interface_type].keys()),
        ):
            # Check if item types are the same
            if (
                doc_interface[interface_type][doc_item]["type"]
                != node_interface[interface_type][node_item]["type"]
            ):
                print(f"Type of '{doc_item}' {interface_type} doesn't match.")
                return False
    return True
