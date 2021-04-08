# Smart Meter Data Analysis

## Introduction

This project explores the correlation between electricity consumption and customer groups as well as different weather parameters, based on 2013 London smart meter database extracted from [London Datastore](https://data.london.gov.uk/dataset/smartmeter-energy-use-data-in-london-households) and UK weather data extracted from [Renewables Ninja](https://www.renewables.ninja/).

### Datasets
* [2013 London smart meter database](https://data.london.gov.uk/download/smartmeter-energy-use-data-in-london-households/3527bf39-d93e-4071-8451-df2ade1ea4f2/Power-Networks-LCL-June2015(withAcornGps) (765.12 MB, unzipped 11.3GB)
* [Renewables Ninja UK weather data](https://www.renewables.ninja/country_downloads/GB/ninja_weather_country_GB_merra-2_land_area_weighted.csv) (22.36 MB)

**Description:**
The London smart meter dataset contains energy consumption, in kWh (per half hour), unique household identifier, date and time, and CACI Acorn group. The CSV file is around 10GB when unzipped and contains around 167million rows. More information can be found on the [Low Carbon London](https://innovation.ukpowernetworks.co.uk/) webpage

The Renewables Ninja weather dataset contains hourly weather data within Great Britain, including temperature, precipitation, snowfall, etc. More information can be found on Renewable Ninja's [documentation](https://www.renewables.ninja/documentation).

**London smart meter dataset variables:**
1. **LCLid:** Unique household identifier representing one smart meter unit
1. **stdorToU:** Mode of energy pricing: dynamic or standard Time of Use (ToU)
1. **DateTime:** Date and time at half-hourly interval
1. **KWH/hh (per half hour):** Energy consumption, in kWh (per half hour)
1. **Acorn_grouped:** Grouped category of CACI Acorn group

**Renewable Ninja UK weather dataset variables:*
1. **time:**: Date and time in UTC at hourly level
1. **temperature:** Temperature at 2 meters above ground in degrees Celsius
1. **precipitation:** 
1. **irradiance_surface:** Irradiance at ground level in W/m^2 
1. **irradiance_toa:** Irradiance at top of atmosphere in W/m^2 
1. **snowfall:** Snowfall in mm/hour
1. **snow_mass:** Snow mass in kg/m^2
1. **cloud_cover:** Cloud cover as a fraction [0,1]
1. **air_density:** Air density at ground level in kg/m^3

**Additional features created:**
1. **Month:** Month of DateTime
1. **Weekday:** Weekday of DateTime
1. **Hour:** Hour of DateTime

## Analysis
1. **Loading data and save as pickle:** Loading both London smart meter database and Renewable Ninja weather data. For smart meter database, a feature is created to reduce sample size due to exceptionally large size. The model will first try to load any pickle saved in the data folder to save time. If no pickle file is found, it will load the raw data and save a pickle version for the future. 

1. **Splitting train and test sets:** Splitting dataset into two sets: training and testing, with a 20:80 split. Stratified train-test split is used to ensure a consistent distribution of Acorn group. 

1. **Data cleaning:** Removing unnecessary columns, such as "Acorn", renaming variables (e.g. "KWH/hh (per half hour)" to "Consumption"), resampling DateTime to become hourly data, converting variables to the correct data type (e.g. DateTime as DateTime type)

1. **Feature creation:** Creating new and relevant features from DateTime: Month, hour and weekday, given basic understanding of factors affecting consumptions

1. **Data pre-processing:** Applying imputation on missing data, feature scaling on numerical data (Precipitation, snowfall, etc) and OneHot encoding on categorical data (e.g. Acorn_grouped, Month, weekday, hour, etc). This is currently done in Jupyter Notebook as a transformation pipeline.

1. **Dimension reduction:** Variables such as snow fall vs snow mass, irradiance_toa vs irradiance_surface might exhibit covariance. Dimension reduction process such as PCA or factor analysis will be used to improve predictive power of model.

1. **Training and selection model:** Linear regression, decision tree regression and random forest regression will be trained and compared by looking at the RMSE through 10-fold cross-validation. This is currently done in Jupyter Notebook. 

1. **Visualisation:** Results visualised with plots such as feature importance, tree plot, feature contribution to each Acorn group, etc. 

## About this repository
* **src:** Folder of all source codes
 * **run_model.py:** Main script to call other module functions
 * **config.py:** Script to specify all configurations, mostly folder and file directories for now, but will include model parameters in the next updates
 * **data:** Folder containing all data-related scripts
   * **database.py:** Script to load smart meter and weather database, with functions to reformat dataset and reduce sample size
   * **preprocessing.py:** Script to preprocess data, including DateTime resampling and later numerical/categorical data transformation   
   * **split_train_test_sets.py:** Perform train-test-split
 * **features:** Folder containing all feature-related scripts
   * **features.py:** create time features (month, hour and weekday) and join weather feature from the weather database (temperature, precipitation, irradiance, snowfall, snow mass, cloud cover and air density)
 * **models:** Folder containing all model-related scripts
  * **model.py:** Empty for now, but later will be updated with the analysis process in the Jupyter Notebook.
* **Notebook:** Folder containing all data exploration/analysis/visualisation Jupyter Notebook files

## Data visualisation
(to be updated)
