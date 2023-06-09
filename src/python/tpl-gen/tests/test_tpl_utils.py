import json
import yaml
import pytest
from pathlib import Path
from unittest.mock import patch, mock_open
from utils.tpl_utils import read_config_file


def test_read_json_file():
    file_path = Path("/path/to/config.json")
    expected_dict = {"key": "value"}
    mock_json_file = mock_open(read_data=json.dumps(expected_dict))
    with patch("builtins.open", mock_json_file):
        result = read_config_file(file_path)
        assert result == expected_dict


def test_read_yaml_file():
    file_path = Path("/path/to/config.yaml")
    expected_dict = {"key": "value"}
    mock_yaml_file = mock_open(read_data=yaml.dump(expected_dict))
    with patch("builtins.open", mock_yaml_file):
        result = read_config_file(file_path)
        assert result == expected_dict


def test_file_not_found_error():
    file_path = Path("/path/to/config.txt")
    with patch("builtins.open", side_effect=FileNotFoundError()):
        with pytest.raises(FileNotFoundError):
            read_config_file(file_path)
