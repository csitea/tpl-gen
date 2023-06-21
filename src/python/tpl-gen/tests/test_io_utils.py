import pytest
import os
import tempfile
from tpl_gen.libs.utils.io_utils import list_files_and_dirs  # Assuming your function is in `your_module`
#from ..libs.utils.env_utils import *

def test_list_files_and_dirs():
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create dummy files and directories
        os.mkdir(os.path.join(tmpdir, "subdir"))
        with open(os.path.join(tmpdir, "file1.txt"), "w") as f:
            f.write("Test")
        with open(os.path.join(tmpdir, "file2.txt"), "w") as f:
            f.write("Test")

        # Test directory case
        dir_result = list_files_and_dirs(tmpdir)
        assert sorted(dir_result) == sorted([
            os.path.join(tmpdir, "file1.txt"),
            os.path.join(tmpdir, "file2.txt"),
            os.path.join(tmpdir, "subdir")
        ])

        # Test glob case
        glob_result = list_files_and_dirs(os.path.join(tmpdir, "*.txt"))
        assert sorted(glob_result) == sorted([
            os.path.join(tmpdir, "file1.txt"),
            os.path.join(tmpdir, "file2.txt")
        ])
