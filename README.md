


Build the docker image with the following command:

```
docker build -t reliable-rosbag .
```

Run the docker image with the following command:

```
docker run -it -v ${PWD}:/app/ reliable-rosbag 
```

Now you can run the reliable-rosbag.py script from the docker container with the following command:

```
python3 reliable-rosbag.py <bag-name> -t <topic1> -t <topic2> ...
```


## Usage

```
user106_2017-03-08.bag -t /naoqi_driver_node/camera/front/image_raw -t /naoqi_driver_node/camera/bottom/image_raw
```

python3 reliable-rosbag/reliable-rosbag.py user106_2017-03-08.bag -t /naoqi_driver_node/camera/front/image_raw -t /naoqi_driver_node/camera/bottom/image_raw


docker run -it --rm --name reliable-rosbag -v $(pwd):/home/reliable-rosbag reliable-rosbag user106_2017-03-08.bag -t /naoqi_driver_node/camera/front/image_raw -t /naoqi_driver_node/camera/bottom/image_raw

ENTRYPOINT ["/bin/bash", "-c", "source /root/.bashrc && python3 reliable-rosbag.py"]

docker exec -it reliable-rosbag user106_2017-03-08.bag -t /naoqi_driver_node/camera/front/image_raw -t /naoqi_driver_node/camera/bottom/image_raw
