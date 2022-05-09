# Hourglass Data Post Processing

UAV_PPK:
In complex mountainous terrain, RTK base station corrections may be insufficient for correct model alignments across multiple dates. For this reason, the following workflow is created to be able to improve GPS locational accuracy. UAV_PPK provides the code necessary to correct the UAV collected GPS data for the entirety of a flight based on the MTSU CORS Base Station located on the Montana State University Campus. This code is based on the AEROTAS excel sheet found here: https://www.aerotas.com/phantom-4-rtk-ppk-processing-workflow and works to improve transparency and automation for the data products collected by the UAV. The next code will then correct geolocation tags on UAV collected imagery to be read into a flight imagery processing application.

UAV_PhotoLocations:
This code is still in development! When completed, this will repopulate UAV images with their corrected geolocation information. Until this code is complete, you can just read in the output file from the previous code into your flight imagery processing software.

HG_WX_Cleanup:
At the fieldsite, there is an automated weather station present. This weather station collects a variety of information, but to be used correctly, needs to be further cleaned. This code provides the framework necessary to clean up variables for this exported dataset. 
