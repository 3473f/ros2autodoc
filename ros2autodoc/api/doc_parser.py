import os
import re


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
            parse_params = False
            parse_subs = False
            parse_pubs = False
            parse_srvs = False
            parse_actions = False

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
                    # Rest flags
                    parse_params = False
                    parse_subs = False
                    parse_pubs = False
                    parse_srvs = False
                    parse_actions = False

                    # Create new node
                    curr_node_name = line.strip()[4:]
                    self.nodes[curr_node_name] = {
                        "parameters": {},
                        "subscribers": {},
                        "publishers": {},
                        "services": {},
                        "actions": {},
                    }
                    continue

                if parse_params:
                    if line.startswith("- **"):
                        param_name = line.split("**`")[1].split("`**")[0]
                        if param_name:
                            self.nodes[curr_node_name]["parameters"][param_name] = {
                                "type": "",
                                "description": "",
                            }
                            match = re.search(r"\((.*?)\)", line)
                            if match:
                                data_type = match.group(1)
                            else:
                                data_type = ""
                            self.nodes[curr_node_name]["parameters"][param_name][
                                "type"
                            ] = data_type
                    elif line.startswith("    ") and line.strip():
                        self.nodes[curr_node_name]["parameters"][param_name][
                            "description"
                        ] = line.strip()
                    continue

                elif parse_subs:
                    if line.startswith("- **"):
                        sub_name = line.split("**`")[1].split("`**")[0]
                        if sub_name:
                            self.nodes[curr_node_name]["subscribers"][sub_name] = {
                                "type": "",
                                "description": "",
                            }
                            match = re.search(r"\((.*?)\)", line)
                            if match:
                                data_type = match.group(1)
                            else:
                                data_type = ""
                            self.nodes[curr_node_name]["subscribers"][sub_name][
                                "type"
                            ] = data_type
                    elif line.startswith("    ") and sub_name:
                        self.nodes[curr_node_name]["subscribers"][sub_name][
                            "description"
                        ] = line.strip()
                    continue

                elif parse_pubs:
                    if line.startswith("- **"):
                        pub_name = line.split("**`")[1].split("`**")[0]
                        if pub_name:
                            self.nodes[curr_node_name]["publishers"][pub_name] = {
                                "type": "",
                                "description": "",
                            }
                            match = re.search(r"\((.*?)\)", line)
                            if match:
                                data_type = match.group(1)
                            else:
                                data_type = ""
                            self.nodes[curr_node_name]["publishers"][pub_name][
                                "type"
                            ] = data_type
                    elif line.startswith("    ") and pub_name:
                        self.nodes[curr_node_name]["publishers"][pub_name][
                            "description"
                        ] = line.strip()
                    continue

                elif parse_srvs:
                    if line.startswith("- **"):
                        srvs_name = line.split("**`")[1].split("`**")[0]
                        if srvs_name:
                            self.nodes[curr_node_name]["services"][srvs_name] = {
                                "type": "",
                                "description": "",
                            }
                            match = re.search(r"\((.*?)\)", line)
                            if match:
                                data_type = match.group(1)
                            else:
                                data_type = ""
                            self.nodes[curr_node_name]["services"][srvs_name][
                                "type"
                            ] = data_type
                    elif line.startswith("    ") and srvs_name:
                        self.nodes[curr_node_name]["services"][srvs_name][
                            "description"
                        ] = line.strip()
                    continue

                elif parse_actions:
                    if line.startswith("- **"):
                        action_name = line.split("**`")[1].split("`**")[0]
                        if action_name:
                            self.nodes[curr_node_name]["actions"][action_name] = {
                                "type": "",
                                "description": "",
                            }
                            match = re.search(r"\((.*?)\)", line)
                            if match:
                                data_type = match.group(1)
                            else:
                                data_type = ""
                            self.nodes[curr_node_name]["actions"][action_name][
                                "type"
                            ] = data_type
                    elif line.startswith("    ") and action_name:
                        self.nodes[curr_node_name]["actions"][action_name][
                            "description"
                        ] = line.strip()

    def get_nodes(self):
        return self.nodes
