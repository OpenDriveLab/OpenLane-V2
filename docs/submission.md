# Submission

## Driving Scene Topology
:fire: `Task of CVPR 2024 AGC Track Mapless Driving`

The submitted results are required to be stored in a `pickle` file, which is a dict of identifier and [formatted Map Element Bucket predictions](../data/README.md#map-element-bucket) a frame.

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



## OpenLane Topology
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

## Steps
1. Create a team on [EvalAI](https://eval.ai/web/challenges/challenge-page/1925).
2. Click the 'Participate' tag, then choose a team for participation.
3. Choose the phase 'Test Phase' and upload the file formatted as mentioned above.
4. Check if the submitted file is valid, which is indicated by the 'Status' under the tag of 'My Submissions'. A valid submission would provide performance scores.
