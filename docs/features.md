# Features

## 3D Lane Detection
🛣️ The [OpenLane-V1](https://github.com/OpenDriveLab/OpenLane) dataset, which is the first real-world and the largest scaled 3D lane dataset to date, provides lane line annotations in 3D space.
Similarly, we annotate 3D lane centerlines and include the F-Score for evaluating predicted results  of undirected lane centerlines.
Furthermore, we define the subtask of 3D lane detection as detecting directed 3D lane centerlines from the given multi-view images covering the whole horizontal FOV.

<p align="center">
  <img src="https://github.com/OpenDriveLab/OpenLane-V2/assets/29263416/16f9264e-1693-469d-880e-876449788cb4" width="696px" >
</p>

## Traffic Element Recognition
🚥 Traffic elements and their attribute provide crucial information for autonomous vehicles.
The attribute represents the semantic meaning of a traffic element, such as the red color of a traffic light. 
In this subtask, on the given image in the front view, the location of traffic elements (traffic lights and road signs) and their attributes are demanded to be perceived simultaneously.
Compared to typical 2D detection datasets, the challenge is that the size of traffic elements is tiny due to the large scale of outdoor environments.

<p align="center">
  <img src="https://github.com/OpenDriveLab/OpenLane-V2/assets/29263416/bc35d569-7df0-4499-a98e-3b43a67aff1d" width="696px" >
</p>

## Topology Recognition
🕸️ Given multi-view images, the model learns to recognize the topology relationships among lane centerlines and between lane centerlines and traffic elements.
The most similar task is link prediction in the field of graph, in which the vertices are given and only edges are predicted by models.
In our case, both vertices and edges are unknown for the model.
Thus, lane centerlines and traffic elements are needed to be detected first, and then the topology relationships are built.

<p align="center">
  <img src="https://github.com/OpenDriveLab/OpenLane-V2/assets/29263416/c7c1fc1e-ea26-4a71-b3d2-8baaa3afb08c" width="696px" >
</p>

## SD Map
🧭 The standard-definition map (SD map) comprises road-level topology information and is commonly utilized for routing and navigation.
SD maps serve as extra sensor inputs to offer preliminary knowledge.

<p align="center">
  <img src="https://github.com/OpenDriveLab/OpenLane-V2/assets/29263416/38e25241-b831-4002-9791-e92d115c1c3f" width="696px" >
</p>

## Map Element Bucket
🗺️ Except for the centerline, a lane segment includes lanelines that define the boundaries of a lane and incorporate line types for particular purposes such as lane switching.
Road boundaries and pedestrian crossing are represented as special areas which contribute to regulating the behaviors of vehicles.
This update preserves the essence of the standard version of OpenLane-V2 while supplementing with additional elements to provide unified representations of the static driving scenes.

<p align="center">
  <img src="https://github.com/OpenDriveLab/OpenLane-V2/assets/29263416/64465460-265c-4df0-a7b2-59774761e03c" width="696px" >
</p>
