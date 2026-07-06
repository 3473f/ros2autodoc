import os

TODO = "TODO: description\n\n"

_SECTION_TITLES = {
    "parameters": "### Parameters",
    "subscribers": "### Subscribers",
    "publishers": "### Publishers",
    "services": "### Services",
    "actions": "### Actions",
}


def _default_header(package_name):
    return (
        "# " + package_name + "\n\n"
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


def write_documentation_file(file_path, package_name, preamble_lines, nodes):
    """Atomically (re)write the whole documentation file.

    `nodes` is the full ordered mapping of node_name -> interfaces (untouched
    nodes plus any that were updated), used to rewrite every node section in
    place instead of appending duplicates.
    """
    if preamble_lines:
        content = "".join(preamble_lines)
    else:
        content = _default_header(package_name)

    for node_name, interfaces in nodes.items():
        content += DocWriter(None, node_name, interfaces).render_node_section()

    tmp_path = file_path + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        f.write(content)
    os.replace(tmp_path, file_path)


class DocWriter:
    def __init__(self, package_name, node_name, interfaces):
        self.package_name = package_name
        self.node_name = node_name
        self.interfaces = interfaces

    def render_node_section(self):
        """Render this node's documentation section as a string."""
        lines = ["### " + self.node_name + "\n\n"]
        for interface_type, title in _SECTION_TITLES.items():
            entries = self.interfaces[interface_type]
            if entries:
                lines.append(title + "\n\n")
                for name, entry in entries.items():
                    lines.append(self._render_entry(name, entry))
        return "".join(lines)

    def write(self, path):
        if not os.path.exists(path) and self.package_name is not None:
            with open(path, "w", encoding="utf-8") as f:
                f.write(_default_header(self.package_name))

        with open(path, "a", encoding="utf-8") as f:
            f.write(self.render_node_section())

    def _render_entry(self, name, entry):
        _type = entry["type"]
        _description = entry["description"]
        return f"- **`{name}`** ({_type})\n\n    {_description}\n\n"
