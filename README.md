# velodyne-docker
Dockerized Velodyne LiDAR package.

## Velodyne configuration

Connect to Velodyne using an ethernet cable.
   
To access the sensor's Web Interface, you must know the sensor's Ip. You can find it for example using `nmap`:

Find your ethernet Ip:

```
ifconfig
```

Use your ethernet Ip to find devices in the same network. You need to replace the last number of Ip with 0/24 for example if your Ip is 10.15.20.1 then:

```
nmap -sn 10.15.20.0/24
```

This will list all devices in the same network including Velodyne.

Then you need to specify the host to which Velodyne will be able to send data. In the browser enter the sensor Ip to access Web Interface. 
Go to **Host (Destination)** and change Ip Address to your device.
Click the **set** button on the right, then go to the bottom and click the **Save configuration** button.

For more information about Velodyne configuration refer to official User Manuals.

## Run Velodyne in docker

Clone this repo:

```
git clone https://github.com/husarion/velodyne-docker
```

Sensor's parameters can be changed inside the `compose.yaml` file.

Run docker compose:

```
cd velodyne-docker
docker compose up
```

You should be able to see sensor data on the `/velodyne_points` topic with standard `sensor_msgs/PointCloud2` message type.

## Run with the Husarion Panther robot

To run the Velodyne Puck sensor with the Husarion Panther robot you need to specify a transform between the robot and LIDAR links. Sensor position relative to the robot can be set by editing the `panther_velodyne.launch` file in the `/panther_velodyne` directory. Then go to the `panther_velodyne` directory and run:

```bash
cd panther_velodyne
docker compose up
```
