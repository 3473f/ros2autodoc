# ros2autodoc

[![Colcon Build](https://github.com/3473f/ros2autodoc/actions/workflows/colcon_build.yml/badge.svg)](https://github.com/3473f/ros2autodoc/actions/workflows/colcon_build.yml)
[![Ament Lint](https://github.com/3473f/ros2autodoc/actions/workflows/ament_lint.yml/badge.svg)](https://github.com/3473f/ros2autodoc/actions/workflows/ament_lint.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/b865f4364ab1cc6a5ae3/maintainability)](https://codeclimate.com/github/3473f/ros2autodoc/maintainability)

## Overview

The `ros2autodoc` package provides a ROS2 command line interface tool to automatically generate documentation for ROS2 nodes.
The tool outputs an initial documentation file detailing the interface (parameters, publishers, subscribers, services and actions) for a running ROS2 node. The package was tested with ROS2 Foxy, Humble and Iron.

## Installation

1. Install a recent ROS2 version.
2. Make sure that `colcon` is installed:

```shell
sudo apt install python3-colcon-common-extensions
```

3. Clone this repo into your workspace:

```shell
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws
git clone https://github.com/3473f/ros2autodoc src/ros2autodoc
```

4. Build the workspace:

```shell
colcon build
source install/setup.bash
```

## Usage

### Generate

```shell
$ ros2 autodoc generate --help

usage: ros2 autodoc generate [-h] [--nodes [node ...]] [--executables [executables ...]] [--output-dir] [--seperate-files] package_name

Automatically generate documentation for a ROS2 node

positional arguments:
  package_name          name of the package containing the nodes to be documented.

options:
  -h, --help            show this help message and exit
  --nodes [node ...]    name of the nodes to be documented.
  --executables [executables ...]
                        name of the executables for the nodes to be documented.
  --output-dir          the directory where documentation should be written. If not specified, the file will be saved to the current directory.
  --seperate-files      when this option is set, the node documentation will be written to separate files and no package documentation will be generated

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

usage: ros2 autodoc check [-h] [--nodes [node ...]] [--executables [executables ...]] package_name input_file

Check if a ROS2 node API is documented

positional arguments:
  package_name          name of the package containing the nodes to be documented.
  input_file            absolute path of the documentation of the nodes.

options:
  -h, --help            show this help message and exit
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
