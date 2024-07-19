ARG ROS_DISTRO=humble
ARG PREFIX=
FROM husarnet/ros:${PREFIX}${ROS_DISTRO}-ros-core

ARG ROS_DISTRO
ARG PREFIX

SHELL ["/bin/bash", "-c"]

WORKDIR /ros2_ws

RUN apt-get update && apt-get install -y \
        python3-transforms3d \
        ros-dev-tools \
        ros-${ROS_DISTRO}-velodyne && \
    rosdep init && \
    rosdep update --rosdistro $ROS_DISTRO && \
    rosdep install -i --from-path src --rosdistro $ROS_DISTRO -y && \
    source /opt/ros/$ROS_DISTRO/setup.bash && \
    colcon build --cmake-args -DBUILD_TESTING=OFF -DCMAKE_BUILD_TYPE=Release && \
    echo $(cat /opt/ros/humble/share/velodyne_driver/package.xml | grep '<version>' | sed -r 's/.*<version>([0-9]+.[0-9]+.[0-9]+)<\/version>/\1/g') >> /version.txt && \
    # Size optimalization
    apt-get remove -y \
        ros-dev-tools && \
    apt-get clean && \
    rm -rf src build && \
    rm -rf /var/lib/apt/lists/*

COPY demo/config/ /config
COPY demo/velodyne.launch.py /
