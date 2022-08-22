#!/usr/bin/env python
# coding: utf-8

# This code should be used to clean up weather station data for the Hourglass Field Site. This code was developed by Madeline Beck on 04/05/2022

# In[1]:


# Import the packages needed to run this code.
# Import numerical tools
import numpy as np
# Import pyplot for plotting
import matplotlib.pyplot as plt
#Import pandas for reading in and managing data
import pandas as pd
import math
# Import seaborn for plotting purposes
import seaborn as sns
# Magic function to make matplotlib inline; other style specs must come AFTER
get_ipython().run_line_magic('matplotlib', 'inline')
get_ipython().run_line_magic('config', "InlineBackend.figure_formats = {'svg',}")
#Comment the above line and uncomment the line below if svg graphics are not working in your browser.
#%config InlineBackend.figure_formats = {'png', 'retina'}


# Step 1: Read in Hourly data from the Automated Weather Station.

# In[3]:


# Read in the ASW Hourly data. 
# Note that data must be first cleaned in Excel before uploading. This is because the Campbell Data Logger exports a 
# .dat file that is difficult to read in correctly in python. Therefore, simply copy and paste the .dat data into a 
# new Excel file and save as a csv.

# Note that I would like to automate this step in the future, but for now, the data must be first cleaned before it 
# can be read into python

# Read in the csv from the path on your computer
hg_hourly_record = pd.read_csv('/Users/f67f911/Desktop/HG2022_Data/Hourglass_Hourly_Cleaned.csv')
# Read the head of the data to make sure that is has been read in correctly. If it has not, you will have extra rows 
# before the data, your TIMESTAMP column will not be considered a header, or you will not have header data at all.
# Check this step before moving on.
hg_hourly_record.head()


# In[5]:


# Save a version of your data in case you mess up later. This will allow you to just run this line of code to reset 
# your dataframe in case of a mistake
hg_hourly = hg_hourly_record


# Step 2: Clean up the weather station data. 
# 
# Let's start by cleaning up our data. For purposes of this project, we do not need all of the data columns that were created by the Campbell program. 

# In[6]:


# We can read in all of the column names. This will make it so we are less likely to make typos when dropping columns
hg_hourly.columns


# In[7]:


# Let's drop the record row to start out with to make sure it works
hg_hourly = hg_hourly.drop(['RECORD'], axis = 1)
# Check to make sure the data still looks correct
hg_hourly.head()


# In[8]:


# Looks good. Let's start dropping other miscellaneous columns. Note that there columns still contain important 
# information, I just do not need them for this code and would therefore like to leave them out
hg_hourly = hg_hourly.drop(['Q','WS_ms_Max', 'WS_ms_S_WVT', 'WindDir_D1_WVT', 'WindDir_SD1_WVT','T109_C_Avg',
                            'BP_mmHg','CNR4TC', 'CNR4TK','RsNet', 'RlNet','Rn', 'LUpCo', 'LDnCo'], axis = 1)


# In[9]:


# Again, check the data to make sure it looks correct. If it does, move on.
hg_hourly.head()


# In[10]:


# Further clean up the data. Give the columns names that are a bit more intuitive and that will help with further 
# analysis

hg_hourly = hg_hourly.rename({
    'AirTC':'AirTempC',
    'AirTC_Avg':'Avg_AirTemp',
    # skipping RH, snowdepth, just adding a note in case an error occurs later
    # more column names will be added once I figure out what each of the variables stand for
    'SUp': 'Incoming_Shortwave',
    'SDn': 'Outgoing_Shortwave',
    'LUp': 'Incoming_Longwave',
    'LDn': 'Outgoing_Longwave'
    
},
    axis = 1
)
hg_hourly.columns


# In[11]:


# Clean up the timestamp data to get it into a useable format. This will allow us to filter by timestamp data in 
# future steps
hg_hourly['TIMESTAMP'] =  pd.to_datetime(hg_hourly['TIMESTAMP'])#, format='%m/%d/%Y %M:%S')
hg_hourly = hg_hourly.set_index(['TIMESTAMP'])
# Check to make sure that TIMESTAMP data is now in a DateTime format
hg_hourly.head()


# In[12]:


# Unfortunately, the way our data is read in, some of the values are seen as objects and not as float numbers. We 
# therefore need to change this or we cannot do calculations on our data. 
# See what datatype we have in our dataframe right now.
hg_hourly.dtypes


# In[13]:


