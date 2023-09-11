#!/bin/bash
set -e

# setup ros environment
source "/opt/ros/$ROS_DISTRO/setup.bash"
source "/colcon_ws/install/setup.bash"

# run ros2autodoc
NODE=""
PACKAGE=""

while getopts ":n:p:" opt; do
    case "${opt}" in
        n)
            NODE=${OPTARG}
            ;;
        p)
            PACKAGE=${OPTARG}
            ;;
        *)
            exit
            ;;
    esac
done

if [[ "$NODE" = "" ]]; then
    echo "No nodes are provided. Exiting container."
    exit
elif [[ "$PACKAGE" = "" ]]; then
    ros2 autodoc generate "$NODE"
    exit
else
    ros2 autodoc generate "$NODE" --package-name "$PACKAGE"
    exit
fi