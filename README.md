# Hourglass Data Post Processing

## 01_PPK_Correction.ipynb

When conducting UAV flights in complex mountainous terrain, RTK capabilities may be insufficient when creating models based on the imagery collected. This is because satellite ephemeris errors 
change from day to day, and these errors are further exaggerated when you already have fewer observed satellites and unequal sky coverage due the influence of steep slopes. For this reason, it 
can become necessary to post-process your UAV imagery before further processing. This code can be used to achieve that. 

The steps of this code are as follows:
1. Import the RTKLIB corrected RINEX drone data
1. Import the Timestamp.MRK file created from the UAV
1. Create a calculation dataframe to correct imagery locations based on the corrected RTKLIB file
1. Create a new export file with updated Lat, Lon, and elevation and associated errors
1. Read the original exif data from the images and append that to your export file
1. Subtract the observed snow depth at the RTK site from each elevation observation
1. Export a final .csv with the updated lat, long, elevation and pitch, roll, yaw

### When carrying out this code, it is important to have a specific file structure in place. You can tweak the code for your own needs, but this structure has worked well for me. 

* Within your holding folder, mine is titled "HG_PPK", have multiple folders for each day of flights with their date in the form "20210624".
* In this folder, have a folder for your images titled "Imagery", and a folder for your GPS files titled "Raw_files".
* Within the imagery folder, have folders for each flight done on that day
* Within the raw_files folder, have all your RTKLIB corrected RINEX files saved as .csv and all timestamp files saved as .MRK

--- 
**Optional Folders**
* RTK Base heights in a .csv file

If done correctly, the end of the code should export an updated .csv file titled "Date of flight"+Corrected_Imagery_Locs.csv 

## HG_WX_Cleanup:

At the fieldsite, there is an automated weather station present. This weather station collects a variety of information, but to be used correctly, needs to be further cleaned. This code provides the framework necessary to clean up variables for this exported dataset. 

**Hourglass_Hourly.csv**
This is an example file that is downloaded directly from the Campbell datalogger. This code can be cloned with this repository to be run as an example code for the HG_WX_Cleanup code. 
