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


def update_documentation(node, node_name, file_path):
    """Update the documentation for the given node."""
    parser = DocParser(file_path)
    writer = DocWriter(None, node_name)
    if node_name not in parser.get_node_names():
        print(f"Node {node_name} not found in document {file_path}")
        return

    param_names, params, description = _get_parameters(node, node_name)
    if len(params) > 0:
        writer.get_parameters(param_names, params, description)
    subscribers = get_subscriber_info(
        node=node, remote_node_name=node_name, include_hidden=False
    )
    if len(subscribers) > 0:
        writer.get_subscribers(subscribers)
    publishers = get_publisher_info(
        node=node, remote_node_name=node_name, include_hidden=False
    )
    if len(publishers) > 0:
        writer.get_publishers(publishers)
    service_servers = get_service_server_info(
        node=node, remote_node_name=node_name, include_hidden=False
    )
    if len(service_servers) > 0:
        writer.get_service_servers(service_servers)
    actions_servers = get_action_server_info(
        node=node, remote_node_name=node_name, include_hidden=False
    )
    if len(actions_servers) > 0:
        writer.get_action_servers(actions_servers)

    curr_node = writer.get_node()
    for i, parsed_node in enumerate(parser.get_nodes()):
        if parsed_node.name == curr_node.name:
            # compare both of their content
            continue


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
