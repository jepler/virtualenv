import pytest

from virtualenv.activation import PythonActivator
from virtualenv.config.cli.parser import VirtualEnvOptions
from virtualenv.discovery.builtin import get_interpreter
from virtualenv.run import session_via_cli


@pytest.mark.skipif(get_interpreter("2.7", []) is None, reason="No 2.7 interpreter installed")
def test_python_activator_cross(session_app_data, cross_python, special_name_dir):
    options = VirtualEnvOptions()
    cli_args = [
        str(special_name_dir),
        "-p",
        str(cross_python.executable),
        "--app-data",
        str(session_app_data.lock.path),
        "--without-pip",
        "--activators",
        "",
    ]
    session = session_via_cli(cli_args, options)
    activator = PythonActivator(options)
    session.creator.bin_dir.mkdir(parents=True)
    results = activator.generate(session.creator)
    assert len(results) == 1
    result = results[0]
    content = result.read_text()
    # check that the repr strings have been correctly stripped
    assert "\"'" not in content
