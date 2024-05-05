import os

TODO = "TODO: description\n\n"


class DocWriter:
    def __init__(self, package_name, node_name, interfaces):
        self.package_name = package_name
        self.node_name = node_name
        self.interfaces = interfaces

    def write(self, path):
        if not os.path.exists(path) and self.package_name is not None:
            with open(path, "w", encoding="utf-8") as f:
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
                )

        with open(path, "a", encoding="utf-8") as f:
            f.write("### " + self.node_name + "\n\n")
            if self.interfaces["parameters"]:
                f.write("### Parameters\n\n")
                for name, entry in self.interfaces["parameters"].items():
                    self._write_entry(f, name, entry)
            if self.interfaces["subscribers"]:
                f.write("### Subscribers\n\n")
                for name, entry in self.interfaces["subscribers"].items():
                    self._write_entry(f, name, entry)
            if self.interfaces["publishers"]:
                f.write("### Publishers\n\n")
                for name, entry in self.interfaces["publishers"].items():
                    self._write_entry(f, name, entry)
            if self.interfaces["services"]:
                f.write("### Services\n\n")
                for name, entry in self.interfaces["services"].items():
                    self._write_entry(f, name, entry)
            if self.interfaces["actions"]:
                for name, entry in self.interfaces["actions"].items():
                    self._write_entry(f, name, entry)

    def _write_entry(self, file, name, entry):
        _type = entry["type"]
        _description = entry["description"]
        file.write(f"- **`{name}`** ({_type})\n\n")
        file.write(f"    {_description}\n\n")
