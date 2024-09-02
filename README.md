# velodyne-docker

Dockerized Velodyne LiDAR package.

## Velodyne configuration

Connect to Velodyne using an ethernet cable.

To access the sensor's Web Interface, you must know the sensor's IP. You can find it for example using `nmap`:

Find your ethernet IP:

```bash
ifconfig
```

Use your ethernet IP to find devices in the same network. You need to replace the last number of IP with 0/24 for example if your IP is 10.15.20.1 then:

```bash
nmap -sn 10.15.20.0/24
```

This will list all devices in the same network including Velodyne.

Then you need to specify the host to which Velodyne will be able to send data. In the browser enter the sensor IP to access Web Interface.
Go to **Host (Destination)** and change IP Address to your device.
Click the **set** button on the right, then go to the bottom and click the **Save configuration** button.

For more information about Velodyne configuration refer to official User Manuals.

If you find an IP of Velodyne change [configuration file](./demo/config/panther_velodyne_driver.yaml) to connect to the sensor.

## Run Velodyne in docker

Clone this repo:

```bash
git clone -b ros2 https://github.com/husarion/velodyne-docker
```

Sensor's parameters can be changed, by editing or providing your own config files and mounting them into the container. Default config files are located in [config](./demo/config/) directory.

Run docker compose:

```bash
cd velodyne-docker/demo
docker compose up
```

You should be able to see sensor data on the `/panther/velodyne/velodyne_points` topic with standard `sensor_msgs/msg/PointCloud2` message type.

## Parameters

The image includes a custom `velodyne.launch.py` file, which is based on the official Velodyne package but includes additional configurations for easier integration with Husarion robots. This launch file contains the following parameters:

| **Parameter**           | **Description** | **Default Value** |
| ----------------------- | --------------- | ----------------- |
| `device_namespace`      | Namespace for the device, utilized in TF frames and preceding device topics. This aids in differentiating between multiple devices on the same robot. | `"velodyne"` |
| `driver_params_file`    | Path to the parameter file for the velodyne_driver_node node. | `"/config/panther_velodyne_driver.yaml"` |
| `robot_namespace`       | Namespace to all launched nodes and use namespace as tf_prefix. This aids in differentiating between multiple robots with the same devices. | `env("ROBOT_NAMESPACE")` (`""` if not specified) |
| `transform_params_file` | Path to the parameter file for the velodyne_transform_node node. | `"/config/panther_velodyne_pointcloud.yaml"`     |
| `x`                     | Initial robot position in the global 'x' axis. | `0.185` |
| `y`                     | Initial robot position in the global 'y' axis. | `0.0`   |
| `z`                     | Initial robot position in the global 'z' axis. | `0.209` |
| `roll`                  | Initial robot 'roll' orientation.              | `0.0`   |
| `pitch`                 | Initial robot 'pitch' orientation.             | `0.0`   |
| `yaw`                   | Initial robot 'yaw' orientation.               | `0.0`   |

Using both `device_namespace` and `robot_namespace` makes:

- Topic: `{robot_namespace}/{device_namespace}/{default_topic}`
- URDF Link: `{robot_namespace}/{device_namespace}`

> [!IMPORTANT]
> The default configuration files are set up for the VLP16 LIDAR model. If you are using a different model, it is recommended to adjust the configuration files accordingly. For guidance, refer to the [Velodyne ROS2 driver repository](https://github.com/ros-drivers/velodyne/tree/ros2).
