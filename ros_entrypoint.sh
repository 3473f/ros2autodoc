#!/bin/bash
set -e

# setup ros environment
source "/opt/ros/$ROS_DISTRO/setup.bash"
source "/colcon_ws/install/setup.bash"

# debugging
echo "Package is: $package"
echo "Node is: $node"

# run ros2autodoc
if [[ -z "$package" ]]; then
    if [[ -z "$node" ]]; then
        echo "No nodes are provided. Exiting container."
    else
        ros2 autodoc generate "$node"
    fi
elif [[ -z "$node" ]]; then
    echo "No nodes are provided. Exiting container."
else
    ros2 autodoc generate "$node" --package-name "$package"
    echo "Documentation generated successfully!"
fi