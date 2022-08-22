#!/usr/bin/env python
# coding: utf-8

# MSc student, Zachary Miller, worked to create an R script to accomplish what the excel file did. This is my first attempt to transfer this file to a python notebook to allow for an integrated, easier workflow, as well as the ability for others to work on this data on cloud servers, such as google.colab. This code was first created 20220323
# 
# *This code was next worked on 20220506
# *This code is currently including the code that I know works! I am still trying to figure out how to get the closest timestamp calculations to work, but wanted to create a clean code that I know is working so that my V1 code can continue to be very messy without making mistakes.

# In[1]:


# Import numerical tools
import numpy as np
# Import pyplot for plotting
import matplotlib.pyplot as plt
#Import pandas for reading in and managing data
import pandas as pd
import math
# Magic function to make matplotlib inlineSet the filename for the code used for your imagery collection. This is the first 7 digits when you download imagery. Set the date for your flight collections.; other style specs must come AFTER
get_ipython().run_line_magic('matplotlib', 'inline')
get_ipython().run_line_magic('config', "InlineBackend.figure_formats = {'svg',}")
#Comment the above line and uncomment the line below if svg graphics are not working in your browser.
#%config InlineBackend.figure_formats = {'png', 'retina'}


# Set the filename for the code used for your imagery collection. This is the first 7 digits when you download imagery. Set the date for your flight collections.

# In[2]:


filename = "101_0170"
date = "20210310"


# Read in the already corrected RINEX file from the drone. 

# In[6]:


RTKLIB_record = pd.read_csv('/Users/f67f911/Desktop/UAV_PPK_GitHub/101_0170_Rinex_conv.csv')
# View the head of the data to make sure it has been read in correctly
RTKLIB_record.head()


# Read in the timestamp data as is from the UAV. 

# In[7]:


timestamp_record = pd.read_table('/Users/f67f911/Desktop/UAV_PPK_GitHub/101_0170_Timestamp.MRK', header = None)
timestamp_record.columns = ['Photo', 'GPS_Date','% GPST','Northing_diff_mm','Easting_diff_mm','Elevation_diff_mm','Lat','Lon','Height_m','std_North_m, std_East_m, std_Ele_m','RTK_status_flag']
# View the head of the data to make sure it has been read in correctly. 
timestamp_record.head()


# Note status flag values - 0: no positioning; 16: single-point positioning mode; 34:RTK floating solution; 50: RTK fixed solution. When flag of a photo is not equal to 50, it is recommended that you should not use that image in further processing.

# Clean the timestamp file to convert non-numeric text in columns to numeric

# In[8]:


# Create a holding record for the timestamp data in case the dataframe is messed up
timestamp = timestamp_record


# When looking at our columns, we can see that there are many numbers followed by letters. We need to get rid of those numbers in order to continue with our analysis. This code can definitely be cleaned up. For example, right now it works because all of the flight logs I am using take place in the United States, meaning that the letters following the timestamp data will all be the same. However, this is not necessarily the case in other areas.
# * Further code should focus on getting rid of values in the columns that are not of the type string. Note that future code will still need to make sure to maintain positive and negative values. Without this, the further calculations will be messed up.

# In[9]:


timestamp['Northing_diff_mm'] = timestamp['Northing_diff_mm'].str.replace(',N', '')
timestamp['Easting_diff_mm'] = timestamp['Easting_diff_mm'].str.replace(',E', '')
timestamp['Elevation_diff_mm'] = timestamp['Elevation_diff_mm'].str.replace(',V', '')
timestamp['Lat'] = timestamp['Lat'].str.replace(',Lat','')
timestamp['Lon'] = timestamp['Lon'].str.replace(',Lon','')
timestamp['Height_m'] = timestamp['Height_m'].str.replace(',Ellh','')
#timestamp['std_North_m, std_East_m, std_Ele_m'] = timestamp['std_North_m, std_East_m, std_Ele_m'].str.replace(',','')
timestamp['RTK_status_flag'] = timestamp['RTK_status_flag'].str.replace(',Q','')


# In[15]:


# Look at the datatypes for the timestamps. The way the csv is read in, the column data is not necessarily in the 
# correct format. We can check what data type each of the columns is, and change as needed.
timestamp.dtypes


# In[17]:


