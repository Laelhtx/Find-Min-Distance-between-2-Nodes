from abaqus import *
from abaqusConstants import *
import visualization
import numpy as np
import csv
# from sklearn.neighbors import KDTree

vp = session.viewports[session.currentViewportName]
odb = vp.displayedObject

print(odb.name)
print(odb.steps.keys())

nodeSetA = "NodeSetA-2"
nodeSetB = "NodeSetB_21"
setNames = [nodeSetA, nodeSetB]

step = odb.steps.values()[-1]
frame = step.frames[-1]


def calcFinalCoord(nodeSet, stepName = "Load"):
    finalCoord = []
    allNodeID = []
    node_set = odb.rootAssembly.nodeSets[nodeSet].nodes[0]
    for node in node_set:
        originalCoord_temp = node.coordinates
        nodeID = node.label
        finalU_temp = odb.steps[stepName].frames[-1].fieldOutputs["U"].getSubset(region = node).values[0].data
        finalCoord_temp = originalCoord_temp + finalU_temp
        finalCoord.append(finalCoord_temp)
        allNodeID.append(nodeID)
    return finalCoord, allNodeID

finalCoordA, setA_ID = calcFinalCoord(nodeSetA)
finalCoordB, setB_ID = calcFinalCoord(nodeSetB)

finalCoordA = np.array(finalCoordA)
finalCoordB = np.array(finalCoordB)
setA_ID = np.array(setA_ID).reshape(-1, 1)
setB_ID = np.array(setB_ID).reshape(-1, 1)
combined_A = np.hstack((setA_ID, finalCoordA))
combined_B = np.hstack((setB_ID, finalCoordB))

with open("Final_Coordinates_of_set_A_2.csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerow(["Node ID", "X", "Y", "Z"])
    writer.writerows(combined_A)

with open("Final_Coordinates_of_set_B_2.csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerow(["Node ID", "X", "Y", "Z"])
    writer.writerows(combined_B)

