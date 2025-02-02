# ros2autodoc

[![Colcon Build](https://github.com/3473f/ros2autodoc/actions/workflows/colcon_build.yml/badge.svg)](https://github.com/3473f/ros2autodoc/actions/workflows/colcon_build.yml)
[![Ament Lint](https://github.com/3473f/ros2autodoc/actions/workflows/ament_lint.yml/badge.svg)](https://github.com/3473f/ros2autodoc/actions/workflows/ament_lint.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/b865f4364ab1cc6a5ae3/maintainability)](https://codeclimate.com/github/3473f/ros2autodoc/maintainability)

## Overview

The `ros2autodoc` package extends the ROS 2 CLI tools to generate API documentation for ROS2 nodes, update previously generated documentation or check if a node is documented for use in CI/CD jobs. The tool outputs a markdown file in the style of ROS Wiki.

## Installation

1. Clone this repo into your workspace:

```shell
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws
git clone https://github.com/3473f/ros2autodoc src/ros2autodoc
```

2. Build the workspace:

```shell
colcon build
source install/setup.bash
```

## Usage

### Generate

```shell
$ ros2 autodoc generate --help

usage: ros2 autodoc generate [-h] [--nodes [node ...]] [--executables [executables ...]] [--launch-file launch_file]
                             [--output-dir] [--seperate-files]
                             package_name

Automatically generate documentation for a ROS2 node

positional arguments:
  package_name          name of the package containing the nodes to be documented.

options:
  -h, --help            show this help message and exit
  --nodes [node ...]    name of the nodes to be documented.
  --executables [executables ...]
                        name of the executables for the nodes to be documented.
  --launch-file launch_file
                        name of the launch file to start the nodes.
  --output-dir          the directory where documentation should be written. If not specified, the file will be saved
                        to the current directory.
  --seperate-files      when this option is set, the node documentation will be written to separate files and no
                        package documentation will be generated.

```

### Example

We are going to demonstrate the usage of this package using the turtlesim package included in ROS2.

```shell
ros2 autodoc generate turtlesim --nodes turtlesim draw_square --executables turtlesim_node draw_square
```

This should output the following [README.md](https://github.com/3473f/ros2autodoc/blob/main/example/README.md) file to your current working directory.

### Check

```shell
$ ros2 autodoc check --help

usage: ros2 autodoc check [-h] [--launch-file launch_file] [--nodes [node ...]] [--executables [executables ...]] package_name input_file

Check if a ROS2 node API is documented

positional arguments:
  package_name          name of the package containing the nodes to be documented.
  input_file            absolute path of the documentation of the nodes.

options:
  -h, --help            show this help message and exit
  --launch-file launch_file
                        name of the launch file to start the nodes.
  --nodes [node ...]    name of the nodes to be documented.
  --executables [executables ...]
                        name of the executables for the nodes to be documented.
```

### Example

Check if the node interfaces are listed properly in the file:

```shell
ros2 autodoc check turtlesim path/to/ros2autodoc/src/example/README.md --nodes turtlesim --executables turtlesim_node
```

This should output the following and exit

```shell
Node 'turtlesim' interfaces are correctly listed.
```

### Update

```shell
usage: ros2 autodoc update [-h] [node ...] input_file

Update the documentation of a ROS2 node

positional arguments:
  node        name of the nodes to be documented. If not specified, all running nodes from the package will be documented.
  input_file  absolute path of the README.md file to be updated.

options:
  -h, --help  show this help message and exit
```
