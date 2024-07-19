<div id="top" align="center">

# OpenLane-V2
**The World's First Perception and Reasoning Benchmark for Scene Structure in Autonomous Driving.**

[![OpenLane-V2](https://img.shields.io/badge/OpenLane--V2-v2.0-blueviolet)](/data)
[![devkit](https://img.shields.io/badge/devkit-v2.1.0-blueviolet)](/docs/getting_started.md)
[![LICENSE](https://img.shields.io/badge/license-Apache%202.0-blue)](#license--citation)
[![testserver](https://img.shields.io/badge/Test%20Server-%F0%9F%A4%97-ffc107)](https://huggingface.co/spaces/AGC2024/mapless-driving-2024)

<!-- **English | [中文](./README-zh-hans.md)**

_In terms of ambiguity, the English version shall prevail._ -->

</div>

> - [Paper](https://proceedings.neurips.cc/paper_files/paper/2023/hash/3c0a4c8c236144f1b99b7e1531debe9c-Abstract-Datasets_and_Benchmarks.html) (Accepted at NeurIPS 2023 Track Datasets and Benchmarks)
> - [CVPR 2023 Autonomous Driving Challenge - OpenLane Topology Track](https://opendrivelab.com/challenge2023/#openlane_topology)
> - [CVPR 2024 Autonomous Grand Challenge - Mapless Driving Track](https://opendrivelab.com/challenge2024/#mapless_driving)
> - Point of contact: [Huijie (王晖杰)](mailto:wanghuijie@pjlab.org.cn) or [Tianyu (李天羽)](mailto:litianyu@pjlab.org.cn)

## Leaderboard

### Mapless Driving at CVPR 2024 AGC (Server remains `active`)
We maintain a [leaderboard](https://opendrivelab.com/challenge2024/#mapless_driving) and [test server](https://huggingface.co/spaces/AGC2024/mapless-driving-2024) on the task of **Driving Scene Topology**. If you wish to add new / modify results to the leaderboard, please drop us an email.

- [Challenge 2024](https://opendrivelab.com/challenge2024/#mapless_driving)

![image](https://github.com/user-attachments/assets/2ef60d09-c875-4891-abbc-c2400ab0a283)


### OpenLane Topology Challenge at CVPR 2023 (Server remains `active`)
We maintain a [leaderboard](https://opendrivelab.com/challenge2023/#openlane_topology) and [test server](https://eval.ai/web/challenges/challenge-page/1925/overview) on the task of **OpenLane Topology**. If you wish to add new / modify results to the leaderboard, please drop us an email following the instructions [here](https://eval.ai/web/challenges/challenge-page/1925/submission).

- [Challenge 2023](https://opendrivelab.com/challenge2023/#openlane_topology)

![image](https://github.com/OpenDriveLab/OpenLane-V2/assets/29263416/4c1d7dc5-ce00-40de-8907-71060b6ca2f9)


## Table of Contents
- [News](#news)
- [Introducing `OpenLane-V2 Update`](#introducing-openlane-v2-update)
- [Task and Evaluation](#task-and-evaluation)
- [Highlights](#highlights-of-openlane-v2)
- [Getting Started](#getting-started)
- [License & Citation](#license--citation)
- [Related Resources](#related-resources)


## News

> Note
> 
> The difference between `v1.x` and `v2.x` is that we updated APIs and materials on lane segment and SD map in `v2.x`.
>
> ❗️Update on **evaluation metrics** led to differences in TOP scores between `vx.1` ([`v1.1`](https://github.com/OpenDriveLab/OpenLane-V2/releases/tag/v1.1.0), [`v2.1`](https://github.com/OpenDriveLab/OpenLane-V2/releases/tag/v2.1.0)) and `vx.0` (`v1.0`, `v2.0`).
> We encourage the use of **`vx.1`** metrics.
> For more details please see issue [#76](https://github.com/OpenDriveLab/OpenLane-V2/issues/76).

- **`2024/06/01`** The [Autonomous Grand Challenge](https://opendrivelab.com/challenge2024/#mapless_driving) wraps up.
- **`2024/03/01`** We are hosting **CVPR 2024 Autonomous Grand Challenge**.
- **`2023/11/01`** Devkit `v2.1.0` and `v1.1.0` released.
- **`2023/08/28`** Dataset `subset_B` released.
- **`2023/07/21`** Dataset `v2.0` and Devkit `v2.0.0` released.
- **`2023/07/05`** The [test server of OpenLane Topology](https://eval.ai/web/challenges/challenge-page/1925/overview) is re-opened.
- **`2023/06/01`** The [Challenge at the CVPR 2023 Workshop](https://opendrivelab.com/challenge2023/#openlane_topology) wraps up.
- **`2023/04/21`** A baseline based on [InternImage](https://github.com/OpenGVLab/InternImage) released. Check out [here](https://github.com/OpenGVLab/InternImage/tree/master/autonomous_driving/openlane-v2).
- **`2023/04/20`** [OpenLane-V2 paper](https://arxiv.org/abs/2304.10440) is available on arXiv.
- **`2023/02/15`** Dataset `v1.0`, Devkit `v1.0.0`, and baseline model released.
- **`2023/01/15`** Initial OpenLane-V2 dataset sample `v0.1` released.

<p align="right">(<a href="#top">back to top</a>)</p>

## Introducing `OpenLane-V2 Update`

We are happy to announce an important update to the OpenLane family, featuring two sets of additional data and annotations.

- **`Map Element Bucket`.** We provide a diverse span of road elements (as a `bucket`) to build the driving scene - on par with all elements in HD Map. Armed with the newly introduced [**lane segment**](/docs/features.md#map-element-bucket) representations, we unify various map elements to incorporate comprehensive aspects of the captured static scenes to empower [DriveAGI](https://github.com/OpenDriveLab/DriveAGI).  
:bell: The proposed **lane segment** representation is published with [**LaneSegNet**](https://github.com/OpenDriveLab/LaneSegNet) in ICLR 2024!

<p align="center">
  <img src="https://github.com/OpenDriveLab/OpenLane-V2/assets/29263416/77846f69-fe77-45aa-b769-e85fd98a0596" width="696px">
</p>

-  **`Standard-definition (SD) Map`.** As a new sensor input, [**SD Map**](/docs/features.md#sd-map) supplements multi-view images with topological and positional priors to strengthen structural acknowledge in the neural networks.

<p align="center">
  <img src="https://github.com/OpenDriveLab/OpenLane-V2/assets/29263416/0b3f4678-fa57-4187-afd6-e55db12a76a6" width="696px">
</p>

<p align="right">(<a href="#top">back to top</a>)</p>

## Task and Evaluation

### Driving Scene Topology

Given sensor inputs, lane segments are required to be perceived, instead of lane centerlines in the task of OpenLane Topology.
Besides, pedestrian crossings and road boundaries are also desired to build a comprehensive understanding of the driving scenes.
The [OpenLane-V2 UniScore (OLUS)](docs/metrics.md#driving-scene-topology) is utilized  to summarize model performance in all aspects.

### OpenLane Topology
Given sensor inputs, participants are required to deliver not only perception results of lanes and traffic elements but also topology relationships among lanes and between lanes and traffic elements simultaneously.
In this task, we use [OpenLane-V2 Score (OLS)](docs/metrics.md#openlane-topology) to evaluate model performance.

<p align="right">(<a href="#top">back to top</a>)</p>


## Highlights of OpenLane-V2

### Unifying Map Representations

One of the superior formulations in the bucket is [**Lane Segment**](/docs/features.md#map-element-bucket). It serves as a unifying and versatile representation of lanes, paving the way for multiple downstream applications. With the introduction of [**SD Map**](/docs/features.md#sd-map), the autonomous driving system is capable of utilizing these informative priors for achieving satisfactory performance in perception and reasoning.

The following table sums up a detailed comparison of different `lane formulations` to achieve various functionalities.

<table>
  <tr align="center">
    <td rowspan="2">Lane Formulation</td>
    <td colspan="8">Functionality</td>
  </tr>
  <tr align="center">
    <td>3D Space</td>
    <td>Laneline Cateogry</td>
    <td>Lane Direction</td>
    <td>Drivable Area</td>
    <td>Lane-level Drivable Area</td>
    <td>Lane-lane Topology</td>
    <td>Bind to Traffic Element</td>
    <td>Laneline-less</td>
  </tr>
  <tr align="center">
    <td>2D Laneline</td>
    <td></td>
    <td>✅</td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
  </tr>
  <tr align="center">
    <td>3D Laneline</td>
    <td>✅</td>
    <td>✅</td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
  </tr>
  <tr align="center">
    <td>Online (pseudo) HD Map</td>
    <td>✅</td>
    <td></td>
    <td></td>
    <td>✅</td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
  </tr>
  <tr align="center">
    <td>Lane Centerline</td>
    <td>✅</td>
    <td></td>
    <td>✅</td>
    <td></td>
    <td></td>
    <td>✅</td>
    <td>✅</td>
    <td>✅</td>
  </tr>
  <tr align="center">
    <td><b>Lane Segment</b> (newly released)</td>
    <td>✅</td>
    <td>✅</td>
    <td>✅</td>
    <td>✅</td>
    <td>✅</td>
    <td>✅</td>
    <td>✅</td>
    <td>✅</td>
  </tr>
</table>

> - 3D Space: whether the perceived entities are represented in the 3D space.
> - Laneline Category: categories of the visible laneline, such as solid and dash.
> - Lane Direction: the driving direction that vehicles need to follow in a particular lane.
> - Drivable Area: the entire area where vehicles are allowed to drive.
> - Lane-level Drivable Area: drivable area of a single lane, which restricts vehicles from trespassing neighboring lanes.
> - Lane-lane Topology: connectivity of lanes that builds the lane network to provide routing information.
> - Bind to Traffic Element: correspondence to traffic elements, which provide regulations according to traffic rules.
> - Laneline-less: the ability to provide guidance in areas where no visible laneline is available, such as intersections.


### Introducing 3D Laneline 
Previous datasets annotate lanes on images in the perspective view. Such a type of 2D annotation is insufficient to fulfill real-world requirements.
Following the [OpenLane-V1](https://github.com/OpenDriveLab/OpenLane) practice, we annotate [**lanes in 3D space**](/docs/features.md#3d-lane-detection) to reflect the geometric properties in the real 3D world.

### Recognizing Extremely Small Traffic Elements
Not only preventing collision but also facilitating efficiency is essential. 
Vehicles follow predefined traffic rules for self-disciplining and cooperating with others to ensure a safe and efficient traffic system.
[**Traffic elements**](/docs/features.md#traffic-element-recognition) on the roads, such as traffic lights and road signs, provide practical and real-time information.

### Topology Reasoning between Lane and Road Elements 
A traffic element is only valid for its corresponding lanes. 
Following the wrong signals would be catastrophic. 
Also, lanes have their predecessors and successors to build the map. 
Autonomous vehicles are required to **reason** about the [**topology relationships**](/docs/features.md#topology-recognition) to drive in the right way.

<!--
### Data scale and diversity matters - building on top of renowned Benchmarks
Experience from the sunny day does not apply to the dancing snowflakes.
For machine learning, data is the must-have food.
We provide annotations on data collected in various cities, from Austin to Singapore and from Boston to Miami.
The **diversity** of data enables models to generalize in different atmospheres and landscapes.
-->

<p align="right">(<a href="#top">back to top</a>)</p>


## Getting Started
- [Download Data](/docs/getting_started.md#download-data)
- [Install Devkit](/docs/getting_started.md#install-devkit)
- [Prepare Dataset](/docs/getting_started.md#prepare-dataset)
- [Train a Model](/docs/getting_started.md#train-a-model)

<p align="right">(<a href="#top">back to top</a>)</p>


## License & Citation

> Prior to using the OpenLane-V2 dataset, you should agree to the terms of use of the [nuScenes](https://www.nuscenes.org/nuscenes) and [Argoverse 2](https://www.argoverse.org/av2.html) datasets respectively.
> OpenLane-V2 is distributed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0) license.
> All code within this repository is under [Apache License 2.0](./LICENSE).

Please use the following citation when referencing OpenLane-V2:

```bibtex
@inproceedings{wang2023openlanev2,
  title={OpenLane-V2: A Topology Reasoning Benchmark for Unified 3D HD Mapping}, 
  author={Wang, Huijie and Li, Tianyu and Li, Yang and Chen, Li and Sima, Chonghao and Liu, Zhenbo and Wang, Bangjun and Jia, Peijin and Wang, Yuting and Jiang, Shengyin and Wen, Feng and Xu, Hang and Luo, Ping and Yan, Junchi and Zhang, Wei and Li, Hongyang},
  booktitle={NeurIPS},
  year={2023}
}

@article{li2023toponet,
  title={Graph-based Topology Reasoning for Driving Scenes},
  author={Li, Tianyu and Chen, Li and Wang, Huijie and Li, Yang and Yang, Jiazhi and Geng, Xiangwei and Jiang, Shengyin and Wang, Yuting and Xu, Hang and Xu, Chunjing and Yan, Junchi and Luo, Ping and Li, Hongyang},
  journal={arXiv preprint arXiv:2304.05277},
  year={2023}
}

@inproceedings{li2023lanesegnet,
  title={LaneSegNet: Map Learning with Lane Segment Perception for Autonomous Driving},
  author={Li, Tianyu and Jia, Peijin and Wang, Bangjun and Chen, Li and Jiang, Kun and Yan, Junchi and Li, Hongyang},
  booktitle={ICLR},
  year={2024}
}
```

<p align="right">(<a href="#top">back to top</a>)</p>


## Related Resources
[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

- [DriveAGI](https://github.com/OpenDriveLab/DriveAGI) | [DriveLM](https://github.com/OpenDriveLab/DriveLM) | [OpenScene](https://github.com/OpenDriveLab/OpenScene)
- [TopoNet](https://github.com/OpenDriveLab/TopoNet) | [LaneSegNet](https://github.com/OpenDriveLab/LaneSegNet)
- [PersFormer](https://github.com/OpenDriveLab/PersFormer_3DLane) | [OpenLane](https://github.com/OpenDriveLab/OpenLane)
- [BEV Perception Survey & Recipe](https://github.com/OpenDriveLab/BEVPerception-Survey-Recipe) | [BEVFormer](https://github.com/fundamentalvision/BEVFormer)

<p align="right">(<a href="#top">back to top</a>)</p>
