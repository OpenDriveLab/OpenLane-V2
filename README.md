<div id="top" align="center">

# OpenLane-V2
**The world's First Perception and Reasoning Benchmark for Scene Structure in Autonomous Driving.**

<a href="#data">
  <img alt="OpenLane-v2: v0.1" src="https://img.shields.io/badge/OpenLane--V2-v0.1-blueviolet"/>
</a>
<a href="#devkit">
  <img alt="devkit: v0.1.0" src="https://img.shields.io/badge/devkit-v0.1.0-blueviolet"/>
</a>
<a href="#license">
  <img alt="License: Apache2.0" src="https://img.shields.io/badge/license-Apache%202.0-blue.svg"/>
</a>

**[English](./README.md) | [中文](./README-zh-hans.md)**


<img src="./imgs/poster.gif" width="696px">

</div>

## Table of Contents
- [Highlight](#highlight---why-we-are-exclusive)
- [Task](#task)
  - [3D Lane Detection 🛣️](#3d-lane-detection-%EF%B8%8F)
  - [Traffic Element Recognition 🚥](#traffic-element-recognition-)
  - [Topology Recognition 🕸️](#topology-recognition-%EF%B8%8F)
- [News](#news)
- [Data](#data)
- [Devkit](#devkit)
- [Get Started](#get-started)
- [Benchmark and Leaderboard](#benchmark-and-leaderboard-to-be-released)
- [Citation](#citation)
- [License](#license)

## Highlight - why we are exclusive?

### $\color{Magenta}\fcolorbox{white}{white}{The world is three-dimensional - Introducing 3D laneline}$ 
Previous datasets annotate lanes on images in the perspective view. Such a type of 2D annotation is insufficient to fulfill real-world requirements.
Following the [OpenLane](https://github.com/OpenPerceptionX/OpenLane) dataset, we annotate $\color{blue}\fcolorbox{white}{white}{lanes in 3D space}$ to reflect their properties in the real world.

### $\color{Magenta}\fcolorbox{white}{white}{Be aware of traffic signals - Recognizing Extremely Small road elements}$ 
Not only preventing collision but also facilitating efficiency is essential. 
Vehicles follow predefined traffic rules for self-disciplining and cooperating with others to ensure a safe and efficient traffic system.
$\color{blue}\fcolorbox{white}{white}{Traffic elements}$ on the roads, such as traffic lights and road signs, provide practical and real-time information.

### $\color{Magenta}\fcolorbox{white}{white}{Beyond perception - Topology Reasoning between lane and road elements}$ 
A traffic element is only valid for its corresponding lanes. 
Following the wrong signals would be catastrophic. 
Also, lanes have their predecessors and successors to build the map. 
Autonomous vehicles are required to $\color{blue}\fcolorbox{white}{white}{reason}$ about the $\color{blue}\fcolorbox{white}{white}{topology relationships}$ to drive in the right way.
In this dataset, we hope to shed light on the task of $\color{blue}\fcolorbox{white}{white}{scene structure perception and reasoning}$.

### $\color{Magenta}\fcolorbox{white}{white}{Data scale and diversity matters - building on Top of Awesome Benchmarks}$
Experience from the sunny day does not apply to the dancing snowflakes.
For machine learning, data is the must-have food.
We provide annotations on data collected in various cities, from Austin to Singapore and from Boston to Miami.
The $\color{blue}\fcolorbox{white}{white}{diversity}$ of data enables models to generalize in different atmospheres and landscapes.

<p align="right">(<a href="#top">back to top</a>)</p>

## Task
The primary task of the dataset is **scene structure perception and reasoning**, which requires the model to recognize the dynamic drivable states of lanes in the surrounding environment. 
The challenge of this dataset includes not only detecting lane centerlines and traffic elements but also recognizing the attribute of traffic elements and topology relationships on detected objects.
We define the **[OpenLane-V2 Score (OLS)](./docs/metrics.md#openlane-v2-score)**, which is the average of various metrics covering different aspects of the primary task:

$$
OLS = average(mAP_{LC} + mAP_{TE} + mAP_{LCLC} + mAP_{LCTE}).
$$

The metrics of different subtasks are described below.

### 3D Lane Detection 🛣️
The [OpenLane](https://github.com/OpenPerceptionX/OpenLane) dataset, which is the first real-world and the largest scaled 3D lane dataset to date, provides lane line annotations in 3D space.
Similarly, we annotate 3D lane centerlines and include the F-Score for evaluating predicted results  of undirected lane centerlines.
Furthermore, we define the subtask of 3D lane detection as detecting directed 3D lane centerlines from the given multi-view images covering the whole horizontal FOV.
The instance-level evaluation metric of average precision $mAP_{LC}$ is utilized to measure the detection performance on lane centerlines.

<p align="center">
  <img src="./imgs/lane.gif" width="696px" >
</p>

### Traffic Element Recognition 🚥
Existing datasets pay little attention to the detection of traffic elements and their attribute, which provide crucial information for autonomous vehicles.
The attribute represents the semantic meaning of a traffic element, such as the red color of a traffic light. 
In this subtask, on the given image in the front view, the location of traffic elements (traffic lights and road signs) and their attributes are demanded to be perceived simultaneously.
Compared to typical 2D detection datasets, the challenge is that the size of traffic elements is tiny due to the large scale of outdoor environments.
Similar to the typical 2D detection task, the metric of $mAP_{TE}$ is utilized to measure the performance of traffic elements (TE) detection averaged over different attributes.

<p align="center">
  <img src="./imgs/traffic_element.gif" width="696px" >
</p>

### Topology Recognition 🕸️
We first define the task of recognizing topology relationships in the field of autonomous driving.
Given multi-view images, the model learns to recognize the topology relationships among lane centerlines and between lane centerlines and traffic elements.
The most similar task is link prediction in the field of graph, in which the vertices are given and only edges are predicted by models.
In our case, both vertices and edges are unknown for the model.
Thus, lane centerlines and traffic elements are needed to be detected first, and then the topology relationships are built.
Adapted from the task of link prediction, $mAP_{LCLC}$ is used for topology among lane centerlines (LCLC), and $mAP_{LCTE}$ for topology between lane centerlines and traffic elements (LCTE).

<p align="center">
  <img src="./imgs/topology.gif" width="696px" >
</p>

<p align="right">(<a href="#top">back to top</a>)</p>

## News
- [2023/01]
  * Dataset `v0.1`: Initial OpenLane-V2 dataset sample released.
  * Devkit `v0.1.0`: Initial OpenLane-V2 devkit released.

<p align="right">(<a href="#top">back to top</a>)</p>

## Data
The OpenLane-V2 dataset is a large-scale dataset for scene structure perception and reasoning in the field of autonomous driving. 
Following [OpenLane](https://github.com/OpenPerceptionX/OpenLane), the first 3D lane dataset, we provide lane annotations in 3D space.
The difference is that instead of lane lines, we annotate lane centerlines, which can be served as the trajectory for autonomous vehicles.
Besides, we provide annotations on traffic elements (traffic lights and road signs) and their attribute, and the topology relationships among lane centerlines and between lane centerlines and traffic elements.

The dataset is divided into two subsets. 
**The `subset_A` serves as the primary subset and is utilized for the coming challenges and leaderboard, in which no external data, including the other subset, is allowed**.
The `subset_B` can be used to test the generalization ability of the model.
For more details, please refer to the corresponding pages: [use of data](./data/README.md), [notes of annotation](./docs/annotation.md), and [dataset statistics](./docs/statistics.md).

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
python setup.py install
```

2. Use [links](./data/README.md#download) to download data manually from <img src="https://ssl.gstatic.com/docs/doclist/images/drive_2022q3_32dp.png" alt="Google Drive" width="18"/> or <img src="https://nd-static.bdstatic.com/m-static/v20-main/favicon-main.ico" alt="Baidu Yun" width="18"/>. 
Then put them into the `data/OpenLane-V2/` folder and unzip them. 
The resulting folder hierarchy is described [here](./data/README.md#hierarchy).
Alternatively, use the following commands:

```sh
cd data/OpenLane-V2
wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1TjcGaHSd1tTMl0rsaxdP_GWnKf2CiDIx' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1TjcGaHSd1tTMl0rsaxdP_GWnKf2CiDIx" -O OpenLane-V2-subset-A-example.tar
md5sum -c openlanev2.md5
tar -xvf *.tar
cd ../..
```

3. Run the [tutorial](./tutorial.ipynb) on jupyter notebook to get familiar with the dataset and devkit.

<p align="right">(<a href="#top">back to top</a>)</p>

## Benchmark and Leaderboard (To be released)
We will provide an initial benchmark on the OpenLane-V2 dataset, and you are welcome to add your work here!
Please stay tuned for the release of the benchmark.

| Method | OLS (main metric) | $mAP_{LC}$ | $mAP_{TE}$ | $mAP_{LCLC}$ | $mAP_{LCTE}$ | F-Score* |
| - | - | - | - | - | - | - |
| - | - | - | - | - | - | - |

<sub>* F-Score is not taken into consideration in both the challenge and leaderboard.</sub>

<p align="right">(<a href="#top">back to top</a>)</p>

## Citation
OpenLane-V2 is a joint work from [OpenDriveLab team](http://opendrivelab.com/) at Shanghai AI Lab with [Noah's Ark Lab](http://dev3.noahlab.com.hk/) at Huawei. Please use the following citation when referencing OpenLane-V2:

```bibtex
@misc{ openlanev2_dataset,
  author = {{OpenLane-V2 Dataset Contributors}},
  title = {{OpenLane-V2: The world's First Perception and Reasoning Benchmark for Scene Structure in Autonomous Driving}},
  url = {https://github.com/OpenDriveLab/OpenLane-V2},
  license = {Apache-2.0},
  year = {2023}
}
```

Our dataset is built on top of the [nuScenes](https://www.nuscenes.org/nuscenes) and [Argoverse 2](https://www.argoverse.org/av2.html) datasets. Please also cite:

```bibtex
@article{ nuscenes2019,
  author = {Holger Caesar and Varun Bankiti and Alex H. Lang and Sourabh Vora and Venice Erin Liong and Qiang Xu and Anush Krishnan and Yu Pan and Giancarlo Baldan and Oscar Beijbom},
  title = {nuScenes: A multimodal dataset for autonomous driving},
  journal = {arXiv preprint arXiv:1903.11027},
  year = {2019}
}

@INPROCEEDINGS { Argoverse2,
  author = {Benjamin Wilson and William Qi and Tanmay Agarwal and John Lambert and Jagjeet Singh and Siddhesh Khandelwal and Bowen Pan and Ratnesh Kumar and Andrew Hartnett and Jhony Kaesemodel Pontes and Deva Ramanan and Peter Carr and James Hays},
  title = {Argoverse 2: Next Generation Datasets for Self-driving Perception and Forecasting},
  booktitle = {Proceedings of the Neural Information Processing Systems Track on Datasets and Benchmarks (NeurIPS Datasets and Benchmarks 2021)},
  year = {2021}
}
```

<p align="right">(<a href="#top">back to top</a>)</p>

## License
Before using the OpenLane-V2 dataset, you should register on the website and agree to the terms of use of the [nuScenes](https://www.nuscenes.org/nuscenes) and [Argoverse 2](https://www.argoverse.org/av2.html) datasets.
All code within this repository is under [Apache License 2.0](./LICENSE).

<p align="right">(<a href="#top">back to top</a>)</p>
