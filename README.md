# ros2autodoc

![humble_build](https://github.com/3473f/ros2autodoc/actions/workflows/humble_build.yml/badge.svg)
[![Maintainability](https://api.codeclimate.com/v1/badges/b865f4364ab1cc6a5ae3/maintainability)](https://codeclimate.com/github/3473f/ros2autodoc/maintainability)

## Overview

The ros2autodoc package provides a ROS2 command line interface tool to automatically generate documentation for ROS2 nodes. The tool outputs an initial documentation file detailing the interface (parameters, publishers, subscribers, services and actions) for a running ROS2 node.

## Installation

1. Install ROS Galactic or Humble.
2. Make sure that `colcon` is installed:

    ```
    sudo apt install python3-colcon-common-extensions
    ```

3. Clone this repo into your workspace:

    ```
    mkdir -p ~/ros2_ws/src
    cd ~/ros2_ws
    git clone https://github.com/3473f/ros2autodoc ./src
    ```

4. Build the workspace:

    ```
    colcon build
    source install/setup.bash
    ```

## Usage
```
$ ros2 autodoc generate --help

usage: ros2 autodoc generate [-h] [--output-dir OUTPUT_DIR] package_name [node ...]

Automatically generate documentation for a ROS2 node

positional arguments:
  package_name          name of the package to be documented.
  node                  name of the nodes to be documented. If not specified, all running nodes from the package will be documented.

options:
  -h, --help            show this help message and exit
  --output-dir OUTPUT_DIR
                        the directory where documentation should be written.

```

## Example

We are going to demonstrate the usage of this package using the turtlesim package included in ROS2.

First, run the turtlesim node:
```
ros2 run turtlesim turtlesim_node
```
Next, run the draw_square node in another terminal:
```
ros2 run turtlesim draw_square
```
Finally, generate the documentation for these two nodes by running this command in a new terminal:
```
ros2 autodoc generate turtlesim turtlesim draw_square
```

This should output the following [README.md](https://github.com/3473f/ros2autodoc/blob/main/example/README.md) file to your current working directory.
