# ros2autodoc

![humble_build](https://github.com/3473f/ros2autodoc/actions/workflows/humble_build.yml/badge.svg)

## Overview

The ros2autodoc package provides a ROS2 command line interface tool to automatically generate documentation for ROS2 nodes. The tool outputs an initial documentation file detailing the interface (parameters, publishers, subscribers, services and actions) for a running ROS2 node.

## Progress

- [x] Access the parameters, publishers, subscribers, services, actions for the nodes (proof of concept)
- [x] Implement the interface for the user
- [ ] Write the documentation out in markdown format
### turtlesim

#### Parameters
- **`background_b`** (integer)

	TODO: description

- **`background_g`** (integer)

	TODO: description

- **`background_r`** (integer)

	TODO: description

#### Subscribers
- **`/turtle1/cmd_vel`** (geometry_msgs/msg/Twist)

	TODO: description

#### Publishers
- **`/turtle1/color_sensor`** (turtlesim/msg/Color)

	TODO: description

- **`/turtle1/pose`** (turtlesim/msg/Pose)

	TODO: description

#### Services
- **`/clear`** (std_srvs/srv/Empty)

	TODO: description

- **`/kill`** (turtlesim/srv/Kill)

	TODO: description

- **`/reset`** (std_srvs/srv/Empty)

	TODO: description

- **`/spawn`** (turtlesim/srv/Spawn)

	TODO: description

- **`/turtle1/rotate_absolute/_action/cancel_goal`** (action_msgs/srv/CancelGoal)

	TODO: description

- **`/turtle1/rotate_absolute/_action/get_result`** (turtlesim/action/RotateAbsolute_GetResult)

	TODO: description

- **`/turtle1/rotate_absolute/_action/send_goal`** (turtlesim/action/RotateAbsolute_SendGoal)

	TODO: description

- **`/turtle1/set_pen`** (turtlesim/srv/SetPen)

	TODO: description

- **`/turtle1/teleport_absolute`** (turtlesim/srv/TeleportAbsolute)

	TODO: description

- **`/turtle1/teleport_relative`** (turtlesim/srv/TeleportRelative)

	TODO: description

#### Actions
- **`/turtle1/rotate_absolute`** (turtlesim/action/RotateAbsolute)

	TODO: description

### draw_square

#### Parameters
#### Subscribers
- **`/turtle1/pose`** (turtlesim/msg/Pose)

	TODO: description

#### Publishers
- **`/turtle1/cmd_vel`** (geometry_msgs/msg/Twist)

	TODO: description

#### Services
