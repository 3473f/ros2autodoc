# ROS2 node API
from ros2node.api import (
    INFO_NONUNIQUE_WARNING_TEMPLATE,
    get_action_server_info,
    get_publisher_info,
    get_service_server_info,
    get_subscriber_info,
)

# ROS2 param API
from ros2param.api import (
    call_describe_parameters,
    call_list_parameters,
    get_parameter_type_string,
)

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


class NodeInterfaceCollector:
    def __init__(self):
        self.interfaces = {}

    def get_interfaces(self, node, node_name):
        """ Get the interfaces for the given node."""
        self._query_interfaces(self, node, node_name)
        return self.interfaces

    def _query_interfaces(self, node, node_name):
        # Parameters
        param_names, params_map, desciption_map = self._get_parameters(node, node_name)
        if len(param_names > 0):
            for param in param_names:
                if param not in PARAMS_TO_IGNORE:
                    param_type = params_map[param]
                    param_description = desciption_map[param]
                    if not param_description:
                        param_description = TODO
                    self.interfaces['parameters'][param] = {
                        "type": param_type,
                        "description": param_description,
                    }
        # Subscribers
        subscribers = get_subscriber_info(
            node=node, remote_node_name=node_name, include_hidden=False
        )
        if len(subscribers > 0):
            for sub in subscribers:
                if sub.name not in SUBSCRIBERS_TO_IGNORE:
                    self.interfaces['subscribers'][sub.name] = {
                        "type": ", ".join(sub.types),
                        "description": TODO,
                    }
        # Publishers
        publishers = get_publisher_info(
            node=node, remote_node_name=node_name, include_hidden=False
        )
        if len(publishers > 0):
            for pub in publishers:
                if pub.name not in PUBLISHERS_TO_IGNORE:
                    self.interfaces['publishers'][pub.name] = {
                        "type": ", ".join(pub.types),
                        "description": TODO,
                    }
        # Services
        service_servers = get_service_server_info(
            node=node, remote_node_name=node_name, include_hidden=False
        )
        if len(service_servers > 0):
            for srv in service_servers:
                if not self._ignore_service(srv.name):
                    self.interfaces['services'][srv.name] = {
                        "type": ", ".join(srv.types),
                        "description": TODO,
                    }
        # Actions
        actions_servers = get_action_server_info(
            node=node, remote_node_name=node_name, include_hidden=False
        )
        if len(actions_servers > 0):
            for action in actions_servers:
                self.interfaces['services'][action.name] = {
                    "type": ", ".join(action.types),
                    "description": TODO,
                }

    def _get_parameters(self, node, node_name):
        name_to_type_map = {}
        name_to_description_map = {}
        parameter_names = call_list_parameters(node=node, node_name=node_name)
        sorted_names = sorted(parameter_names)
        resp = call_describe_parameters(
            node=node, node_name=node_name, parameter_names=sorted_names
        )
        for descriptor in resp.descriptors:
            name_to_type_map[descriptor.name] = get_parameter_type_string(descriptor.type)
            name_to_description_map[descriptor.name] = descriptor.description
        return sorted_names, name_to_type_map, name_to_description_map
    
    def _ignore_service(self, srv_name):
        return any(srv_name == "/" + node_name + srv for srv in SERVICES_TO_IGNORE)