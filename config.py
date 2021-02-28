import os
import tarfile
import urllib

file_path = os.path.dirname(os.path.abspath(__file__))

# Configure folder locations for database and results
database_folder = os.path.abspath(os.path.join(file_path, "./data/"))
results_folder = os.path.abspath(os.path.join(file_path, "./results/"))

# Configure paths for smart meter dataset and temperature dataset
smart_meter_data_path = database_folder + "/london_smart_meter_data_2013.csv"
temperature_data_path = database_folder + "/temperature_uk.csv"