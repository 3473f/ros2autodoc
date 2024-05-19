# ROS2 node API
from ros2node.api import (
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
    "qos_overrides./tf.publisher.depth",
    "qos_overrides./tf.publisher.durability",
    "qos_overrides./tf.publisher.history",
    "qos_overrides./tf.publisher.reliability",
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
TODO = "TODO: description"


class NodeInterfaceCollector:
    def __init__(self, node, node_name):
        self.node = node
        self.node_name = node_name
        self.interfaces = {
            "parameters": {},
            "subscribers": {},
            "publishers": {},
            "services": {},
            "actions": {},
        }

    def get_interfaces(self):
        """Get the interfaces for the given node."""
        self._query_interfaces()
        return self.interfaces

    def _query_interfaces(self):
        # Parameters
        param_names, params_map, desciption_map = self._get_parameters()
        if param_names:
            self._add_parameter_info(param_names, params_map, desciption_map)

        # Subscribers
        subscribers = get_subscriber_info(
            node=self.node, remote_node_name=self.node_name, include_hidden=False
        )
        if subscribers:
            self._add_interface_info(
                self.interfaces["subscribers"], subscribers, SUBSCRIBERS_TO_IGNORE
            )

        # Publishers
        publishers = get_publisher_info(
            node=self.node, remote_node_name=self.node_name, include_hidden=False
        )
        if publishers:
            self._add_interface_info(
                self.interfaces["publishers"], publishers, PUBLISHERS_TO_IGNORE
            )

        # Services
        service_servers = get_service_server_info(
            node=self.node, remote_node_name=self.node_name, include_hidden=False
        )
        if service_servers:
            filtered_services = [
                srv
                for srv in service_servers
                if not self._ignore_service(self.node_name, srv.name)
            ]
            self._add_interface_info(self.interfaces["services"], filtered_services, [])

        # Actions
        actions_servers = get_action_server_info(
            node=self.node, remote_node_name=self.node_name, include_hidden=False
        )
        if actions_servers:
            self._add_interface_info(self.interfaces["actions"], actions_servers, [])

    def _add_interface_info(self, interface_dict, items, ignore_list):
        for item in items:
            if item.name not in ignore_list:
                interface_dict[item.name] = {
                    "type": ", ".join(item.types),
                    "description": TODO,
                }

    def _add_parameter_info(self, param_names, params_map, desciption_map):
        for param in param_names:
            if param not in PARAMS_TO_IGNORE:
                param_type = params_map[param]
                param_description = desciption_map.get(param, TODO)
                self.interfaces["parameters"][param] = {
                    "type": param_type,
                    "description": param_description,
                }

    def _get_parameters(self):
        name_to_type_map = {}
        name_to_description_map = {}
        parameter_names = call_list_parameters(node=self.node, node_name=self.node_name)
        sorted_names = sorted(parameter_names)
        resp = call_describe_parameters(
            node=self.node, node_name=self.node_name, parameter_names=sorted_names
        )
        for descriptor in resp.descriptors:
            name_to_type_map[descriptor.name] = get_parameter_type_string(
                descriptor.type
            )
            name_to_description_map[descriptor.name] = descriptor.description
        return sorted_names, name_to_type_map, name_to_description_map

    def _ignore_service(self, node_name, srv_name):
        return any(srv_name == "/" + node_name + srv for srv in SERVICES_TO_IGNORE)
