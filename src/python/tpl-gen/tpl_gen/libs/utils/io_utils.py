import os
import glob

def list_files_and_dirs(path_str):
    if os.path.isdir(path_str):
        files = []
        for dirpath, dirnames, filenames in os.walk(path_str):
            for filename in filenames:
                files.append(os.path.join(dirpath, filename))
        return sorted(files)
    else:
        return sorted(glob.glob(path_str))


def replace_path(src_path, tgt_path):
    # Normalize paths and resolve levels
    src_path = os.path.normpath(src_path)
    tgt_path = os.path.normpath(tgt_path)

    # Count levels in tgt_path
    tgt_levels = len(tgt_path.split(os.sep))

    # Replace the same number of levels in src_path
    src_parts = src_path.split(os.sep)
    replaced_src_path = os.sep.join(src_parts[tgt_levels:])

    # Prepend the tgt_path to the replaced src_path
    final_path = os.path.join(tgt_path, replaced_src_path)

    return final_path
