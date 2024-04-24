# Submission

## Guide

- [Guide for CVPR 2024 AGC Track `Mapless Driving`](#guide-for-cvpr-2024-agc)
- [Guide for CVPR 2023 Challenge `OpenLane Topology Challenge`](#submission-guide-for-cvpr-2023-challenge)


## Guide for CVPR 2024 AGC
:fire: `CVPR 2024 AGC Track Mapless Driving`
> - Official website: :globe_with_meridians: [AGC2024](https://opendrivelab.com/challenge2024/#mapless_driving)
> - Evaluation server: :hugs: [Hugging Face](https://huggingface.co/spaces/AGC2024/mapless-driving-2024)

### Driving Scene Topology

The submitted results of `OpenLane-V2 subset-A test` are required to be stored in a binary `pickle` file, which is a dict of identifier and [formatted Map Element Bucket predictions](/data/README.md#map-element-bucket) a frame.

```
{
    'method':                               <str> -- name of the method
    'team':                                 <str> -- name of the team, identical to the Google Form
    'authors':                              <list> -- list of str, authors
    'e-mail':                               <str> -- e-mail address
    'institution / company':                <str> -- institution or company
    'country / region':                     <str> -- country or region, checked by iso3166*
    'results': {
        [identifier]: {                     <tuple> -- identifier of the frame, (split, segment_id, timestamp)
            'predictions': {
                'lane_segment':[            (i lane segments in the current frame)
                    {   
                        'id':               <int> -- unique ID in the current frame
                        'centerline':       <float> [n, 3] -- 3D coordiate
                        'left_laneline':    <float> [n, 3] -- 3D coordiate
                        'right_laneline':   <float> [n, 3] -- 3D coordiate
                        'confidence':       <float> -- confidence
                    },
                    ...
                ],
                'traffic_element':[         (j traffic elements in the current frame)
                    {
                        'id':               <int> -- unique ID in the current frame
                        'attribute':        <int> -- attribute of traffic element
                        'points':           <float> [2, 2] -- top-left and bottom-right corners of the 2D bounding box
                        'confidence':       <float> -- confidence, only for prediction
                    },
                    ...
                ],
                'area':[                    (k areas in the current frame)
                    {   
                        'id':               <int> -- unique ID in the current frame
                        'category':         <int> -- area category
                        'points':           <float> [n, 3] -- 3D coordiate
                        'confidence':       <float> -- confidence, only for prediction
                    },
                    ...
                ],
                'topology_lsls':            <float> [n, n] -- adjacent matrix among lane segments
                'topology_lste':            <float> [n, k] -- adjacent matrix between lane segments and traffic elements
            }
        },
        ...
    }
}
```
- The `#points` of lane segment and area could be various. But we recommend `10` for each line in lane segment and `20` for area to keep align with ground truth.
- We recommend astype all `float` to `np.float16` to reduce the submission file size.

### Test before submission
Hugging Face server will not return any detailed error if submission failed. Please test the submission file of `val` set before submit.

``` python
from openlanev2.lanesegment.evaluation.evaluate import evaluate

metrics = evaluate(
    ground_truth='data/OpenLane-V2/data_dict_subset_A_val_ls.pkl', 
    predictions='/path/to/submission.pkl'
)
print(metrics)
```

### Steps
1. Register for your team by filling in this [Google Form](https://docs.google.com/forms/d/e/1FAIpQLSctm2iipw5r1_wY-kVt7X-4RRynnt3ZzYMzaBVzEpNStoc-rQ/viewform).
2. Prepare your results formatted [as mentioned above](#driving-scene-topology).
3. Follow the steps in the `Submission Information` tab of [**the competition space**](https://huggingface.co/spaces/AGC2024/mapless-driving-2024). 


## Submission Guide for CVPR 2023 Challenge
:fire: `CVPR 2023 OpenLane Topology Challenge`

### OpenLane Topology
The submitted results are required to be stored in a pickle file, which is a dict of identifier and [formatted predictions](/data/README.md#annotations) of a frame:

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
