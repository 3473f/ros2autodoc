import os

PARAMS_TO_IGNORE = ["use_sim_time",
                    "qos_overrides./parameter_events.publisher.depth",
                    "qos_overrides./parameter_events.publisher.durability",
                    "qos_overrides./parameter_events.publisher.history",
                    "qos_overrides./parameter_events.publisher.reliability"]
SUBSCRIBERS_TO_IGNORE = ["/parameter_events"]
PUBLISHERS_TO_IGNORE = ["/parameter_events", "/rosout"]
SERVICES_TO_IGNORE = ["/describe_parameters",
                      "/get_parameter_types",
                      "/get_parameters",
                      "/list_parameters",
                      "/set_parameters",
                      "/set_parameters_atomically"]

class DocWriter():
    def __init__(self, package_name, node_name, directory):
        self.node_name = node_name
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

    def write_parameters(self, param_names, params_map):
        with open(self.file, "a") as f:
            f.write('#### Parameters\n')
        for param in param_names:
            if param not in PARAMS_TO_IGNORE:
                param_type = params_map[param]
                with open(self.file, "a") as f:
                    f.write('- **`{name}`** ({type})\n\n'.format(
                                        name=param, type=param_type))
                    f.write('\tTODO: description\n\n')

    def write_subscribers(self, subscribers):
        with open(self.file, "a") as f:
            f.write('#### Subscribers\n')
        for sub in subscribers:
            if sub.name not in SUBSCRIBERS_TO_IGNORE:
                with open(self.file, "a") as f:
                    f.write('- **`{name}`** ({type})\n\n'.format(
                                name=sub.name, type=', '.join(sub.types)))
                    f.write('\tTODO: description\n\n')
        
    def write_publishers(self, publishers):
        with open(self.file, "a") as f:
            f.write('#### Publishers\n')
        for pub in publishers:
            if pub.name not in PUBLISHERS_TO_IGNORE:
                with open(self.file, "a") as f:
                    f.write('- **`{name}`** ({type})\n\n'.format(
                                name=pub.name, type=', '.join(pub.types)))
                    f.write('\tTODO: description\n\n')

    def write_service_servers(self, services):
        with open(self.file, "a") as f:
            f.write('#### Services\n')
        for srv in services:
            if not self._ignore_service(srv.name):
                with open(self.file, "a") as f:
                    f.write('- **`{name}`** ({type})\n\n'.format(
                                name=srv.name, type=', '.join(srv.types)))
                    f.write('\tTODO: description\n\n')

    def _ignore_service(self, srv_name):
        for srv in SERVICES_TO_IGNORE:
            if srv_name == '/' + self.node_name + srv:
                return True
        return False
    
    def write_action_servers(self, actions):
        with open(self.file, "a") as f:
            f.write('#### Actions\n')
        for action in actions:
            with open(self.file, "a") as f:
                f.write('- **`{name}`** ({type})\n\n'.format(
                            name=action.name, type=', '.join(action.types)))
                f.write('\tTODO: description\n\n')
