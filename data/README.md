# Data

## Download
| Subset | Google Drive <img src="https://ssl.gstatic.com/docs/doclist/images/drive_2022q3_32dp.png" alt="Google Drive" width="18"/> | Baidu Yun <img src="https://nd-static.bdstatic.com/m-static/v20-main/favicon-main.ico" alt="Baidu Yun" width="18"/> | md5 | Size |
| --- | --- | --- | --- | --- |
| subset_A | [example](https://drive.google.com/file/d/1TjcGaHSd1tTMl0rsaxdP_GWnKf2CiDIx/view?usp=sharing) | [example](https://pan.baidu.com/s/1BytNMBryAVKCDSlBoDANNA?pwd=bxb9) | cd145ded28f1366475cd81aff9476df4 | ~360M |
| subset_A | coming soon | coming soon | - | - |
| subset_B | coming soon | coming soon | - | - |

## Preprocess
The dataset is preprocessed into pickle files representing different collections, which then be used for training models or evaluation:

```sh
cd data
python OpenLane-V2/preprocess.py 
```

## Hierarchy
The hierarchy of folder `OpenLane-V2/` is described below:
```
└── OpenLane-V2
    ├── train
    |   ├── [segment_id]
    |   |   ├── image
    |   |   |   ├── [camera]
    |   |   |   |   ├── [timestamp].jpg
    |   |   |   |   └── ...
    |   |   |   └── ...
    |   |   └── info
    |   |       ├── [timestamp].json
    |   |       └── ...
    |   └── ...
    ├── val
    |   └── ...
    ├── test
    |   └── ...
    ├── data_dict_example.json
    ├── data_dict_subset_A.json
    ├── data_dict_subset_B.json
    ├── openlanev2.md5
    └── preprocess.py

```

- `[segment_id]` specifies a sequence of frames, and `[timestamp]` specifies a single frame in a sequence.
- `image/` contains images captured by various cameras, and `info/` contains meta data and annotations of a single frame.
- `data_dict_[xxx].json` notes the split of train / val / test under the subset of data.

## Meta Data
The json files under the `info/` folder contain meta data and annotations for each frame.
Each file is formatted as follows:

```
{
    'version':                              <str> -- version
    'segment_id':                           <str> -- segment_id
    'meta_data': {
        'source':                           <str> -- name of the original dataset
        'source_id':                        <str> -- original identifier of the segment
    }
    'timestamp':                            <int> -- timestamp of the frame
    'sensor': {
        [camera]: {                         <str> -- name of the camera
            'image_path':                   <str> -- image path
            'extrinsic':                    <dict> -- extrinsic parameters of the camera
            'intrinsic':                    <dict> -- intrinsic parameters of the camera
        },
        ...
    }                              
    'pose':                                 <dict> -- ego pose
    'annotation':                           <dict> -- anntations for the current frame
}
```

## Annotations
For a single frame, annotations are formatted as follow:

```
{
    'lane_centerline': [                    (n lane centerlines in the current frame)
        {   
            'id':                           <int> -- unique ID in the current frame
            'points':                       <float> [n, 3] -- 3D coordiate
            'confidence':                   <float> -- confidence, only for prediction
        },
        ...
    ],
    'traffic_element': [                    (k traffic elements in the current frame)
        {   
            'id':                           <int> -- unique ID in the current frame
            'category':                     <int> -- traffic element category
                                                1: 'traffic_light',
                                                2: 'road_sign',
            'attribute':                    <int> -- attribute of traffic element
                                                0:  'unknown',
                                                1:  'red',
                                                2:  'green',
                                                3:  'yellow',
                                                4:  'go_straight',
                                                5:  'turn_left',
                                                6:  'turn_right',
                                                7:  'no_left_turn',
                                                8:  'no_right_turn',
                                                9:  'u_turn',
                                                10: 'no_u_turn',
                                                11: 'slight_left',
                                                12: 'slight_right,
            'points':                       <float> [2, 2] -- top-left and bottom-right corners of the 2D bounding box
            'confidence':                   <float> -- confidence, only for prediction
        },
        ...
    ],
    'topology_lclc':                        <float> [n, n] -- adjacent matrix among lane centerlines
    'topology_lcte':                        <float> [n, k] -- adjacent matrix between lane centerlines and traffic elements
}
```

- `id` is the identifier of a lane centerline or traffic element and is consistent in a sequence.
For predictions, it can be randomly assigned but unique in a single frame.
- `topology_lclc` and `topology_lcte` are adjacent matrices, where row and column are sorted according to the order of the lists `lane_centerline` and `traffic_element`. 
It is a MUST to keep the ordering the same for correct evaluation. 
For ground truth, only 0 or 1 is a valid boolean value for an element in the matrix. 
For predictions, the value varies from 0 to 1, representing the confidence of the predicted relationship. 
- #lane_centerline and #traffic_element are not required to be equal between ground truth and predictions. 
In the process of evaluation, a matching of ground truth and predictions is determined.
