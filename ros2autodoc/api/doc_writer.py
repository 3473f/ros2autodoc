import os

class DocWriter():
    def __init__(self, package_name, node_name, directory):
        self.file = directory + '/README.md'

        if os.path.exists(self.file):
            with open(self.file, "a") as f:
                f.write('### ' + node_name + '\n\n')
        else:
            with open(self.file, "w") as f:
                f.write('# ' + package_name + '\n\n'
                        '## Overview\n\n'
                        'TODO: package describtion\n\n'
                        '## Installation\n\n'
                        'TODO: installation instructions\n\n'
                        '## Usage\n\n'
                        'TODO: running instructions\n\n'
                        '## Config files\n\n'
                        'TODO: add config files\n\n'
                        '## Nodes\n\n'
                        '### ' + node_name + '\n\n')

    def write_parameters(self, params):
        with open(self.file, "a") as f:
            f.write('#### Parameters\n')

    def write_publishers(self, publishers):
        with open(self.file, "a") as f:
            f.write('#### Publishers\n')

    def write_service_servers(self, services):
        with open(self.file, "a") as f:
            f.write('#### Services\n')

    def write_action_servers(self, actions):
        with open(self.file, "a") as f:
            f.write('#### Actions\n')