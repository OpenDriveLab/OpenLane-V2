<div id="top" align="center">

# OpenLane-V2
**全球首个自动驾驶道路结构感知和推理基准。**

<a href="#数据">
  <img alt="OpenLane-v2: v0.1" src="https://img.shields.io/badge/OpenLane--V2-v0.1-blueviolet"/>
</a>
<a href="#开发工具">
  <img alt="devkit: v0.1.0" src="https://img.shields.io/badge/devkit-v0.1.0-blueviolet"/>
</a>
<a href="#引用">
  <img alt="License: Apache2.0" src="https://img.shields.io/badge/license-Apache%202.0-blue.svg"/>
</a>
  
**[中文](./README-zh-hans.md) | [English](./README.md)**
  
  
<img src="./imgs/poster.gif" width="696px">

</div>


## 目录

- [摘要](#摘要)
- [任务](#任务)
  - [3D车道线检测🛣️](#3d车道线检测-%EF%B8%8F)
  - [交通标志检测🚥](#交通标志检测-)
  - [拓扑认知🕸️](#拓扑认知-%EF%B8%8F)
- [信息发布](#信息发布)
- [数据](#数据)
- [开发工具](#开发工具)
- [入门指南](#入门指南)
- [基准和排行榜](#基准和排行榜)
- [引用](#引用)
- [许可说明](#许可说明)

## 摘要
### $\color{Magenta}\fcolorbox{white}{white}{三维场景，3D车道}$
<!-- 针对自动驾驶场景，现有数据集一般都是在图像上标注车道线，但真实的行车场景是3D，2D车道线数据无法在一些特殊场景确保车辆自动行驶，如上下坡、路面不平整等场景。
[OpenLane](https://github.com/OpenPerceptionX/OpenLane) 是第一个真实场景3D车道线数据集，我们提供  $\color{blue}{3D车道中心线}$ 真值以反映它们在真实环境中的特性。 -->
道路环境需要怎样的建模才能满足车辆自动驾驶功能的需求？

以往的数据集一般都在2D图像上标注车道，但在实际应用中，由于缺乏高度信息，2D车道数据无法支持车辆在上下坡、路面不平整等场景行驶，因此3D车道数据是不可或缺的。

同我们之前的工作 [OpenLane](https://github.com/OpenDriveLab/OpenLane) 一致，OpenLane-V2提供三维车道标注。
### $\color{Magenta}\fcolorbox{white}{white}{关注交通标注，确保行车规范}$
在道路上平稳的行驶只是第一步，驾驶汽车还需要遵循环境中的 $\color{blue}{交通要素}$（交通灯，路标）信息指示，确保不违反当地交通法规，因此OpenLane-V2也提供了2D交通要素标注。

交通要素在2D图像上尺寸大多都较小，检测领域中小目标检测一直是个热点，这也是该基准的挑战之一。

### $\color{Magenta}\fcolorbox{white}{white}{拓扑关系支撑场景结构化}$ 
环境中交通元素应仅对其特定的车道有指示作用，遵循错误的信号将造成灾难性的后果，因此需要明确车道与交通元素的关系。环境中的车道也不应是割裂存在的，车道与车道的关系也同样重要。

OpenLane-V2提供车道与车道、车道与交通要素之间的拓扑关系，打造结构化场景。

自动驾驶汽车需要通过 $\color{blue}{推理}$ 捕捉正确的 $\color{blue}{拓扑关系}$ 以正确的方式行驶。
我们希望这个数据集的建立可以促进 $\color{blue}{道路场景感知和推理}$ 任务的发展。

### $\color{Magenta}\fcolorbox{white}{white}{多元大规模数据，搭建超赞数据集}$
对于机器学习任务，数据是必备的基石。
我们提供从奥斯汀到新加坡，从波士顿到迈阿密等各个城市收集的数据的标注，
支撑数据的 $\color{blue}{多元性}$。

<p align="right">(<a href="#top">回到顶部</a>)</p>


## 任务

数据集的首要任务是**场景结构感知和推理**，这需要模型能够识别周围环境中车道的可行驶状态。
该数据集的任务不仅包括车道中心线和交通元素检测，还包括检测到的对象的拓扑关系识别。
我们定义了[**OpenLane-V2 Score (OLS)**](./docs/metrics.md#openlane-v2-score)，该指标涵盖主要任务不同方面指标的平均值：

$$
OLS = average(mAP_{LC} + mAP_{TE} + mAP_{LCLC} + mAP_{LCTE}).
$$

子任务的指标如下所述：

### 3D车道线检测 🛣️

[OpenLane](https://github.com/OpenPerceptionX/OpenLane) 数据集是迄今为止第一个真实世界和规模最大的 3D 车道数据集，提供 3D 空间下的车道线标注。
在OpenLane基础上，我们将 3D 车道检测的任务定义如下：从覆盖整个水平 FOV(视场角-Field Of View) 的多视图中检测带方向的 3D 车道中心线。
用平均精度 $mAP_{LC}$ 指标评估车道中心线的检测性能。

<p align="center">
  <img src="./imgs/lane.gif" width="696px" >
</p>

### 交通标志检测 🚥

现有的数据集很少关注交通标志的检测及其语义，但是交通标志是自动驾驶汽车中关键信息。
该属性表示交通元素的语义，例如交通灯的红色。
在这个子任务中，在给定的前视图图像上，要求同时感知交通元素（交通灯和路标）的位置及其属性。
与典型的 2D 检测数据集相比，挑战在于由于室外环境的大规模，交通元素的尺寸很小。
与典型的 2D 检测任务类似，
$mAP_{TE}$ 的度量用于衡量在不同属性上平均的交通元素 (TE) 检测的性能。


<p align="center">
  <img src="./imgs/traffic_element.gif" width="696px" >
</p>


### 拓扑认知 🕸️
我们首先定义在自动驾驶领域识别拓扑关系的任务。
给定多视图图像，该模型学习识别车道中心线之间以及车道中心线与交通元素之间的拓扑关系。
最相似的任务是图领域的连通性预测，其中顶点是给定的，模型只预测边。
在我们的例子中，模型的顶点和边都是未知的。
因此，首先需要检测车道中心线和交通要素，然后建立拓扑关系。
参照连通性预测任务，
我们用 $mAP_{LCLC}$ 评估车道中心线（LCLC）之间的拓扑表现，
用 $mAP_{LCTE}$ 评估车道中心线和交通元素（LCTE）之间的拓扑表现。

<p align="center">
  <img src="./imgs/topology.gif" width="696px" >
</p>

<p align="right">(<a href="#top">回到顶部</a>)</p>




## 信息发布
- [2023/01]
  * 数据集 v0.1： OpenLane-V2 [数据集样本](data/OpenLane-V2/dataset-sample/)。
  * 开发工具 v0.1： OpenLane-V2 开发工具。

<p align="right">(<a href="#top">回到顶部</a>)</p>


## 数据

OpenLane-V2 数据集是自动驾驶领域用于道路结构感知和推理的大规模数据集。
与 [OpenLane](https://github.com/OpenPerceptionX/OpenLane)数据集一致，我们提供三维空间中的车道真值。与之有区别的是，OenLane-V2提供的是车道中心线的3D标注，而OpenLane提供的是车道分割线3D标注。此外，我们还提供了交通标志(交通灯和路标)及其属性的2D框标注，和车道中心线之间以及车道中心线与交通要素之间的拓扑关系标注。

数据集分为两个子集。
**`subset_A`作为主要子集，服务于即将到来的比赛和排行榜，比赛中不允许任何外部数据，包括本数据集其他子集**。
`subset_B`可以用来测试模型的泛化能力。
更多信息请参考对应的页面：[使用数据](./data/README.md)、[标注文档](./docs/annotation.md)与[数据统计](./docs/statistics.md).。

<p align="right">(<a href="#top">回到顶部</a>)</p>


## 开发工具

我们提供了一个开发工具来方便社区熟悉并使用 OpenLane-V2 数据集。
可以通过 `openlanv2` 的API实现数据集的使用，例如加载图像、加载元数据和评估结果。
更多开发工具信息请参考[开发工具](./docs/devkit.md)。

<p align="right">(<a href="#top">回到顶部</a>)</p>

## 入门指南

按照以下步骤熟悉 OpenLane-V2 数据集：

1. 运行以下命令安装必要的工具包，完成研究环境准备：

```sh
git clone https://github.com/OpenDriveLab/OpenLane-V2.git
cd OpenLane-V2
conda create -n openlanev2 python=3.8 -y
conda activate openlanev2
pip install -r requirements.txt
python setup.py install
```

2. 点击[链接](./data/README.md#download)从<img src="https://ssl.gstatic.com/docs/doclist/images/drive_2022q3_32dp.png" alt="Google Drive" width="18"/>或<img src="https://nd-static.bdstatic.com/m-static/v20-main/favicon-main.ico" alt="Baidu Yun" width="18"/>下载数据。
并将它们移动至 `data/OpenLane-V2/` 文件夹下解压。
生成的目录结构应[如下](./data/README.md#hierarchy)所示。
或者用这些命令来实现此步骤:

```sh
cd data/OpenLane-V2
wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1TjcGaHSd1tTMl0rsaxdP_GWnKf2CiDIx' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1TjcGaHSd1tTMl0rsaxdP_GWnKf2CiDIx" -O OpenLane-V2-subset-A-example.tar
md5sum -c openlanev2.md5
tar -xvf *.tar
cd ../..
```

3. 在 jupyter notebook 上运行 [tutorial](./tutorial.ipynb) 熟悉数据集与对应的开发工具。


<p align="right">(<a href="#top">回到顶部</a>)</p>



## 基准和排行榜
我们将提供 OpenLane-V2 数据集的初始基准测试，欢迎您在这里添加您的工作!
基准和排行榜将在不久后发布，请持续关注。

| Method | OLS (main metric) | $mAP_{LC}$ | $mAP_{TE}$ | $mAP_{LCLC}$ | $mAP_{LCTE}$ | F-Score* |
| - | - | - | - | - | - | - |
| - | - | - | - | - | - | - |

<sub>*在比赛和排行榜中不考虑 F-Score。
  
<p align="right">(<a href="#top">回到顶部</a>)</p>


## 引用

OpenLane-V2 由上海人工智能实验室的 [OpenDriveLab团队](http://opendrivelab.com/) 和华为 [诺亚方舟实验室](http://dev3.noahlab.com.hk/) 共同合作完成。
使用 OpenLane-V2 时请使用如下引用：
  
```bibtex
@misc{ openlanev2_dataset,
  author = {{OpenLane-V2 Dataset Contributors}},
  title = {{OpenLane-V2: The world's First Perception and Reasoning Benchmark for Scene Structure in Autonomous Driving}},
  url = {https://github.com/OpenDriveLab/OpenLane-V2},
  license = {Apache-2.0},
  year = {2023}
}
```

我们的数据集是基于[NuScenes](https://www.nuscenes.org/nuscenes) 和[Argoverse](https://www.argoverse.org/av2.html)数据集工作拓展而来。如果引用本作，也请使用如下引用：
  
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

<p align="right">(<a href="#top">回到顶部</a>)</p>

## 许可说明
使用 OpenLane-V2 数据集时，您需要在网站上注册并同意 [nuScenes](https://www.nuscenes.org/nuscenes) 和 [Argoverse 2](https://www.argoverse.org/av2.html) 数据集的使用条款。

本项目的发布受 [Apache License 2.0](./LICENSE)许可认证。


<p align="right">(<a href="#top">回到顶部</a>)</p>

