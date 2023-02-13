import os
import sys

from ros2autodoc.api.doc_writer import DocWriter

# ROS2 node API
from ros2node.api import get_action_server_info
from ros2node.api import get_node_names
from ros2node.api import get_publisher_info
from ros2node.api import get_service_server_info
from ros2node.api import get_subscriber_info
from ros2node.api import INFO_NONUNIQUE_WARNING_TEMPLATE

# ROS2 param API
from ros2param.api import call_describe_parameters
from ros2param.api import call_list_parameters
from ros2param.api import get_parameter_type_string

# ROS2 pkg API
from ros2pkg.api import get_executable_paths
from ros2pkg.api import get_package_names

def check_for_package(package_name):
    """
    Check if the given package is available.
    """
    if package_name not in get_package_names():
        return False
    return True

def check_for_node(node, node_name):
    """
    check if the given node is available and running.
    """
    running_nodes = get_node_names(node=node, include_hidden_nodes=True)
    count = [n.full_name for n in running_nodes].count(node_name)
    if count > 1:
        print(
            INFO_NONUNIQUE_WARNING_TEMPLATE.format(
                num_nodes=count, node_name=node_name),
                file=sys.stderr)
        return False
    if count > 0:
        return True
    else:
        print("Unable to find node '{}'.".format(node_name))
        return False

def get_nodes(package_name):
    """
    Get all the nodes in a given package.
    """
    paths = get_executable_paths(package_name=package_name)
    nodes = []
    for path in sorted(paths):
        nodes.append(os.path.basename(path))
    return nodes

def document_node(node, package_name, node_name, path):
    """
    Document the given node.
    """
    writer = DocWriter(package_name, node_name, path)
    param_names, params = _get_parameters(node, node_name)
    if len(params) > 0:
        writer.write_parameters(param_names, params)
    subscribers = get_subscriber_info(
        node=node, remote_node_name=node_name, include_hidden=False)
    if len(subscribers) > 0:
        writer.write_subscribers(subscribers)
    publishers = get_publisher_info(
        node=node, remote_node_name=node_name, include_hidden=False)
    if len(publishers) > 0:
        writer.write_publishers(publishers)
    service_servers = get_service_server_info(
        node=node, remote_node_name=node_name, include_hidden=True)
    if len(service_servers) > 0:
        writer.write_service_servers(service_servers)
    actions_servers = get_action_server_info(
        node=node, remote_node_name=node_name, include_hidden=True)
    if len(actions_servers) > 0:
        writer.write_action_servers(actions_servers)


def _get_parameters(node, node_name):
    name_to_type_map = {}
    parameter_names = call_list_parameters(node=node, node_name=node_name)
    sorted_names = sorted(parameter_names)
    resp = call_describe_parameters(
                    node=node, node_name=node_name,
                    parameter_names=sorted_names)
    for descriptor in resp.descriptors:
        name_to_type_map[descriptor.name] = get_parameter_type_string(
                                                            descriptor.type)
    return sorted_names, name_to_type_map