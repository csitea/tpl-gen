import os
import glob

def list_files_and_dirs(path_str):
    if os.path.isdir(path_str):
        return sorted([os.path.join(path_str, f) for f in os.listdir(path_str)])
    else:
        return sorted(glob.glob(path_str))
