from abaqus import *
from abaqusConstants import *
import visualization
import numpy as np
import csv
# from sklearn.neighbors import KDTree

vp = session.viewports[session.currentViewportName]
odb = vp.displayedObject

nodeSetA = "NodeSetA-2"
nodeSetB = "NodeSetB_21"

step = odb.steps.values()[-1]
frame = step.frames[-1]


def calcFinalCoord(nodeSet, stepName = "Load"):
    # Get the node set from the ODB
    node_set = odb.rootAssembly.nodeSets[nodeSet]

    # Get the original coordinates of the nodes in the set
    originalCoord_Obj_List = node_set.nodes[0]
    originalCoord = list(map(lambda x: x.coordinates, originalCoord_Obj_List))

    # Get the node IDs of the nodes in the set
    nodeID = list(map(lambda x: x.label, originalCoord_Obj_List))

    # Get the displacement field output for the last frame of the specified step
    finalU_Obj_List = odb.steps[stepName].frames[-1].fieldOutputs["U"].getSubset(region = node_set).values
    finalU = list(map(lambda x: x.data, finalU_Obj_List))
    
    # Calculate the final coordinates by adding the original coordinates and the displacements
    finalCoord = np.array(originalCoord) + np.array(finalU)
    
    return finalCoord, nodeID

finalCoordA, setA_ID = calcFinalCoord(nodeSetA)
finalCoordB, setB_ID = calcFinalCoord(nodeSetB)

finalCoordA = np.array(finalCoordA)
finalCoordB = np.array(finalCoordB)
setA_ID = np.array(setA_ID).reshape(-1, 1)
setB_ID = np.array(setB_ID).reshape(-1, 1)

print(setA_ID.shape)
print(finalCoordA.shape)

combined_A = np.hstack((setA_ID, finalCoordA))
combined_B = np.hstack((setB_ID, finalCoordB))

with open("Final_Coordinates_of_set_A_TestLambda.csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerow(["Node ID", "X", "Y", "Z"])
    writer.writerows(combined_A)

with open("Final_Coordinates_of_set_B_TestLambda.csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerow(["Node ID", "X", "Y", "Z"])
    writer.writerows(combined_B)
