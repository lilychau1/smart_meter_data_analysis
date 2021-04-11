from sklearn.model_selection import StratifiedShuffleSplit
import config

def stratified_train_test_split(smart_meter_df):

    # Split trin and test set with stratified sampling based on Acorn_grouped to ensure the same distribution of acron groups
    split = StratifiedShuffleSplit(n_splits=1, test_size=config.test_set_size, random_state=42)
    for train_index, test_index in split.split(smart_meter_df, smart_meter_df["Acorn_grouped"]):
        strat_train_set = smart_meter_df.loc[train_index]
        strat_test_set = smart_meter_df.loc[test_index]

    return strat_train_set, strat_test_set

