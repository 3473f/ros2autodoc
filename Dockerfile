# Default to ROS Humble
ARG ROS_VERSION=humble
FROM osrf/ros:${ROS_VERSION}-desktop

SHELL [ "/bin/bash", "-c" ]

# Copy ros2autodoc into the container
COPY ./ros2autodoc /colcon_ws/src

# Build the package
WORKDIR /colcon_ws
RUN source /opt/ros/$ROS_DISTRO/setup.bash && \
    colcon build --symlink-install

# Copy ros_entrypoint.sh
COPY --chmod=0755 ros_entrypoint.sh /ros_entrypoint.sh
ENTRYPOINT [ "/ros_entrypoint.sh" ]