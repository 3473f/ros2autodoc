import os
import sys

# ROS2 node API
from ros2node.api import get_action_server_info
from ros2node.api import get_node_names
from ros2node.api import get_publisher_info
from ros2node.api import get_service_server_info
from ros2node.api import INFO_NONUNIQUE_WARNING_TEMPLATE

# ROS2 pkg API
from ros2pkg.api import get_executable_paths
from ros2pkg.api import get_package_names

PUBLISHERS_TO_IGNORE = ["/parameter_events", "/rosout"]
SERVICES_TO_IGNORE = ["/describe_parameters",
                      "/get_parameter_types",
                      "/get_parameters",
                      "/list_parameters",
                      "/set_parameters",
                      "/set_parameters_atomically"]

def print_names_and_types(names_and_types):
    print(*[2 * '  ' + s.name + ': ' + ', '.join(
            s.types) for s in names_and_types], sep='\n')

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

# def _get_parameters():
#     pass

# def _get_publishers():
#     pass

# def _get_service_servers(node, node_name):
#      """
#      Get service servers provided by the node and their types. 
#      """
#      service_servers = get_service_server_info(
#          node=node, remote_node_name=node_name, include_hidden=True)
#      return service_servers

# def _get_action_servers(node, node_name):
#     """
#     Get action servers provided by the node and their types.
#     """
#     actions_servers = get_action_server_info(
#         node=node, remote_node_name=node_name, include_hidden=True)
#     return actions_servers