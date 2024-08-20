import os
import shutil

import pytest
from click.testing import CliRunner

from src.main import cli


@pytest.fixture
def runner():
    """Fixture to provide a Click testing runner."""
    return CliRunner()


def test_create_module(runner: CliRunner):
    module_name = "user"
    folder_name = module_name
    module_file = f"{module_name}_module.py"
    file_path = os.path.join(folder_name, module_file)

    # Helper function to clean up the file and folder
    def cleanup():
        if os.path.exists(file_path):
            os.remove(file_path)
        if os.path.exists(folder_name):
            shutil.rmtree(folder_name)

    # Ensure the folder and file do not exist before the test
    cleanup()

    try:
        # Invoke the CLI command to create the module file
        result = runner.invoke(cli, ["generate", "module", module_name])

        # Assertions
        assert (
            result.exit_code == 0
        ), f"Command failed with exit code {result.exit_code}"
        assert os.path.exists(file_path), f"File '{file_path}' was not created."

        with open(file_path, "r") as f:
            content = f.read()

        # Define expected content based on the plain module example
        expected_content = f"""from src.{module_name} import {module_name.title()}Controller, {module_name.title()}Service\nfrom aiostipy.common import Module\nclass {module_name.title()}Module(Module):\n\tcontrollers = [{module_name.title()}Controller]\n\tservices = [{module_name.title()}Service]\n\tpass
""".strip()
        assert content.strip() == expected_content.strip(), (
            f"File content does not match expected content.\n"
            f"Expected: '{expected_content}'\n"
            f"Found: '{content}'"
        )

    finally:
        # Clean up: Remove the file and folder after the test
        cleanup()
