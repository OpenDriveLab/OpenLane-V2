# Devkit
Here we describe the API provided by the OpenLane-V2 devkit.
The subpackage `openlanev2.centerline` comprises tools for the original task of scene structure perception and reasoning, while the subpackage `openlanev2.lanesegment` is specified for the Map Element Bucket.

## dataset

`Collection` is a collection of frames and `Frame` is a data structure containing meta data of a frame.

## evaluation

Given the ground truth and predictions, which are formatted dict or the path to pickle storing the dict that ground truth is preprocessed pickle file and predictions are formatted as described [here](./submission.md#format), this function returns a dict storing all metrics defined by our task.

## io
This subpackage wraps all IO operations of the OpenLane-V2 devkit.
It can be modified for different IO operations.

## preprocessing

Given a data_dict storing identifiers of frames, this function collects meta data the frames and stores it into a pickle file for efficient IO for the following operations.

## visualization
This subpackage provides tools for visualization. Please refer to the [tutorials](/tutorials) for examples.
