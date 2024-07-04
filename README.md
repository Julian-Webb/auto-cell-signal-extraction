This is a method to extract the signals of cells in a recording. It works based on clustering parts of the image based on the similarity of their signals.
It has been developed and used for extraction of signals from calcium imaging recordings of glioblastoma cells but has the potential to work for other types of cells.

# Approach
The approach consists of the following steps:  
A) Read out relevant **properties** of the **image** (height, width, number of frames, etc.)  
B) Divide the image into small squares ("**regions of interest**"/ROIs) in a grid-like fashion   
C) For each ROI, extract the **signal over time**  
D) **Detrend the signal**  
E) **Remove the ROIs** that don't contain a cell  
F) Calculate the **distances/similarities** between the signals of the ROIs (only if using agglomerative clustering)  
G) **Cluster** the ROIs based on their signal similarity (and, in some cases, location)  
H) For each cluster, extract a **representative signal** based on its members  

Since, each cluster should represent a cell, the final result is a signal for each cell.  

*For further details, see `Using Activity-Related Signal Changes for Automated Cell Segmentation and Signal Extraction.pdf`.*

# File Structure
The **src** folder contains all the code. 
The main file to execute is `main.py`. 
Before executing, all file paths, parameters, and analysis options must be specified in `options.py`.
The remaining code is structured according to the alphabetic order of the steps above.
The folder of a step generally contains its code for computation and for visualization of that step.

The **data** folder contains the data to be analyzed.
To analyze a recording, create a folder with its name. 
Inside that folder create a folder called 'raw' and place the recording inside.
For example, if the recording is called 'recording1.tif', the path should be 'data/recording1/raw/recording1.tif'.
When running, the code will automatically create a results and figures folder and place the resulting files there.


