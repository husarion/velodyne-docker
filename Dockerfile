ARG ROS_DISTRO=humble
ARG PREFIX=
FROM husarnet/ros:${PREFIX}${ROS_DISTRO}-ros-core

ARG ROS_DISTRO
ARG PREFIX

SHELL ["/bin/bash", "-c"]

WORKDIR /ros2_ws

RUN apt-get update && apt-get install -y \
        python3-transforms3d \
        ros-${ROS_DISTRO}-velodyne \
        ros-${ROS_DISTRO}-nav2-common && \
    source /opt/ros/$ROS_DISTRO/setup.bash && \
    echo $(cat /opt/ros/$ROS_DISTRO/share/velodyne_driver/package.xml | grep '<version>' | sed -r 's/.*<version>([0-9]+.[0-9]+.[0-9]+)<\/version>/\1/g') >> /version.txt && \
    # Size optimalization
    apt-get clean && \
    rm -rf src build && \
    rm -rf /var/lib/apt/lists/*

COPY demo/config/ /config
COPY demo/velodyne.launch.py /
