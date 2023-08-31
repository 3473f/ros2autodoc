# BSD 3-Clause License
#
# Copyright (c) 2023, Mohamed Abdelaziz
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#
#    * Neither the name of the the copyright holder nor the names of its
#      contributors may be used to endorse or promote products derived from
#      this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

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

    def get_parameters(self, param_names, params_map, desciption_map):
        for param in param_names:
            if param not in PARAMS_TO_IGNORE:
                param_type = params_map[param]
                param_description = desciption_map[param]
                self.parameters.append(
                    {
                        "name": param,
                        "type": param_type,
                        "description": param_description,
                    }
                )

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
                f.write("### " + self.node_name + "\n\n")
        else:
            if self.package_name is not None:
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
        if "description" in item:
            _description = item["description"]
            file.write(f"\t{_description}\n\n")
        else:
            file.write(f"\t{TODO}")
