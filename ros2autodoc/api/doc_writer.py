import os

PARAMS_TO_IGNORE = [
    "use_sim_time",
    "qos_overrides./parameter_events.publisher.depth",
    "qos_overrides./parameter_events.publisher.durability",
    "qos_overrides./parameter_events.publisher.history",
    "qos_overrides./parameter_events.publisher.reliability",
]
SUBSCRIBERS_TO_IGNORE = ["/parameter_events"]
PUBLISHERS_TO_IGNORE = ["/parameter_events", "/rosout"]
SERVICES_TO_IGNORE = [
    "/describe_parameters",
    "/get_parameter_types",
    "/get_parameters",
    "/list_parameters",
    "/set_parameters",
    "/set_parameters_atomically",
]
TODO = "TODO: description\n\n"


class DocWriter:
    def __init__(self, package_name, node_name, directory):
        self.package_name = package_name
        self.node_name = node_name
        self.file = directory + "/README.md"
        self.parameters = []
        self.subscribers = []
        self.publishers = []
        self.services = []
        self.actions = []

    def get_parameters(self, param_names, params_map):
        for param in param_names:
            if param not in PARAMS_TO_IGNORE:
                param_type = params_map[param]
                self.parameters.append({"name": param, "type": param_type})

    def get_subscribers(self, subscribers):
        for sub in subscribers:
            if sub.name not in SUBSCRIBERS_TO_IGNORE:
                self.subscribers.append(
                    {"name": sub.name, "type": ", ".join(sub.types)}
                )

    def get_publishers(self, publishers):
        for pub in publishers:
            if pub.name not in PUBLISHERS_TO_IGNORE:
                self.publishers.append({"name": pub.name, "type": ", ".join(pub.types)})

    def get_service_servers(self, services):
        for srv in services:
            if not self._ignore_service(srv.name):
                self.services.append({"name": srv.name, "type": ", ".join(srv.types)})

    def _ignore_service(self, srv_name):
        return any(srv_name == "/" + self.node_name + srv for srv in SERVICES_TO_IGNORE)

    def get_action_servers(self, actions):
        for action in actions:
            self.actions.append({"name": action.name, "type": ", ".join(action.types)})

    def write(self):
        if os.path.exists(self.file):
            with open(self.file, "a", encoding="utf-8") as f:
                f.write("##\n\n")
                f.write("### " + self.node_name + "\n\n")
        else:
            with open(self.file, "w", encoding="utf-8") as f:
                f.write(
                    "# " + self.package_name + "\n\n"
                    "## Overview\n\n"
                    f"{TODO}"
                    "## Installation\n\n"
                    f"{TODO}"
                    "## Usage\n\n"
                    f"{TODO}"
                    "## Config files\n\n"
                    f"{TODO}"
                    "## Nodes\n\n"
                    "### " + self.node_name + "\n\n"
                )

        with open(self.file, "a", encoding="utf-8") as f:
            if self.parameters:
                f.write("### Parameters\n\n")
                for param in self.parameters:
                    self._write_item(f, param)
            if self.subscribers:
                f.write("### Subscribers\n\n")
                for sub in self.subscribers:
                    self._write_item(f, sub)
            if self.publishers:
                f.write("### Publishers\n\n")
                for pub in self.publishers:
                    self._write_item(f, pub)
            if self.services:
                f.write("### Services\n\n")
                for srv in self.services:
                    self._write_item(f, srv)
            if self.actions:
                f.write("### Actions\n\n")
                for action in self.actions:
                    self._write_item(f, action)

    def _write_item(self, file, item):
        _name = item["name"]
        _type = item["type"]
        file.write(f"- **`{_name}`** ({_type})\n\n")
        file.write(f"{TODO}")
