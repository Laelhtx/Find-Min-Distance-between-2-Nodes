import numpy as np
from sklearn.neighbors import KDTree
import pandas as pd


def readCSV(filename):
    data = pd.read_csv(filename, header=0)
    coordinates = data.iloc[:, 1:4].to_numpy()
    nodeID = data.iloc[:, 0].to_numpy().reshape(-1, 1)
    return coordinates, nodeID


setA_coord, setA_ID = readCSV("..\\ANALYSIS\\SK24-032DA_001\\Final_Coordinates_of_set_A_TestLambda.csv")
setB_coord, setB_ID = readCSV("..\\ANALYSIS\\SK24-032DA_001\\Final_Coordinates_of_set_B_TestLambda.csv")

def find_min_distance(setA_coord, setA_ID, setB_coord, setB_ID):
    # Build KDTree for set B
    tree = KDTree(setB_coord, leaf_size=2)
   
    # Query the nearest neighbor in set B for each node in set A
    distances, indices = tree.query(setA_coord, k=1)  # k=1 for the closest neighbor
   
    # Find the minimum distance and its index
    min_index = np.argmin(distances)
    min_distance = distances[min_index][0]
    coordA = setA_coord[min_index]
    coordB = setB_coord[indices[min_index][0]]
   
    # Get the corresponding node IDs
    nodeA_ID = setA_ID[min_index][0]
    nodeB_ID = setB_ID[indices[min_index][0]][0]
   
    return min_distance, nodeA_ID, nodeB_ID, coordA, coordB


# Example usage
min_dist, nodeA_ID, nodeB_ID, coordA, coordB= find_min_distance(setA_coord, setA_ID, setB_coord, setB_ID)


def getVerticalProjection(coordA, coordB):
    # Calculate the vector between the two points
    vector = coordB - coordA
   
    # Define the vertical direction (0, 0, 1)
    vertical_direction = np.array([0, 1, 0])
   
    # Calculate the projection of the vector onto the vertical direction
    projection = np.dot(vector, vertical_direction)

    return projection


def getRadialProjection(coordA, coordB, axis="Y"):
    # Calculate the vector between the two points
    vector = coordB - coordA

    # Determine the R axis direction
    if axis == "X":
        e_z = np.array([1, 0, 0])
        project_plane = np.array([0, 1, 1])
    elif axis == "Y":
        e_z = np.array([0, 1, 0])
        project_plane = np.array([1, 0, 1])
    elif axis == "Z":
        e_z = np.array([0, 0, 1])
        project_plane = np.array([1, 1, 0])
   
    # Define the unit vector in radial direction
    proj = coordB * project_plane
    r_norm = np.linalg.norm(proj)
    if r_norm == 0:
        raise ValueError("Radial direction is undefined at the axis.")
   
    # Normalize the radial direction vector
    e_r = proj / r_norm

    # Calculate the projection of the vector onto the radial direction
    projection = np.dot(vector,e_r)

    return projection

vertical_projection = getVerticalProjection(coordA, coordB)
radial_projection = getRadialProjection(coordA, coordB, axis="Y")

print(f"Minimum Distance: {min_dist}")
print(f"Node in A: {nodeA_ID}, Coordinates: {coordA}")
print(f"Node in B: {nodeB_ID}, Coordinates: {coordB}")
print(f"Vertical Projection of Minimum Distance: {vertical_projection}")
print(f"Radial Projection of Minimum Distance: {radial_projection}")

