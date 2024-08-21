import os
import shutil
from typing import List

import pytest
from click.testing import CliRunner

from aiostipy_cli.main import cli


def create_folder_safely(resource_name: str):
    """Ensure the folder does not exist before the test starts."""
    if os.path.exists(resource_name):
        shutil.rmtree(resource_name)


def check_files_and_content(resource_name: str, files: List[str], contents: List[str]):
    """Check if the required files exist in the folder and validate their content."""
    for file, content in zip(files, contents):
        file_path = os.path.join(resource_name, file)
        assert os.path.isfile(file_path), f"File '{file_path}' was not found."
        with open(file_path, "r") as f:
            file_content = f.read().strip()
            assert (
                file_content == content
            ), f"File '{file_path}' does not contain expected content."


@pytest.fixture
def runner():
    """Fixture to provide a click testing runner."""
    return CliRunner()


def test_create_resource(runner: CliRunner):
    """Test the creation of a resource folder and the necessary files."""
    resource_name = "user"
    files = [
        f"{resource_name}_controller.py",
        f"{resource_name}_service.py",
        f"{resource_name}_module.py",
    ]
    contents = [
        f"""from aiostipy.common import Controller\n\nclass {resource_name.title()}Controller(Controller):\n\tpass
""".strip(),
        f"""from aiostipy.common import Service\n\nclass {resource_name.title()}Service(Service):\n\tpass
""".strip(),
        f"""from .{resource_name}_controller import {resource_name.title()}Controller\nfrom .{resource_name}_service import {resource_name.title()}Service\nfrom aiostipy.common import Module\n\nclass {resource_name.title()}Module(Module):\n\tcontrollers = [{resource_name.title()}Controller]\n\tservices = [{resource_name.title()}Service]\n\tpass
""".strip(),
    ]

    create_folder_safely(resource_name)

    try:
        # Invoke the CLI command
        result = runner.invoke(cli, ["generate", "resource", resource_name])

        # Assertions
        assert (
            result.exit_code == 0
        ), f"Command failed with exit code {result.exit_code}"
        assert os.path.exists(
            resource_name
        ), f"Folder '{resource_name}' was not created."
        assert f"Folder '{resource_name}' created" in result.output.strip()

        check_files_and_content(resource_name, files, contents)

    finally:
        # Clean up: Remove the folder after the test
        if os.path.exists(resource_name):
            shutil.rmtree(resource_name)


def test_resource_exists(runner: CliRunner):
    """Test if the command handles already existing folders properly."""
    resource_name = "user"
    resource_path = os.path.join(os.getcwd(), resource_name)

    # Ensure the folder exists
    os.makedirs(resource_path, exist_ok=True)

    try:
        result = runner.invoke(cli, ["generate", "resource", resource_name])
        assert (
            result.exit_code == 0
        ), f"Command failed with exit code {result.exit_code}"
        assert f"Folder '{resource_name}' already exists!" in result.output.strip()

    finally:
        shutil.rmtree(resource_name)
