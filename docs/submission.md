# Submission

## Format
The submitted results are required to be stored in a pickle file, which is a dict of identifier and [formatted predictions](../data/README.md#annotations) of a frame:

```
{
    'method':                               <str> -- name of the method
    'authors':                              <str> -- list of authors
    'affiliation':                          <str> -- optional, affiliation
    'description':                          <str> -- optional, description of the method
    'url':                                  <str> -- optional, link to paper or repository
    'predictions': {
        [identifier]: {                     <tuple> -- identifier of the frame, (split, segment_id, timestamp)
            'lane_centerline':              ...
            'traffic_element':              ...
            'topology_lclc':                ...
            'topology_lcte':                ...
        },                       
        ...
    }
}
```

## Instruction
The submission instruction is coming soon.
