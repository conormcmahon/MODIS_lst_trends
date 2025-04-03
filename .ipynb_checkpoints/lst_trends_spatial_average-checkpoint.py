
import ee
import time
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import PyQt5

start_time = time.perf_counter()

# Initialize the Earth Engine module.
ee.Initialize(project='corvus-phenology-drylands')

# Print metadata for a DEM dataset.
#print(ee.Image('USGS/SRTMGL1_003'))

print('')

# Target point 
target_point = ee.Geometry.Point(-115, 33)

# New dataset
lst_test = ee.ImageCollection('MODIS/061/MOD21A1D').filterBounds(target_point).filterDate(ee.Date("2020-01-01"), ee.Date("2020-12-31"))
#print(lst_test.getInfo())
#print(lst_test.first().getInfo())

before_resampling_time = time.perf_counter()

print('\nLoading libraries and imagery took about ', before_resampling_time - start_time, " seconds\n")

#lst_sample_first = lst_test.first().sample(target_point, 1000).get('LST_1KM').getInfo()
first_sample_time = time.perf_counter()

#print(lst_sample_first)
#print('\nGetting first sample took ', first_sample_time - before_resampling_time, " seconds\n")

lst_sample_mean_1 = lst_test.mean().sample(target_point, 1000).first().get('LST_1KM').getInfo()
mean_1_sample_time = time.perf_counter()

print(lst_sample_mean_1)
print('\nGetting mean sample took ', mean_1_sample_time - first_sample_time, " seconds\n")

print(lst_test.mean().sample(target_point, 1000).size().getInfo())
print(lst_test.mean().sample(target_point, 1000).first().getInfo())

lst_region_test = lst_test.getRegion(target_point, 1000).getInfo()
spatial_sample_time = time.perf_counter()

#print(lst_region_test.shape())
print("\n", lst_region_test[:5], "\n")
print('\nGetting spatial sample took ', spatial_sample_time - mean_1_sample_time, " seconds\n")

def eeArrayToDF(arr, list_of_bands):
    """Transforms client-side ee.Image.getRegion array to pandas.DataFrame."""
    df = pd.DataFrame(arr)

    # Rearrange the header.
    headers = df.iloc[0]
    df = pd.DataFrame(df.values[1:], columns=headers)

    # Remove rows without data inside.
    df = df[['longitude', 'latitude', 'time', *list_of_bands]].dropna()

    # Convert the data to numeric values.
    for band in list_of_bands:
        df[band] = pd.to_numeric(df[band], errors='coerce')

    # Convert the time field into a datetime.
    df['datetime'] = pd.to_datetime(df['time'], unit='ms')

    # Keep the columns of interest.
    df = df[['time','datetime','longitude','latitude',*list_of_bands]]

    return df

lst_df = eeArrayToDF(lst_region_test, ['LST_1KM'])

def tempMODIStoC(temp_modis):
    """Converts MODIS LST units to degrees Celsius."""
    t_celcius = temp_modis - 273.15
    return t_celcius

# Apply the function to get temperature in Celsius
lst_df['LST_1KM'] = lst_df['LST_1KM'].apply(tempMODIStoC)

dataframe_time = time.perf_counter()

print("\n", lst_df.head())
print("\n", lst_df.shape)
print('\nConverting to Dataframe took ', dataframe_time - spatial_sample_time, " seconds\n")

# Extract data
x_data = np.asanyarray(lst_df['time'].apply(float))
y_data = np.asanyarray(lst_df['LST_1KM'].apply(float))

# Subplots
fig, ax = plt.subplots(figsize=(14, 6))

# Add scatter plot
ax.scatter(lst_df['datetime'], lst_df['LST_1KM'], 
           c='black', alpha=0.2, label='Urban (data)')

# Add some parameters
ax.set_title('Daytime Land Surface Temperature in Imperial Valley', fontsize=16)
ax.set_xlabel('Date', fontsize=14)
ax.set_xlabel('Temperature [C]', fontsize=14)
ax.set_ylim(-0, 70)
ax.grid(lw=0.2)

plt.show()
plt.savefig('plot.png')

print("\ngenerated plot")