import os
import sys
import time

# ROS2 node API
from ros2node.api import INFO_NONUNIQUE_WARNING_TEMPLATE, get_node_names

# ROS2 pkg API
from ros2pkg.api import get_executable_paths, get_package_names

from ros2autodoc.api.doc_parser import DocParser
from ros2autodoc.api.doc_writer import DocWriter
from ros2autodoc.api.node_interface_collector import NodeInterfaceCollector

TODO = "TODO: description"

INTERFACE_TYPES = ["parameters", "subscribers", "publishers", "services", "actions"]


def check_for_package(package_name):
    """Check if the given package is available."""
    if package_name not in get_package_names():
        return False
    return True


def check_for_node(node, node_name, timeout=10.0):
    """Check if the given node is available and running."""
    start_time = time.time()
    end_time = start_time + timeout

    while time.time() < end_time:
        running_nodes = get_node_names(node=node, include_hidden_nodes=True)
        count = [n.full_name for n in running_nodes].count(node_name)

        if count > 1:
            print(
                INFO_NONUNIQUE_WARNING_TEMPLATE.format(
                    num_nodes=count, node_name=node_name
                ),
                file=sys.stderr,
            )
            return True
        elif count > 0:
            return True

        time.sleep(0.1)

    print(f"Unable to find node '{node_name}'.")
    return False


def get_nodes(package_name):
    """Get all the nodes in a given package."""
    paths = get_executable_paths(package_name=package_name)
    nodes = []
    for path in sorted(paths):
        nodes.append(os.path.basename(path))
    return nodes


def document_node(node, package_name, node_name, file_path):
    """Document the given node."""
    interface_collector = NodeInterfaceCollector(node, node_name)
    node_interface = interface_collector.get_interfaces()
    writer = DocWriter(package_name, node_name, node_interface)
    writer.write(file_path)


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

    for interface_type in INTERFACE_TYPES:
        if not check_interface(interface_type, doc_interface, node_interface):
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


def update_node_interface(node, node_name, doc_interface):
    """Diff a node's live interface against its parsed doc interface.

    Mutates `doc_interface` in place (add/update entries from the live node,
    remove entries the node no longer has). Does not touch the filesystem.
    """
    interface_collector = NodeInterfaceCollector(node, node_name)
    node_interface = interface_collector.get_interfaces()

    for interface_type in INTERFACE_TYPES:
        doc_entries = doc_interface[interface_type]
        node_entries = node_interface[interface_type]

        for name, node_entry in node_entries.items():
            doc_entry = doc_entries.get(name)
            if doc_entry is None:
                print(f"Adding missing {interface_type[:-1]}: {name}")
                doc_entries[name] = node_entry
                continue

            if node_entry["type"] != doc_entry["type"]:
                print(f"Updating {interface_type[:-1]} type for {name}")
                doc_entry["type"] = node_entry["type"]

            if (
                node_entry["description"] != doc_entry["description"]
                and node_entry["description"] != TODO
            ):
                print(f"Updating {interface_type[:-1]} description for {name}")
                doc_entry["description"] = node_entry["description"]

        # Now that we added all missing elements,
        # check if there are any elements in the doc that are not in the node
        for name in list(doc_entries):
            if name not in node_entries:
                print(f"Removing {interface_type[:-1]}: {name}")
                del doc_entries[name]

    return doc_interface
