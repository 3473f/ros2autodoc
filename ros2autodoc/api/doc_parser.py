import os
import re

_TYPE_RE = re.compile(r"\((.*?)\)")

_SECTION_HEADERS = {
    "### Parameters": "parameters",
    "### Subscribers": "subscribers",
    "### Publishers": "publishers",
    "### Services": "services",
    "### Actions": "actions",
}


class DocParser:
    def __init__(self, path):
        self.path = path
        self.text_to_keep = []
        self.nodes = {}

    def parse(self):
        """Parse the documentation."""
        if not os.path.exists(self.path):
            print("File not found.")
            return

        with open(self.path) as file:
            start_parsing = False
            current_section = None
            curr_node_name = None
            curr_item_name = None

            for line in file:
                stripped = line.strip()

                if stripped.startswith("## Nodes"):
                    self.text_to_keep.append(line)
                    start_parsing = True
                    continue

                if not start_parsing:
                    self.text_to_keep.append(line)
                    continue

                if stripped in _SECTION_HEADERS:
                    current_section = _SECTION_HEADERS[stripped]
                    curr_item_name = None
                    continue

                if stripped.startswith("### "):
                    current_section = None
                    curr_item_name = None
                    curr_node_name = stripped[4:]
                    self.nodes[curr_node_name] = {
                        "parameters": {},
                        "subscribers": {},
                        "publishers": {},
                        "services": {},
                        "actions": {},
                    }
                    continue

                if current_section is None:
                    continue

                if line.startswith("- **"):
                    item_name = line.split("**`")[1].split("`**")[0]
                    if item_name:
                        curr_item_name = item_name
                        match = _TYPE_RE.search(line)
                        data_type = match.group(1) if match else ""
                        self.nodes[curr_node_name][current_section][item_name] = {
                            "type": data_type,
                            "description": "",
                        }
                elif line.startswith("    ") and stripped and curr_item_name:
                    self.nodes[curr_node_name][current_section][curr_item_name][
                        "description"
                    ] = stripped

    def get_nodes(self):
        return self.nodes

    def get_node_interface(self, node_name):
        if node_name in self.nodes:
            return self.nodes[node_name]
        return None
