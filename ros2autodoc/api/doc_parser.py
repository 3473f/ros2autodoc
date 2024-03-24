import os
import re

from node import Node


class DocParser:
    def __init__(self, path):
        self.path = path
        self.text_to_keep = []
        self.nodes = []

    def parse(self):
        """Parse the documentation."""
        if not os.path.exists(self.path):
            print("File not found.")
            return

        params = {}
        pubs = {}
        subs = {}
        srvs = {}
        actions = {}
        name = None
        with open(self.path) as file:
            start_parsing = False
            parse_params = False
            parse_subs = False
            parse_pubs = False
            parse_srvs = False
            parse_actions = False

            curr_node = None
            node_ctr = 0

            for line in file:
                if line.strip().startswith("## Nodes"):
                    self.text_to_keep.append(line)
                    start_parsing = True
                    continue

                if not start_parsing:
                    self.text_to_keep.append(line)
                    continue

                if line.strip().startswith("### Parameters"):
                    parse_params = True
                    parse_subs = False
                    parse_pubs = False
                    parse_srvs = False
                    parse_actions = False
                    continue
                elif line.strip().startswith("### Subscribers"):
                    parse_params = False
                    parse_subs = True
                    parse_pubs = False
                    parse_srvs = False
                    parse_actions = False
                    continue
                elif line.strip().startswith("### Publishers"):
                    parse_params = False
                    parse_subs = False
                    parse_pubs = True
                    parse_srvs = False
                    parse_actions = False
                    continue
                elif line.strip().startswith("### Services"):
                    parse_params = False
                    parse_subs = False
                    parse_pubs = False
                    parse_srvs = True
                    parse_actions = False
                    continue
                elif line.strip().startswith("### Actions"):
                    parse_params = False
                    parse_subs = False
                    parse_pubs = False
                    parse_srvs = False
                    parse_actions = True
                    continue
                elif line.strip().startswith("### "):
                    # Update last node
                    if len(self.nodes) > 0:
                        self.nodes[node_ctr - 1].parameters = self._dict_to_list(params)
                        self.nodes[node_ctr - 1].publishers = self._dict_to_list(pubs)
                        self.nodes[node_ctr - 1].subscribers = self._dict_to_list(subs)
                        self.nodes[node_ctr - 1].services = self._dict_to_list(srvs)
                        self.nodes[node_ctr - 1].actions = self._dict_to_list(actions)
                    # Rest flags
                    parse_params = False
                    parse_subs = False
                    parse_pubs = False
                    parse_srvs = False
                    parse_actions = False
                    # Empty dicts
                    params = {}
                    pubs = {}
                    subs = {}
                    srvs = {}
                    actions = {}
                    # Create new node
                    curr_node = Node()
                    curr_node.name = line.strip()[4:]
                    self.nodes.append(curr_node)
                    node_ctr = node_ctr + 1
                    continue

                if parse_params:
                    if line.startswith("- **"):
                        name = line.split("**`")[1].split("`**")[0]
                        if name:
                            match = re.search(r"\((.*?)\)", line)
                            if match:
                                data_type = match.group(1)
                            else:
                                data_type = ""
                            if "type" not in params:
                                params[name] = {"type": data_type}
                    elif line.startswith("    "):
                        params[name]["desc"] = line.strip()
                        name = None
                    continue

                elif parse_subs:
                    if line.startswith("- **"):
                        name = line.split("**`")[1].split("`**")[0]
                        if name:
                            match = re.search(r"\((.*?)\)", line)
                            if match:
                                data_type = match.group(1)
                            else:
                                data_type = ""
                            if "type" not in subs:
                                subs[name] = {"type": data_type}
                    elif line.startswith("    "):
                        subs[name]["desc"] = line.strip()
                        name = None
                    continue

                elif parse_pubs:
                    if line.startswith("- **"):
                        name = line.split("**`")[1].split("`**")[0]
                        if name:
                            match = re.search(r"\((.*?)\)", line)
                            if match:
                                data_type = match.group(1)
                            else:
                                data_type = ""
                            if "type" not in pubs:
                                pubs[name] = {"type": data_type}
                    elif line.startswith("    "):
                        pubs[name]["desc"] = line.strip()
                        name = None
                    continue

                elif parse_srvs:
                    if line.startswith("- **"):
                        name = line.split("**`")[1].split("`**")[0]
                        if name:
                            match = re.search(r"\((.*?)\)", line)
                            if match:
                                data_type = match.group(1)
                            else:
                                data_type = ""
                            if "type" not in srvs:
                                srvs[name] = {"type": data_type}
                    elif line.startswith("    "):
                        srvs[name]["desc"] = line.strip()
                        name = None
                    continue

                elif parse_actions:
                    if line.startswith("- **"):
                        name = line.split("**`")[1].split("`**")[0]
                        if name:
                            match = re.search(r"\((.*?)\)", line)
                            if match:
                                data_type = match.group(1)
                            else:
                                data_type = ""
                            if "type" not in actions:
                                actions[name] = {"type": data_type}
                    elif line.startswith("    "):
                        actions[name]["desc"] = line.strip()
                        name = None

            # EOF was reached
            self.nodes[node_ctr - 1].parameters = self._dict_to_list(params)
            self.nodes[node_ctr - 1].publishers = self._dict_to_list(pubs)
            self.nodes[node_ctr - 1].subscribers = self._dict_to_list(subs)
            self.nodes[node_ctr - 1].services = self._dict_to_list(srvs)
            self.nodes[node_ctr - 1].actions = self._dict_to_list(actions)

    def get_nodes(self):
        return self.nodes

    def get_node_names(self):
        node_names = []
        for node in self.nodes:
            node_names.append(node.name)
        return node_names

    def get_node(self, name):
        for node in self.nodes:
            if node.name == name:
                return node
        return False

    def _dict_to_list(self, dictionary):
        output_list = []
        for key in dictionary:
            output_list.append(
                {
                    "name": f"{key}",
                    "type": dictionary[key]["type"],
                    "description": dictionary[key]["desc"],
                }
            )
        return output_list
