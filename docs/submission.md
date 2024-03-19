# Submission

## Guide

- [Guide for CVPR 2024 AGC Track `Mapless Driving`](#guide-for-cvpr-2024-agc)
- [Guide for China3DV 2024 Track `无图驾驶`](#china3dv-2024-比赛提交说明)
- [Guide for CVPR 2023 Challenge `OpenLane Topology Challenge`](#submission-guide-for-cvpr-2023-challenge)


## Guide for CVPR 2024 AGC
:fire: `Task of CVPR 2024 AGC Track Mapless Driving`

### Driving Scene Topology

The submitted results are required to be stored in a binary `pickle` file, which is a dict of identifier and [formatted Map Element Bucket predictions](../data/README.md#map-element-bucket) a frame.

```
{
    'method':                               <str> -- name of the method
    'authors':                              <list> -- list of str, authors
    'e-mail':                               <str> -- e-mail address
    'institution / company':                <str> -- institution or company
    'country / region':                     <str> -- country or region, checked by iso3166*
    'results': {
        [identifier]: {                     <tuple> -- identifier of the frame, (split, segment_id, timestamp)
            'predictions': {
                'lane_segment':                 ...
                'traffic_element':              ...
                'area':                         ...
                'topology_lsls':                ...
                'topology_lste':                ...
            }
        },
        ...
    }
}
```

### Steps
1. Register for your team by filling in this [Google Form](https://docs.google.com/forms/d/e/1FAIpQLSctm2iipw5r1_wY-kVt7X-4RRynnt3ZzYMzaBVzEpNStoc-rQ/viewform).
2. Prepare your results formatted [as mentioned above](#driving-scene-topology).
3. Follow the steps in the `Submission Information` tab of [**the competition space**](https://huggingface.co/spaces/AGC2024/mapless-driving-2024). 


## China3DV 2024 比赛提交说明
:fire: `China3DV 2024 无图驾驶 赛道`

### 提交结果标准格式

参赛队伍需要将结果保存在二进制格式的`pickle`文件中，提交结果应当遵从以下结构：（其中`results`对应的值为一个字典，包括帧标识符和对应的[预测结果格式](../data/README.md#map-element-bucket)。

```
{
    'method':                               <str> -- name of the method
    'authors':                              <list> -- list of str, authors
    'e-mail':                               <str> -- e-mail address
    'institution / company':                <str> -- institution or company
    'country / region':                     <str> -- country or region, checked by iso3166*
    'results': {
        [identifier]: {                     <tuple> -- identifier of the frame, (split, segment_id, timestamp)
            'predictions': {
                'lane_segment':                 ...
                'traffic_element':              ...
                'area':                         ...
                'topology_lsls':                ...
                'topology_lste':                ...
            }
        },
        ...
    }
}
```

### 提交结果
1. 按上述格式保存结果.
2. 点击[**赛道空间**](https://huggingface.co/spaces/AGC2024/mapless-driving-2024)左侧栏中的**Submission Information**标签页，根据其中的指示完成后续提交过程。 



## Submission Guide for CVPR 2023 Challenge
:fire: `Task of CVPR 2023 OpenLane Topology Challenge`

### OpenLane Topology
The submitted results are required to be stored in a pickle file, which is a dict of identifier and [formatted predictions](../data/README.md#annotations) of a frame:

```
{
    'method':                               <str> -- name of the method
    'authors':                              <list> -- list of str, authors
    'e-mail':                               <str> -- e-mail address
    'institution / company':                <str> -- institution or company
    'country / region':                     <str> -- country or region, checked by iso3166*
    'results': {
        [identifier]: {                     <tuple> -- identifier of the frame, (split, segment_id, timestamp)
            'predictions': {
                'lane_centerline':              ...
                'traffic_element':              ...
                'topology_lclc':                ...
                'topology_lcte':                ...
            }
        },
        ...
    }
}
```

### Steps
1. Create a team on [EvalAI](https://eval.ai/web/challenges/challenge-page/1925).
2. Click the 'Participate' tag, then choose a team for participation.
3. Choose the phase 'Test Phase' and upload the file formatted as mentioned above.
4. Check if the submitted file is valid, which is indicated by the 'Status' under the tag of 'My Submissions'. A valid submission would provide performance scores.
