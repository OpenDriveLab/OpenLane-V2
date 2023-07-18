<div id="top" align="center">

# OpenLane-V2
**The World's First Perception and Reasoning Benchmark for Scene Structure in Autonomous Driving.**

<a href="#data">
  <img alt="OpenLane-v2: v1.1" src="https://img.shields.io/badge/OpenLane--V2-v1.1-blueviolet"/>
</a>
<a href="#license">
  <img alt="License: Apache2.0" src="https://img.shields.io/badge/license-Apache%202.0-blue.svg"/>
</a>

<!-- **English | [中文](./README-zh-hans.md)**

_In terms of ambiguity, the English version shall prevail._ -->

</div>

<br>

<div align="center">
  <img src="https://github.com/OpenDriveLab/OpenLane-V2/assets/29263416/6ef38e84-b1c6-49c1-bf20-6966562879d6" width="696px">
  <!--  <img src="https://github.com/OpenDriveLab/OpenLane-V2/assets/29263416/9f47c6be-3411-4440-9efa-836a156b7e44" width="696px"> -->
</div>

<br>

## What's New
Compared to lane centerlines, <b>lane segments</b> contain more detailed information, making them more closely aligned with the representation in HD maps and better suited for downstream tasks. In the [Unifying Map Elements Expansion](#unifying-map-elements-%EF%B8%8F), we introduce lane segments as the fundamental building blocks to build the lane network.
![comparison](https://github.com/OpenDriveLab/OpenLane-V2/assets/29263416/bbd02196-322e-48d5-8264-bedd2d03a288)

<!-- <div align="center">
  <img src="https://github.com/OpenDriveLab/OpenLane-V2/assets/29263416/1e57d1c5-aa8f-43e8-85b0-ff229ac5cb21" width="696px">
</div> -->

Besides, in the [SD Map as Prior Expansion](#sd-map-as-prior-), we regard <b>SD maps</b> as extra sensor inputs to provide preliminary knowledge.

## Table of Contents
- [News](#news)
- [Leaderboard](#leaderboard)
- [Highlight](#highlight---why-we-are-exclusive)
- [Task](#task)
  - [3D Lane Detection 🛣️](#3d-lane-detection-%EF%B8%8F)
  - [Traffic Element Recognition 🚥](#traffic-element-recognition-)
  - [Topology Recognition 🕸️](#topology-recognition-%EF%B8%8F)
  - [SD Map as Prior 🧭](#sd-map-as-prior-)
  - [Unifying Map Elements 🗺️](#unifying-map-elements-%EF%B8%8F)
- [Data](#data)
- [Devkit](#devkit)
- [Get Started](#get-started)
- [Train a Model](#train-a-model)
- [Citation](#citation)
- [License](#license)

## News
- [2023/07]
  * Dataset `v1.1`: The SD Map as Prior Expansion and Unifying Map Elements Expansion released.
  * The test server is re-opened.
- [2023/06]
  * The Challenge at the [CVPR 2023 Workshop](https://opendrivelab.com/AD23Challenge.html) wraps up. ~~The test server will be re-opened soon. Please stay tuned!~~
- [2023/04]
  * A strong baseline based on [InternImage](https://github.com/OpenGVLab/InternImage) released. Check out [here](https://github.com/OpenGVLab/InternImage/tree/master/autonomous_driving/openlane-v2).
  * [OpenLane-V2 paper](https://arxiv.org/abs/2304.10440) is available on arXiv.
  * A stronger baseline released. Check out [here](https://github.com/OpenDriveLab/OpenLane-V2/blob/master/plugin/mmdet3d/configs/baseline_large.py).
- ~~[2023/03]~~
  *  ~~We are hosting a Challenge at the [CVPR 2023 Workshop](https://opendrivelab.com/AD23Challenge.html).~~
- [2023/02]
  * Dataset `v1.0`: Data of `subset_A` released.
  * Baseline model released.
- [2023/01]
  * Dataset `v0.1`: Initial OpenLane-V2 dataset sample released.

<p align="right">(<a href="#top">back to top</a>)</p>

## Leaderboard

### OpenLane Topology
We maintain a [leaderboard](https://opendrivelab.com/AD23Challenge.html#openlane_topology) and [test server](https://eval.ai/web/challenges/challenge-page/1925/overview) on the task of scene structure perception and reasoning. If you wish to add new / modify results to the leaderboard, please drop us an email following the instruction [here](https://eval.ai/web/challenges/challenge-page/1925/submission).

#### Autonomous Driving Challenge at CVPR 2023
![image](https://github.com/OpenDriveLab/OpenLane-V2/assets/29263416/4c1d7dc5-ce00-40de-8907-71060b6ca2f9)

<p align="right">(<a href="#top">back to top</a>)</p>

## Highlight - why we are exclusive?

### The world is three-dimensional - Introducing 3D lane
Previous datasets annotate lanes on images in the perspective view. Such a type of 2D annotation is insufficient to fulfill real-world requirements.
Following the [OpenLane](https://github.com/OpenDriveLab/OpenLane) dataset, we annotate **lanes in 3D space** to reflect their properties in the real world.

### Be aware of traffic signals - Recognizing Extremely Small road elements
Not only preventing collision but also facilitating efficiency is essential. 
Vehicles follow predefined traffic rules for self-disciplining and cooperating with others to ensure a safe and efficient traffic system.
**Traffic elements** on the roads, such as traffic lights and road signs, provide practical and real-time information.

### Beyond perception - Topology Reasoning between lane and road elements 
A traffic element is only valid for its corresponding lanes. 
Following the wrong signals would be catastrophic. 
Also, lanes have their predecessors and successors to build the map. 
Autonomous vehicles are required to **reason** about the **topology relationships** to drive in the right way.
In this dataset, we hope to shed light on the task of **scene structure perception and reasoning**.

### Data scale and diversity matters - building on Top of Awesome Benchmarks
Experience from the sunny day does not apply to the dancing snowflakes.
For machine learning, data is the must-have food.
We provide annotations on data collected in various cities, from Austin to Singapore and from Boston to Miami.
The **diversity** of data enables models to generalize in different atmospheres and landscapes.

<p align="right">(<a href="#top">back to top</a>)</p>

## Task

### 3D Lane Detection 🛣️
The [OpenLane](https://github.com/OpenDriveLab/OpenLane) dataset, which is the first real-world and the largest scaled 3D lane dataset to date, provides lane line annotations in 3D space.
Similarly, we annotate 3D lane centerlines and include the F-Score for evaluating predicted results  of undirected lane centerlines.
Furthermore, we define the subtask of 3D lane detection as detecting directed 3D lane centerlines from the given multi-view images covering the whole horizontal FOV.

<p align="center">
  <img src="https://github.com/OpenDriveLab/OpenLane-V2/assets/29263416/16f9264e-1693-469d-880e-876449788cb4" width="696px" >
</p>

### Traffic Element Recognition 🚥
Traffic elements and their attribute provide crucial information for autonomous vehicles.
The attribute represents the semantic meaning of a traffic element, such as the red color of a traffic light. 
In this subtask, on the given image in the front view, the location of traffic elements (traffic lights and road signs) and their attributes are demanded to be perceived simultaneously.
Compared to typical 2D detection datasets, the challenge is that the size of traffic elements is tiny due to the large scale of outdoor environments.

<p align="center">
  <img src="https://github.com/OpenDriveLab/OpenLane-V2/assets/29263416/bc35d569-7df0-4499-a98e-3b43a67aff1d" width="696px" >
</p>

### Topology Recognition 🕸️
Given multi-view images, the model learns to recognize the topology relationships among lane centerlines and between lane centerlines and traffic elements.
The most similar task is link prediction in the field of graph, in which the vertices are given and only edges are predicted by models.
In our case, both vertices and edges are unknown for the model.
Thus, lane centerlines and traffic elements are needed to be detected first, and then the topology relationships are built.

<p align="center">
  <img src="https://github.com/OpenDriveLab/OpenLane-V2/assets/29263416/c7c1fc1e-ea26-4a71-b3d2-8baaa3afb08c" width="696px" >
</p>

### SD Map as Prior 🧭
The standard-definition map (SD map) comprises road-level topology information and is commonly utilized for routing and navigation.
In the SD Map as Prior Expansion, SD maps serve as extra sensor inputs to offer preliminary knowledge.

<p align="center">
  <img src="https://github.com/OpenDriveLab/OpenLane-V2/assets/29263416/38e25241-b831-4002-9791-e92d115c1c3f" width="696px" >
</p>

### Unifying Map Elements 🗺️
Except for the centerline, a lane segment includes lanelines that define the boundaries of a lane and incorporate line types for particular purposes such as lane switching.
Road boundaries and pedestrian crossing are represented as special areas which contribute to regulating the behaviors of vehicles.
The Unifying Map Elements Expansion preserves the essence of the standard version of OpenLane-V2 while supplementing with additional elements to provide unified representations of the static driving scenes.

<p align="center">
  <img src="https://github.com/OpenDriveLab/OpenLane-V2/assets/29263416/64465460-265c-4df0-a7b2-59774761e03c" width="696px" >
</p>

<p align="right">(<a href="#top">back to top</a>)</p>

## Data
The dataset is divided into two subsets. 
**The `subset_A` serves as the primary subset and is utilized for the coming challenges and leaderboard, in which no external data, including the other subset, is allowed**.
The `subset_B` can be used to test the generalization ability of the model.
For more details, please refer to the corresponding pages: [use of data](./data/README.md), [notes of annotation](./docs/annotation.md), and [dataset statistics](./docs/statistics.md).

[Download](./data/README.md#download) now to discover our dataset!

<p align="right">(<a href="#top">back to top</a>)</p>

## Devkit
We provide a devkit for easy access to the OpenLane-V2 dataset.
After installing the package, the use of the dataset, such as loading images, loading meta data, and evaluating results, can be accessed through the API of `openlanv2`.
For more details on the API, please refer to [devkit](./docs/devkit.md).

<p align="right">(<a href="#top">back to top</a>)</p>


## Get Started
Please follow the steps below to get familiar with the OpenLane-V2 dataset.

1. Run the following commands to install the environment for setting up the dataset:

    ```sh
    git clone https://github.com/OpenDriveLab/OpenLane-V2.git
    cd OpenLane-V2
    conda create -n openlanev2 python=3.8 -y
    conda activate openlanev2
    pip install -r requirements.txt
    python setup.py develop
    ```

2. Use [links](./data/README.md#download) to download data manually from 

    - <img src="https://user-images.githubusercontent.com/29263416/222076048-21501bac-71df-40fa-8671-2b5f8013d2cd.png" alt="OpenDataLab" width="18"/> OpenDataLab,
    - <img src="https://user-images.githubusercontent.com/29263416/236970575-125919cc-1a36-4968-95e7-f5a17f896f9f.png" alt="Google Drive" width="18"/> Google Drive,
    - <img src="https://user-images.githubusercontent.com/29263416/236970717-fe619dd6-7e36-446b-88bf-30ff91028d87.png" alt="Baidu Yun" width="18"/> Baidu Yun.

    Then put them into the `data/OpenLane-V2/` folder and unzip them. 
    The resulting folder hierarchy is described [here](./data/README.md#hierarchy).
    Or use the following commands to download example data for a quick glance at the dataset:

    ```sh
    cd data/OpenLane-V2
    wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1Ni-L6u1MGKJRAfUXm39PdBIxdk_ntdc6' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1Ni-L6u1MGKJRAfUXm39PdBIxdk_ntdc6" -O OpenLane-V2_sample.tar
    md5sum -c openlanev2.md5
    tar -xvf *.tar
    cd ../..
    ```

3. Run the [tutorial](./tutorial.ipynb) on jupyter notebook to get familiar with the dataset and devkit.

<p align="right">(<a href="#top">back to top</a>)</p>


## Train a Model
Plug-ins to prevail deep learning frameworks for training models are provided to start training models on the OpenLane-V2 dataset.
We appreciate your valuable feedback and contributions to plug-ins on different frameworks.

### mmdet3d

The [plug-in](./plugin/mmdet3d/) to MMDetection3d is built on top of [mmdet3d v1.0.0rc6](https://github.com/open-mmlab/mmdetection3d/tree/v1.0.0rc6) and tested under:
- Python 3.8.15
- PyTorch 1.9.1
- CUDA 11.1
- GCC 5.4.0
- mmcv-full==1.5.2
- mmdet==2.26.0
- mmsegmentation==0.29.1

Please follow the [instruction](https://github.com/open-mmlab/mmdetection3d/blob/v1.0.0rc6/docs/en/getting_started.md) to install mmdet3d.
Assuming OpenLane-V2 is installed under `OpenLane-V2/` and mmdet3d is built under `mmdetection3d/`, create a soft link to the plug-in file:
```
└── mmdetection3d
    └── projects
        ├── example_project
        └── openlanev2 -> OpenLane-V2/plugin/mmdet3d
```
Then you can train or evaluate a model using the config `mmdetection3d/projects/openlanev2/configs/baseline.py`, whose path is replaced accordingly.
Options can be passed to enable supported functions during evaluation (`--eval *`), such as `--eval-options dump=True dump_dir=/PATH/TO/DUMP` to save pickle file for submission and `--eval-options visualization=True visualization_dir=/PATH/TO/VIS` for visualization.


<p align="right">(<a href="#top">back to top</a>)</p>


## Citation
Please use the following citation when referencing OpenLane-V2:

```bibtex
@article{wang2023openlanev2,
  title={OpenLane-V2: A Topology Reasoning Benchmark for Scene Understanding in Autonomous Driving}, 
  author={Wang, Huijie and Li, Tianyu and Li, Yang and Chen, Li and Sima, Chonghao and Liu, Zhenbo and Wang, Yuting and Jiang, Shengyin and Jia, Peijin and Wang, Bangjun and Wen, Feng and Xu, Hang and Luo, Ping and Yan, Junchi and Zhang, Wei and Li, Hongyang},
  journal={arXiv preprint arXiv:2304.10440},
  year={2023}
}
```


<p align="right">(<a href="#top">back to top</a>)</p>

## License
Our dataset is built on top of the [nuScenes](https://www.nuscenes.org/nuscenes) and [Argoverse 2](https://www.argoverse.org/av2.html) datasets.
Before using the OpenLane-V2 dataset, you should agree to the terms of use of the [nuScenes](https://www.nuscenes.org/nuscenes) and [Argoverse 2](https://www.argoverse.org/av2.html) datasets respectively.
All code within this repository is under [Apache License 2.0](./LICENSE).

<p align="right">(<a href="#top">back to top</a>)</p>
