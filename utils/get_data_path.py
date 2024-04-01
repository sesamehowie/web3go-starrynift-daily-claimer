import os


def get_data_path(base_path):
    data_dir = os.path.join(base_path, "data" + os.sep)
    return data_dir
