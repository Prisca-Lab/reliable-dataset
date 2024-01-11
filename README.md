# reliable-rosbag
This is a python script that can be used to check the reliability of a rosbag file. 
Here you can find the implementation described in the paper "A Rosbag Tool to Improve Dataset Reliability" by F. Vigni, A. Andriella, S. Rossi.

Running example from UE-HRI Dataset:
- file: user106_2017-03-08.bag
![alt text](img/example.png)


## Usage
You can either directly run the script or use the docker image as described below.


Build the docker image with the following command:
```
docker build -t reliable-rosbag .
```

Run the docker image with the following command:

```
docker run -it -v ${PWD}:/app/ reliable-rosbag 
```

The rosbag is located in the folder where the dockerfile is located.

Now you can run the reliable-rosbag.py script from the docker container with the following command:
```
python3 reliable-rosbag.py <bag-name> -t <topic1> -t <topic2> ...
```

## Example

```
python3 reliable-rosbag.py user106_2017-03-08.bag -t /naoqi_driver_node/camera/front/image_raw -t /naoqi_driver_node/camera/bottom/image_raw -m var
```
