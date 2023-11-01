# Metrics

> Note
>
> ❗️Update on **evaluation metrics** led to differences in TOP scores between `vx.1` ([`v1.1`](https://github.com/OpenDriveLab/OpenLane-V2/releases/tag/v1.1.0), [`v2.1`](https://github.com/OpenDriveLab/OpenLane-V2/releases/tag/v2.1.0)) and `vx.0` (`v1.0`, `v2.0`).
> We encourage the use of **`vx.1`** metrics.
> For more details please see issue [#76](https://github.com/OpenDriveLab/OpenLane-V2/issues/76).

## Driving Scene Topology
We define the **OpenLane-V2 UniScore (OLUS)**, which is the average of various metrics covering different aspects of the primary task:

```math
\text{OLUS} = \frac{1}{5} \bigg[ \text{DET}_{l} + \text{DET}_{a} + \text{DET}_{t} + f(\text{TOP}_{ll}) + f(\text{TOP}_{lt}) \bigg].
```

To evaluate performances on different aspects of the task, several metrics are adopted:
- $\text{DET}_{l}$ for mAP on lane segments,
- $\text{DET}_{a}$ for mAP on areas,
- $\text{DET}_{t}$ for mAP on traffic elements,
- $\text{TOP}_{ll}$ for mAP on topology among lane segments,
- $\text{TOP}_{lt}$ for mAP on topology between lane segments and traffic elements.

If not described explicitly, the metrics are similar to those in the task of [OpenLane Topology](#openlane-topology).
  
### Lane Segment
We adopt the average precision (AP) but define a match of lane segments by considering the lane segment distance.
The mAP for lane segments is averaged over match thresholds of $\\{1.0, 2.0, 3.0\\}$ on the similarity measure.

### Area
Areas, namely pedestrian crossings and road boundaries, are regarded as undirected curves, which are closed or intersected with the boundaries of the BEV range.
We use Chamfer distance to describe the similarity of areas.


## OpenLane Topology
The primary task of the dataset is **scene structure perception and reasoning**, which requires the model to recognize the dynamic drivable states of lanes in the surrounding environment. 
The challenge of this dataset includes not only detecting lane centerlines and traffic elements but also recognizing the attribute of traffic elements and topology relationships on detected objects.
We define the **OpenLane-V2 Score (OLS)**, which is the average of various metrics covering different aspects of the primary task:

```math
\text{OLS} = \frac{1}{4} \bigg[ \text{DET}_{l} + \text{DET}_{t} + f(\text{TOP}_{ll}) + f(\text{TOP}_{lt}) \bigg].
```

<!-- The metrics of different subtasks are described below. -->

To evaluate performances on different aspects of the task, several metrics are adopted:
- $\text{DET}_{l}$ for mAP on directed lane centerlines,
- $\text{DET}_{t}$ for mAP on traffic elements,
- $\text{TOP}_{ll}$ for mAP on topology among lane centerlines,
- $\text{TOP}_{lt}$ for mAP on topology between lane centerlines and traffic elements.

We consolidate the above metrics by computing an average of them, resulting in the **OpenLane-V2 Score (OLS)**.

### Lane Centerline
We adopt the average precision (AP) but define a match of lane centerlines by considering the discrete Frechet distance in the 3D space.
The mAP for lane centerlines is averaged over match thresholds of $\\{1.0, 2.0, 3.0\\}$ on the similarity measure.

### Traffic Element
Similarly, we use AP to evaluate the task of traffic element detection.
We consider IoU distance as the affinity measure with a match threshold of $0.75$.
Besides, traffic elements have their own attribute.
For instance, a traffic light can be red or green, which indicates the drivable state of the lane.
Therefore, the mAP is then averaged over attributes.

### Topology
The topology metrics estimate the goodness of the relationship among lane centerlines and the relationship between lane centerlines and traffic elements.
To formulate the task of topology prediction as a link prediction problem, we first determine a match of ground truth and predicted vertices (lane centerlines and traffic elements) in the relationship graph.
We choose Frechet and IoU distance for the lane centerline and traffic element respectively.
Also, the metric is average over different recalls.

We adopt mAP from link prediction, which is defined as a mean of APs over all vertices. 
Two vertices are regarded as connected if the predicted confidence of the edge is greater than $0.5$.
The AP of a vertex is obtained by ranking all predicted edges and calculating the accumulative mean of the precisions:

```math
mAP = \frac{1}{|V|} \sum_{v \in V} \frac{\sum_{\hat{n} \in \hat{N}(v)} P(\hat{n}) \mathbb{1}(\hat{n} \in N(v))}{|N(v)|},
```

where $N(v)$ denotes ordered list of neighbors of vertex $v$ ranked by confidence and $P(v)$ is the precision of the $i$-th vertex $v$ in the ordered list.

Given ground truth and predicted connectivity of lane centerlines, the mAP is calculated on $G^{l} = (V^{l}, E^{l})$ and $\hat{G}^{l} = (\hat{V}^{l}, \hat{E}^{l})$.
As the given graphs are directed, e.g., the ending point of a lane centerline is connected to the starting point of the next lane centerline, we take the mean of mAP over graphs with only in-going or out-going edges.

To evaluate the predicted topology between lane centerlines and traffic elements, we ignore the relationship among lane centerlines.
The relationship among traffic elements is also not taken into consideration.
Thus this can be seen as a link prediction problem on a bipartite undirected graph that $G = (V^{l} \cup V^{t}, E)$ and $\hat{G} = (\hat{V}^{l} \cup \hat{V}^{t}, \hat{E})$.

# Distances

### Frechet Distance
Discrete Frechet distance measures the geometric similarity of two ordered lists of points.
Given a pair of curves, namely a ground truth $v = (p_1, ..., p_n)$ and a prediction $\hat{v} = (\hat{p}_1, ..., \hat{p}_k)$, a coupling $L$ is a sequence of distinct pairs between $v$ and $\hat{v}$:

```math
(p_{a_1} \ , \ \hat{p}_{b_1} \ ), ..., (p_{a_m} \ , \ \hat{p}_{b_m} \ ),
```

where $a_1, ..., a_m$ and $b_1, ..., b_m$ are nondecreasing surjection such that $1 = a_1 \leq a_i \leq a_j \leq a_m = n$ and $1 = b_1 \leq b_i \leq b_j \leq b_m = k$ for all $i < j$. Then the norm $||L||$ of a coupling $L$ is the distance of the most dissimilar pair in $L$ that:

```math
||L|| = \mathop{max}_{i=1, ..., m} D(p_{a_i} \ , \ \hat{p}_{b_i} \ ).
```

The Frechet distance of a pair of curves is the minimum norm of all possible coupling that:

```math
D_{Frechet}(v, \hat{v}) = min\\{||L|| \ | \ for \ all \ possible \ coupling \ L\\}.
```

### Chamfer Distance
Chamfer distance measures the similarity between two unordered sets by considering the distance of each permutation of the elements.
Given a pair of point sets, namely the ground truth $v = (p_1, ..., p_n)$ and a prediction $\hat{v} = (\hat{p}_1, ..., \hat{p}_k)$, the Chamfer distance is calculated as:

```math
D_{Chamfer}(v, \hat{v}) = \frac{1}{2}(\frac{1}{|v|}\sum_{p \in v} \mathop{min}_{\hat{p} \in \hat{v}} ||p, \hat{p}||_2 + \frac{1}{|\hat{v}|}\sum_{\hat{p} \in \hat{v}} \mathop{min}_{p \in v} ||\hat{p}, p||_2).
```

### IoU Distance
To preserve consistency to the distance mentioned above, we modify the common IoU (Intersection over Union) measure that:

```math
D_{IoU}(X, \hat{X}) = 1 - \frac{|X \cap \hat{X}|}{|X \cup \hat{X}|},
```

where $X$ and $\hat{X}$ is the ground truth and predicted bounding box respectively.

### Lane Segment Distance
By taking the similarity of the centerline and lanelines into account simultaneously, for a pair of lane segments $v = (v_c, v_l, v_r)$ and $\hat{v} = (\hat{v}_c, \hat{v}_l, \hat{v}_r)$, where $v_c$ denotes the centerline, $v_l$ and $v_r$ denotes the left and right lanelines respectively, we define the lane segment distance as:

```math
D_{lane\_segment}(v, \hat{v}) = \frac{1}{2}\bigg(D_{Frechet}(v_c, \hat{v}_c) + D_{Chamfer}(v_l, \hat{v}_l) + D_{Chamfer}(v_r, \hat{v}_r)\bigg).
```
