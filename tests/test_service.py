import os
import shutil

import pytest
from click.testing import CliRunner

from src.main import cli


@pytest.fixture
def runner():
    """Fixture to provide a Click testing runner."""
    return CliRunner()


def test_create_service(runner: CliRunner):
    service_name = "user"
    folder_name = service_name
    service_file = f"{service_name}_service.py"
    file_path = os.path.join(folder_name, service_file)

    # Helper function to clean up the file and folder
    def cleanup():
        if os.path.exists(file_path):
            os.remove(file_path)
        if os.path.exists(folder_name):
            shutil.rmtree(folder_name)

    # Ensure the folder and file do not exist before the test
    cleanup()

    try:
        # Invoke the CLI command to create the service file
        result = runner.invoke(cli, ["generate", "service", service_name])

        # Assertions
        assert result.exit_code == 0
        assert os.path.exists(file_path) == True

        with open(file_path, "r") as f:
            content = f.read()

        # Define expected content based on the plain service example
        expected_content = f"""from aiostipy.common import Service\n\nclass {service_name.title()}Service(Service):\n\tpass"""
        assert content.strip() == expected_content.strip(), (
            f"File content does not match expected content.\n"
            f"Expected: '{expected_content}'\n"
            f"Found: '{content}'"
        )

    finally:
        # Clean up: Remove the file and folder after the test
        cleanup()
