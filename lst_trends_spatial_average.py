
import ee
import time

start_time = time.perf_counter()

# Initialize the Earth Engine module.
ee.Initialize(project='corvus-phenology-drylands')

# Print metadata for a DEM dataset.
print(ee.Image('USGS/SRTMGL1_003'))

print('')

# Target point 
target_point = ee.Geometry.Point(-115, 33)

# New dataset
lst_test = ee.ImageCollection('MODIS/061/MOD21A1D').filterBounds(target_point).filterDate(ee.Date("2020-05-01"), ee.Date("2020-05-31"))
print(lst_test.getInfo())
print(lst_test.first().getInfo())

before_resampling_time = time.perf_counter()

print('\nup until here, it has taken about ', before_resampling_time - start_time, " seconds\n")

lst_sample_first = lst_test.first().sample(target_point, 1000).get('LST_1KM').getInfo()
first_sample_time = time.perf_counter()

print(lst_sample_first)
print('\nGetting first sample took ', first_sample_time - before_resampling_time, " seconds\n")

lst_sample_mean_1 = lst_test.mean().sample(target_point, 1000).first().get('LST_1KM').getInfo()
mean_1_sample_time = time.perf_counter()

print(lst_sample_mean_1)
print('\nGetting first sample took ', mean_1_sample_time - first_sample_time, " seconds\n")

print(lst_test.mean().sample(target_point, 1000).size().getInfo())
print(lst_test.mean().sample(target_point, 1000).first().getInfo())