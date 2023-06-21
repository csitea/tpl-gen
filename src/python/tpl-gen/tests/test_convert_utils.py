# from unittest.mock import patch
# from pathlib import Path
# import pytest
# from tpl_gen.lib.utils.convert_utils import create_tgt_path



# @pytest.mark.parametrize(
#     "file_path, opt_dict, env_vars, expected",
#     [
#         (Path("/src/tpl/test.tpl"), {}, {}, Path("/test")),
#         (Path("/src/tpl/test"), {}, {}, Path("/test")),
#         (Path("/src/tpl/%org%/test.tpl"), {"org": "myorg"}, {}, Path("/myorg/test")),
#         (
#             Path("/src/tpl/%org%/test.tpl"),
#             {"org": "otherorg"},
#             {"org": "myorg"},
#             Path("/myorg/test"),
#         ),
#     ],
# )
# def test_create_tgt_path(monkeypatch, file_path, opt_dict, env_vars, expected):
#     # Patching the environment variables
#     # Those sets here are to emulate our taking the env
#     # vars with higher precedence over the opt vars
#     # TODO this test should be improved this is a hack
#     for key, value in opt_dict.items():
#         monkeypatch.setenv(key, value)

#     for key, value in env_vars.items():
#         monkeypatch.setenv(key, value)

#     from tpl_gen.config import env_params_tpl as env
#     #env.init_env()

#     with patch("utils.env_utils.get_env_as_dict_lower", return_value=env_vars), patch(
#         "utils.string_utils.pkey_replace",
#         side_effect=lambda x, y: x.replace("%org%", y.get("org", "")),
#     ):
#         result = create_tgt_path(file_path, opt_dict)
#         assert result == expected
