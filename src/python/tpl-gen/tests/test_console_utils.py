import tpl_gen.lib.utils.console_utils as cw


def test_print_functions(capsys):
    msg = "Test message"

    # Testing print functions that don't throw errors
    functions_to_test = [cw.print_warn, cw.print_success, cw.print_info, cw.print_error]

    for function in functions_to_test:
        function(msg)
        captured = capsys.readouterr()
        assert msg in captured.out


def test_print_info_heading(capsys):
    heading = "Test Heading"
    cw.print_info_heading(heading)
    captured = capsys.readouterr()
    assert heading in captured.out
