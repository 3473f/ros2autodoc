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
    for node_param in node_interface["parameters"]:
        if node_param in doc_interface["parameters"]:
            # Update type if different
            if node_interface["parameters"][node_param]["type"] != doc_interface["parameters"][node_param]["type"]:
                print(f"Updating parameter type for {node_param}")
                doc_interface["parameters"][node_param]["type"] = node_interface["parameters"][node_param]["type"]
            # Update description if different and not TODO
            if node_interface["parameters"][node_param]["description"] != doc_interface["parameters"][node_param]["description"] and node_interface["parameters"][node_param]["description"] != TODO:
                print(f"Updating parameter description for {node_param}")
                doc_interface["parameters"][node_param]["description"] = node_interface["parameters"][node_param]["description"]
        else:
            print(f"Adding missing parameter: {node_param}")
            doc_interface["parameters"][node_param] = node_interface["parameters"][node_param]

    # Check if subscriber names are the same
    for node_sub in node_interface["subscribers"]:
        if node_sub in doc_interface["subscribers"]:
            # Update type if different
            if node_interface["subscribers"][node_sub]["type"] != doc_interface["subscribers"][node_sub]["type"]:
                print(f"Updating subscriber type for {node_sub}")
                doc_interface["subscribers"][node_sub]["type"] = node_interface["subscribers"][node_sub]["type"]
            # Update description if different and not TODO
            if node_interface["subscribers"][node_sub]["description"] != doc_interface["subscribers"][node_sub]["description"] and node_interface["subscribers"][node_sub]["description"] != TODO:
                print(f"Updating subscriber description for {node_sub}")
                doc_interface["subscribers"][node_sub]["description"] = node_interface["subscribers"][node_sub]["description"]
        else:
            print(f"Adding missing subscriber: {node_sub}")
            doc_interface["subscribers"][node_sub] = node_interface["subscribers"][node_sub]

    # Check if publisher names are the same
    for node_pub in node_interface["publishers"]:
        if node_pub in doc_interface["publishers"]:
            # Update type if different
            if node_interface["publishers"][node_pub]["type"] != doc_interface["publishers"][node_pub]["type"]:
                print(f"Updating publisher type for {node_pub}")
                doc_interface["publishers"][node_pub]["type"] = node_interface["publishers"][node_pub]["type"]
            # Update description if different and not TODO
            if node_interface["publishers"][node_pub]["description"] != doc_interface["publishers"][node_pub]["description"] and node_interface["publishers"][node_pub]["description"] != TODO:
                print(f"Updating publisher description for {node_pub}")
                doc_interface["publishers"][node_pub]["description"] = node_interface["publishers"][node_pub]["description"]
        else:
            print(f"Adding missing publisher: {node_pub}")
            doc_interface["publishers"][node_pub] = node_interface["publishers"][node_pub]

    # Check if service names are the same
    for node_srv in node_interface["services"]:
        if node_srv in doc_interface["services"]:
            # Update type if different
            if node_interface["services"][node_srv]["type"] != doc_interface["services"][node_srv]["type"]:
                print(f"Updating service type for {node_srv}")
                doc_interface["services"][node_srv]["type"] = node_interface["services"][node_srv]["type"]
            # Update description if different and not TODO
            if node_interface["services"][node_srv]["description"] != doc_interface["services"][node_srv]["description"] and node_interface["services"][node_srv]["description"] != TODO:
                print(f"Updating service description for {node_srv}")
                doc_interface["services"][node_srv]["description"] = node_interface["services"][node_srv]["description"]
        else:
            print(f"Adding missing service: {node_srv}")
            doc_interface["services"][node_srv] = node_interface["services"][node_srv]

    # Check if action names are the same
    for node_action in node_interface["actions"]:
        if node_action in doc_interface["actions"]:
            # Update type if different
            if node_interface["actions"][node_action]["type"] != doc_interface["actions"][node_action]["type"]:
                print(f"Updating action type for {node_action}")
                doc_interface["actions"][node_action]["type"] = node_interface["actions"][node_action]["type"]
            # Update description if different and not TODO
            if node_interface["actions"][node_action]["description"] != doc_interface["actions"][node_action]["description"] and node_interface["actions"][node_action]["description"] != TODO:
                print(f"Updating action description for {node_action}")
                doc_interface["actions"][node_action]["description"] = node_interface["actions"][node_action]["description"]
        else:
            print(f"Adding missing action: {node_action}")
            doc_interface["actions"][node_action] = node_interface["actions"][node_action]
    
    # Update the document
    writer = DocWriter(None, node_name, doc_interface)
    writer.write(file_path)


