This repository is created in order to calculated the minimum distance between 2 surfaces after finite element analysis in ABAQUS.
It consists of 2 parts: 
(1) Get_Final_Coordinates: 
  a. Get all the nodes of the 2 surfaces and gather in node set A and node set B
  b. Obtain the original nodes coordinates before loading and the final displacement components in X, Y and Z
  c. Calculate the final nodes coordinates by adding the final displacement components to the original nodes coordinates
  d. The original version is using for loop to extract each nodes coordinates and displacement, while the 001 version is using Lambda to extract the values in batch. It reduces a lot of running time.
(2) Calc_Min_Diatance
  a. Use KD-Tree to find the minimum distance to reduce running time. (Get rid of the For loops which consumes great amount of time
