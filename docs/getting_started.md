# Getting Started

## Download Data
The OpenLane-V2 dataset is a large-scale dataset for scene structure perception and reasoning in the field of autonomous driving. 
Following [OpenLane-V1](https://github.com/OpenDriveLab/OpenLane), the first 3D lane dataset, we provide lane annotations in 3D space.
The difference is that instead of lane lines, we annotate lane centerlines, which can be served as the trajectory for autonomous vehicles.
Besides, we provide annotations on traffic elements (traffic lights and road signs) and their attribute, and the topology relationships among lane centerlines and between lane centerlines and traffic elements.

The dataset is divided into two subsets. 

- **The `subset_A` serves as the primary subset and is utilized for the coming challenges and leaderboard, in which no external data, including the other subset, is allowed**.

- The `subset_B` can be used to test the generalization ability of the model.
For more details, please refer to the corresponding pages: [use of data](/data/README.md), [notes of annotation](/docs/annotation.md), and [dataset statistics](/docs/statistics.md).

[Download](/data/README.md#download) now to discover our dataset!


## Install Devkit
We provide a devkit for easy access to the OpenLane-V2 dataset.
After installing the package, the use of the dataset, such as loading images, loading meta data, and evaluating results, can be accessed through the API of `openlanv2`.
For more details on the API, please refer to [devkit](/docs/devkit.md).


## Prepare Dataset
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

2. Use [links](/data/README.md#download) to download data manually from 

    - <img src="https://user-images.githubusercontent.com/29263416/222076048-21501bac-71df-40fa-8671-2b5f8013d2cd.png" alt="OpenDataLab" width="18"/> OpenDataLab,
    - <img src="https://user-images.githubusercontent.com/29263416/236970575-125919cc-1a36-4968-95e7-f5a17f896f9f.png" alt="Google Drive" width="18"/> Google Drive,
    - <img src="https://user-images.githubusercontent.com/29263416/236970717-fe619dd6-7e36-446b-88bf-30ff91028d87.png" alt="Baidu Yun" width="18"/> Baidu Yun.

    Then put them into the `data/OpenLane-V2/` folder and unzip them. 
    The resulting folder hierarchy is described [here](/data/README.md#hierarchy).
    Or use the following commands to download example data for a quick glance at the dataset:

    ```sh
    cd data/OpenLane-V2
    wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1Ni-L6u1MGKJRAfUXm39PdBIxdk_ntdc6' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1Ni-L6u1MGKJRAfUXm39PdBIxdk_ntdc6" -O OpenLane-V2_sample.tar
    md5sum -c openlanev2.md5
    ls *.tar* | xargs -n1 tar -xvf
    cd ../..
    ```

3. Run the [tutorials](/tutorials) on jupyter notebook to get familiar with the dataset and devkit.


## Train a Model

Plug-ins are provided to start training models on the OpenLane-V2 dataset.
We appreciate your valuable feedback and contributions to plug-ins on different frameworks.

### TODO
- [ ] Plug-in for dataset `v2.0`
- [x] Plug-in for dataset `v1.0`

### Baseline

The [plug-in](/plugin/models/) is built on top of [v1.0.0rc6](https://github.com/open-mmlab/mmdetection3d/tree/v1.0.0rc6) and tested under:
- Python 3.8.15
- PyTorch 1.9.1
- CUDA 11.1
- GCC 5.4.0
- mmcv-full==1.5.2
- mmdet==2.26.0
- mmsegmentation==0.29.1

Please follow the [instruction](https://github.com/open-mmlab/mmdetection3d/blob/v1.0.0rc6/docs/en/getting_started.md) to install the framework.
Assuming OpenLane-V2 is installed under `OpenLane-V2/` and the framework is built under `framework/`, create a soft link to the plug-in file:
```
└── framework
    └── projects
        ├── example_project
        └── openlanev2 -> OpenLane-V2/plugin/models
```
Then you can train or evaluate a model using the config `framework/projects/openlanev2/configs/baseline.py`, whose path is replaced accordingly.
Options can be passed to enable supported functions during evaluation (`--eval *`), such as `--eval-options dump=True dump_dir=/PATH/TO/DUMP` to save pickle file for submission and `--eval-options visualization=True visualization_dir=/PATH/TO/VIS` for visualization.