# We need to set the temperature data and all of the Incoming and Outgoing variables to float variables
# Note that a loop would make this step a lot better, I would like to fix this in the future and make the code more 
# automated, especially if for any reason the data being read in from the Campbell datalogger has different column names
hg_hourly['AirTempC'] = hg_hourly['AirTempC'].astype(float)
hg_hourly['Avg_AirTemp'] = hg_hourly['Avg_AirTemp'].astype(float)
hg_hourly['SnowDepth'] = hg_hourly['SnowDepth'].astype(float)
hg_hourly['Incoming_Shortwave'] = hg_hourly['Incoming_Shortwave'].astype(float)
hg_hourly['Outgoing_Shortwave'] = hg_hourly['Outgoing_Shortwave'].astype(float)
hg_hourly['Incoming_Longwave'] = hg_hourly['Incoming_Longwave'].astype(float)
hg_hourly['Outgoing_Longwave'] = hg_hourly['Outgoing_Longwave'].astype(float)We are done cleaning up the dataframe for now. The next step is to add a few columns for our albedo measurements. It is important to note that we already have a column named albedo, however, the way that the sensor works on the datalogger, we have both shortwave and longwave albedo (at least I think so). Since we have different bands that we are able to calculate, we should add in new columns for these variables.


# We are done cleaning up the dataframe for now. The next step is to add a few columns for our albedo measurements. It is important to note that we already have a column named albedo, however, the way that the sensor works on the datalogger, we have both shortwave and longwave albedo (at least I think so). Since we have different bands that we are able to calculate, we should add in new columns for these variables.

# In[14]:


# Add a column for albedo that is equal to the relationship between incoming and outgoing shortwave and longwave 
# radiation
# Make sure to set this as an object. For our next step of filtering data, we need to have this requirement
hg_hourly['Shortwave_Albedo'] = hg_hourly.Outgoing_Shortwave.div(hg_hourly.Incoming_Shortwave).astype(object)
hg_hourly['Longwave_Albedo'] = hg_hourly.Outgoing_Longwave.div(hg_hourly.Incoming_Longwave).astype(object)


# In[15]:


# Look at the data again. Make sure the new columns have been added and that values have been correctly updated.
# Note that the 'Shortwave_Albedo' column should be very similar to 'Albedo'. If this is not the case, make sure you 
# have names your variables correctly and done the correct calculations.
hg_hourly.head()


# In[16]:


# We still need to clean up the data. We can tell this because Albedo, by definition, is a ratio between incoming and
# outgoing radiation. New snow is known to have a value around 0.9, and ground a value of 0.2. This means that incoming
# radiation, by definition, will always be greater than outgoing since a perfect reflector would have a value of 1. 
# We therefore need to make sure the data is only showing data is between 0 - 1.

# I have changed this code a bit to make it so all values equal to 1 and 0 are also set to NAN. This is because it is 
# a fair assumption in this environment that nothing will be a perfect reflector and nothing will be a perfect absorber.
hg_hourly[(hg_hourly.Shortwave_Albedo >= 1)] = np.nan # sets all values greater than 1 to a NaN
hg_hourly[(hg_hourly.Shortwave_Albedo <= 0)] = np.nan # sets all values greater than 1 to a NaN


# In[17]:


# Look at the 'Shortwave_Albedo' data to make sure the values that do not fit this criteria are set to nan

hg_hourly['Shortwave_Albedo'].head()


# In[18]:


# Do the same for the Longwave Albedo
hg_hourly[(hg_hourly.Longwave_Albedo >= 1)] = np.nan # sets all values greater than 1 to a NaN
hg_hourly[(hg_hourly.Longwave_Albedo <= 0)] = np.nan # sets all values greater than 1 to a NaN


# In[19]:


hg_hourly['Longwave_Albedo'].head()


# Step 3: Begin to graph out the albedo data, now that we have set all incorrect values to nan for the dataset.

# In[20]:


# Use seaborn (sns) for the graphics.
sns.set_theme(style="whitegrid")
sns.set(rc = {'figure.figsize':(15,8)}) # This will make them larger.

# Plot the data points for each albedo measurement.
sns.scatterplot(x="TIMESTAMP", y="Shortwave_Albedo", data=hg_hourly)


# The scatter plot above is VERY noisy and hard to identify any trends. We can filter it to look at just the ablation period (after April 1st which is assumed to be when peak SWE occurs.
# * Note that I can change this value if Peak SWE is observed at a different time of year. This will likely be important in the 2021-2022 winter when peak SWE was likely observed on April 1st (and may have been later due to the high amounts of snow received in May). 

# In[21]:


# Look at the data from April 1st to June 24th when the last UAV flight of the area was done. Set these dates 
# based on the time period you would like to observe by.
hg_hourly_melt = hg_hourly.loc['2021-04-01':'2021-06-24']


# In[22]:


