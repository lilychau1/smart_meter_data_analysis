import os
import tarfile
import urllib

file_path = os.path.dirname(os.path.abspath(__file__))

# Configure folder locations for database and results
raw_database_folder = os.path.abspath(os.path.join(file_path, "../data/raw"))
interim_database_folder = os.path.abspath(os.path.join(file_path, "../data/interim"))
preprocessed_dataset_folder = os.path.abspath(os.path.join(file_path, "../data/preprocessed"))
results_folder = os.path.abspath(os.path.join(file_path, "../results/"))

# Configure paths for smart meter dataset and weather dataset
smart_meter_data_path = raw_database_folder + "/london_smart_meter_data_2013.csv"
weather_data_path = raw_database_folder + "/weather_uk.csv"

smart_meter_data_pickle_path = raw_database_folder + "./smdb_pickle.pkl"
weather_pickle_path = raw_database_folder + "./weatherdb_pickle.pkl"
train_set_pickle_path = interim_database_folder + "./train_pickle.pkl"
test_set_pickle_path = interim_database_folder + "./test_pickle.pkl"
preprossed_train_data_npy_path = preprocessed_dataset_folder+ "./preprocessed_smdb_train_npy.npy"
preprossed_test_data_npy_path = preprocessed_dataset_folder+ "./preprocessed_smdb_test_npy.npy"


# Configure train-test sizes
test_set_size = 0.2