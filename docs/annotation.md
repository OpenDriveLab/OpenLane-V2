# Annotation

## Criterion

The road structure cognition task is defined as inputting the surrounding view images, reconstructing the high-precision map of the self-vehicle, and outputting the recognition result of the direction of the self-vehicle. 
The specific expansion is to input the surrounding view images of the vehicle, HDMap; the output is the lane centerlines, the traffic signs, the topology of the lane centerlines, and the correspondence between lanes centerlines and traffic signs. 
Below are examples of visualizing annotations and relationships between different elements on 2D images.

![image](https://user-images.githubusercontent.com/47048022/209953048-f8ded0da-6005-45b7-8e3d-501dbd422058.png)
![image](https://user-images.githubusercontent.com/47048022/209954207-7b8a1b5a-8243-41d5-91fe-f2de5949107e.png)

## Note

**Traffic Light Properties**
1. Category: circle, left arrow, right arrow, forward arrow, down arrow, right up arrow, bicycle, pedestrian

<div align=center><img src="https://user-images.githubusercontent.com/47048022/209899975-6a728b57-b053-4cd4-87fd-f41a79822a8f.png" width="240" height="160" /><img src="https://user-images.githubusercontent.com/47048022/209902369-32d47838-b5fb-4f6e-b65b-ac7be98cd38b.png" width="240" height="160" /><img src="https://user-images.githubusercontent.com/47048022/209089845-6727edc9-fe13-463c-ba54-3eb2ac301756.png" width="240" height="160" />
</div>


2. Direction: facing, facing left, facing right, leaning left, leaning right
<div align=center><img src="https://user-images.githubusercontent.com/47048022/209089755-00a133ca-2176-4d96-ba9c-ab51ba21779d.png" width="240" height="160" /><img src="https://user-images.githubusercontent.com/47048022/209901358-e0da6866-5b9d-4326-9582-2c2b383b627e.png" width="240" height="160" /><img src="https://user-images.githubusercontent.com/47048022/209901436-4c688ef3-217e-432a-bfda-d9a3a34a89e4.png" width="240" height="160" /></div>


3. Color: red, green, yellow

<div align=center><img src="https://user-images.githubusercontent.com/47048022/209089813-6cdf68be-111d-4c7d-94e6-d4657165d8d0.png" width="240" height="160" /><img src="https://user-images.githubusercontent.com/47048022/209902494-a41d4b56-ebb9-4d3f-b3a5-d55a730a10f6.png" width="240" height="160" /><img src="https://user-images.githubusercontent.com/47048022/209901835-bc8d9781-bea0-4c40-804e-25375830171d.png" width="240" height="160" /></div>