# Plot the data points for each albedo measurement.
sns.scatterplot(x="TIMESTAMP", y="Shortwave_Albedo", data=hg_hourly_melt)


# That is looking a bit better and becoming evident that the data is a bit more clustered, but has lots of outliers. We can clean this up a bit further.

# In[23]:


# Let's look at the standard deviation of the data. We will assume that anything outside of 1 SD away from the mean is 
# an outlier and can therefore be ignored.
Shortwave_Albedo_Mean = hg_hourly_melt['Shortwave_Albedo'].mean()
Shortwave_Albedo_SD = hg_hourly_melt['Shortwave_Albedo'].std()
print("Mean = " + str(Shortwave_Albedo_Mean))
print("Standard Deviation = " + str(Shortwave_Albedo_SD))


# We have been looking at the albedo values. Let's change that to start looking at air temperature.

# In[24]:


# Plot temperature data to see how this data changes over time during the melt cycle.
sns.scatterplot(x="TIMESTAMP", y="Avg_AirTemp", data=hg_hourly_melt)


# This data is quite messy. Let's instead work with the daily data. Hourly data may be beneficial to have later on, but for now it is difficult to make assumptions when using.

# In[26]:


# At this step, I would either upload the data from the daily.dat file, but since that was cumbersome to get into a 
# workable format, I am instead just going to work with the hourly data.
hg_daily = hg_hourly.resample('D').mean()
hg_daily


# In[27]:


# For some reason, it deleted all of my calculated shortwave albedo and longwave albedo calculations. I will redo 
# that here
hg_daily['Shortwave_Albedo'] = hg_daily.Outgoing_Shortwave.div(hg_daily.Incoming_Shortwave).astype(object)
hg_daily['Longwave_Albedo'] = hg_daily.Outgoing_Longwave.div(hg_daily.Incoming_Longwave).astype(object)

# Again, it did not filter out the > 1 and < 0 data, so I will do that now
hg_daily[(hg_daily.Shortwave_Albedo > 1)] = np.nan # sets all values greater than 1 to a NaN
hg_daily[(hg_daily.Shortwave_Albedo < 0)] = np.nan # sets all values greater than 1 to a NaN


hg_daily[(hg_daily.Longwave_Albedo > 1)] = np.nan # sets all values greater than 1 to a NaN
hg_daily[(hg_daily.Longwave_Albedo < 0)] = np.nan # sets all values greater than 1 to a NaN


# In[28]:


# Check the data to make sure we have correctly read in the values
hg_daily.head()


# In[29]:


# Let's graph the temperature data for the entire period of record.
sns.scatterplot(x="TIMESTAMP", y="Avg_AirTemp", data=hg_daily)


# In[30]:


# Again, we can subset the data by the melt period
# Set the data filter range to just look at the 2021 melt cycle
hg_daily_melt = hg_daily.loc['2021-04-01':'2021-06-24']


# In[32]:


# Plot with a lineplot to observe trends
sns.lineplot(x="TIMESTAMP", y="Avg_AirTemp", data=hg_daily_melt)


# The albedo appears to have stayed quite high until the end of May. I am curious of the characteristics of this period as this is when the greatest amount of change was observed for Albedo. Will this be the same case for air temperature? For snowdepth?

# In[33]:


# Create a variable for the data in the increased melt period
hg_daily_increased_melt = hg_daily_melt.loc['20210520':'20210610']


# In[34]:


# Plot the albedo for that period to zoom in.
sns.lineplot(x="TIMESTAMP", y="Shortwave_Albedo", data=hg_daily_increased_melt)


# In[36]:


# Now let's look at snowdepth
sns.lineplot(x="TIMESTAMP", y="SnowDepth", data=hg_daily_increased_melt)


# With this data, we can now begin to analyze trends in the meteorological variables over different time periods to start to understand what may be the largest driving forces for snow depth change at the weather station. These cleaned datasets will be integral to begin to model for Snow Water Equivalent at the field site, and then further to use these observations to extrapolate to the entire field site.
# 
# It is important to note that with this code, many more graphs can be created using seaborn. Refer to this documentation to make such graphs: https://seaborn.pydata.org/
# 

# In[37]:


fig, ax = plt.subplots(figsize=(10,6))
color = 'tab:green'
ax.set_title('Air Temperature and Snowdepth During Ablation Cycle', fontsize=16)
ax = sns.lineplot(x = 'TIMESTAMP', y = 'AirTempC', data = hg_daily_melt, color = '#69d', legend = True)
ax.grid(False)
ax2 = ax.twinx()
sns.lineplot(x = 'TIMESTAMP', y = 'SnowDepth', data = hg_daily_melt, color = 'seagreen', legend = True)
ax2.grid(False)