# Let's change those datatypes so we can actually do calculations on the column values!
timestamp['Northing_diff_mm'] = timestamp['Northing_diff_mm'].astype(int)
timestamp['Easting_diff_mm'] = timestamp['Easting_diff_mm'].astype(int)
timestamp['Elevation_diff_mm'] = timestamp['Elevation_diff_mm'].astype(int)
timestamp['Lat'] = timestamp['Lat'].astype(float)
timestamp['Lon'] = timestamp['Lon'].astype(float)
timestamp['Height_m'] = timestamp['Height_m'].astype(float)
timestamp.head()


# Calculate camera specific positions. Step one is to create a calculations spreadsheet.

# In[10]:


# In the future, I think I can drop the Closest_Loc_ID, since the merging way that I am doing the data will 
# mess up this ID, and therefore will negate the need to have these columns.
calc = pd.DataFrame(columns = ['Northing_diff_mm','Easting_diff_mm','Elevation_diff_mm','Closest_Loc_ID',
                    'Timestamp_of_Closest','Closest_Lat','Closest_Lon','Closest_El','2nd_Closest_Loc_ID',
                    'Timestamp_of_2nd_Closest','2nd_closest_Lat','2nd_Closest_Lon','2nd_Closest_El',
                    'Percent_diff_between_timestamps','Interpolated_Lat','Interpolated_Lon','Interpolated_El',
                    'Lat_Diff_deg','Lon_Diff_deg','El_diff_m','New_Lat','New_Lon','New_El'])


# Step 2: Calculate the values and input into the calc dataframe

# In[18]:


calc['Northing_diff_mm'] = timestamp['Northing_diff_mm']
calc['Easting_diff_mm'] = timestamp['Easting_diff_mm']
calc['Elevation_diff_mm'] = timestamp['Elevation_diff_mm']
# Read in the data to make sure these columns have populated
calc.head()


# Step 3: Convert the latitude difference into degrees.
#     

# In[19]:


# First, we need to create constant values with numbers used in further calculations as conversion factors
# 1 degree latitude in meters
deg_lat_m = 111111
# The latitude used
Lat_used =  45.83505277 
# 1 degree longitude in meters
deg_lon_m = 77414


# In[14]:


# We first need to make sure the northing and easting differences are changed to a type int, so that wer can do our
# further calculations on the values.
calc['Northing_diff_mm'] = calc['Northing_diff_mm'].astype(int)
calc['Easting_diff_mm'] = calc['Easting_diff_mm'].astype(int)
calc['Elevation_diff_mm'] = calc['Elevation_diff_mm'].astype(int)


# In[21]:


# This code calculates the latitude difference in degrees for this dataset. 
calc['Lat_Diff_deg'] = calc['Northing_diff_mm']/1000/deg_lat_m
# The longitude difference in degrees
calc['Lon_Diff_deg'] = calc['Easting_diff_mm']/1000/ deg_lon_m
# The elevation difference in meters
calc['El_diff_m'] = calc['Elevation_diff_mm']/1000
# Call the head of the dataframe to make sure these calculations were done correctly
calc.head()


# Step 4: Calculate the closest latitude. To do this, we first need to calculate the timestamp that is closest.

# In[25]:


# First lets add a column in the RTKLIB data to populate out the timestamps.
# Set a record in case we mess up this data
RTKLIB = RTKLIB_record


# Please note that this code is still in process!! This code does a good job of populating the new lat, lon, and elevation data based on the observed differences, but work is still needed! That is why there are still columns that have not populated, columns that will create calculations that are even more accurate for the UAV! For now, this code may suffice, but I would like to improve it in the future. 

# In[31]:


calc['New_Lat'] = timestamp['Lat'] + calc['Lat_Diff_deg']
calc['New_Lon'] = timestamp['Lon'] + calc['Lon_Diff_deg']
calc['New_El'] = timestamp['Height_m'] + calc['El_diff_m']
calc


# Step 5: Create a file to export for image processing.

# In[38]:


# Create a new file dataframe structure for export
export = pd.DataFrame(columns = ['New_Lat', 'New_Lon', 'New_El'])
export


# In[41]:


# Populate the columns based on the calc dataframe
export['New_Lat'] = calc['New_Lat']
export['New_Lon'] = calc['New_Lon']
export['New_El'] = calc['New_El']
export


# In[42]:


# Now export the data for further processing!!!
export.to_csv(r'/Users/f67f911/Desktop/HG2022_Data/corrected_gps.csv')

