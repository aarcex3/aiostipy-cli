import os
import shutil

import pytest
from click.testing import CliRunner

from src.main import cli


@pytest.fixture
def runner():
    """Fixture to provide a Click testing runner."""
    return CliRunner()


def test_create_controller(runner: CliRunner):
    controller_name = "user"
    folder_name = controller_name
    controller_file = f"{controller_name}_controller.py"
    file_path = os.path.join(folder_name, controller_file)

    # Helper function to clean up the file and folder
    def cleanup():
        if os.path.exists(file_path):
            os.remove(file_path)
        if os.path.exists(folder_name):
            shutil.rmtree(folder_name)

    # Ensure the folder and file do not exist before the test
    cleanup()

    try:
        # Invoke the CLI command to create the controller file
        result = runner.invoke(cli, ["generate", "controller", controller_name])

        # Assertions
        assert (
            result.exit_code == 0
        ), f"Command failed with exit code {result.exit_code}"
        assert os.path.exists(file_path), f"File '{file_path}' was not created."

        with open(file_path, "r") as f:
            content = f.read()

        # Define expected content based on the plain controller example
        expected_content = f"""from aiostipy.common import Controller\nclass {controller_name.title()}Controller(Controller):\n\tpass"""
        assert content.strip() == expected_content.strip(), (
            f"File content does not match expected content.\n"
            f"Expected: '{expected_content}'\n"
            f"Found: '{content}'"
        )

    finally:
        # Clean up: Remove the file and folder after the test
        cleanup()
