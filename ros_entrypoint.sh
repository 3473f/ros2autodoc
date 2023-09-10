#!/bin/bash
set -e

# setup ros environment
source "/opt/ros/$ROS_DISTRO/setup.bash"
source "/colcon_ws/install/setup.bash"

# run ros2autodoc
if [[ -z "$package_name" ]]; then
    if [[ -z "$node_name" ]]; then
        echo "No nodes are provided. Exiting container."
    else
        ros2 autodoc $node_name
    fi
elif [[ -z "$node_name" ]]; then
    echo "No nodes are provided. Exiting container."
else
    ros2 autodoc $node_name --package-name $package_name
fi
