# Use the official ROS Noetic image on top of Ubuntu 20.04
FROM osrf/ros:noetic-desktop-full-focal

# Install the dependencies
RUN apt-get update && \
    apt-get install -y python3 python3-pip ros-noetic-rosbag && \
    pip3 install --upgrade pip && \
    echo "source /opt/ros/noetic/setup.bash" >> /root/.bashrc && \
    pip3 install catkin-tools click rich


# Set the working directory
WORKDIR /app

# Copy the script into the container
COPY /reliable-rosbag/reliable-rosbag.py reliable-rosbag.py

ENV PYTHONPATH=$PYTHONPATH:/opt/ros/noetic/lib/python3/dist-packages

# Update the package list, install sudo, create a non-root user, and grant password-less sudo permissions
# Switching to a non-root user

ENTRYPOINT ["/bin/bash"]

# CMD [ "python3", "reliable-rosbag.py"]
