import os
import shutil

import pytest
from click.testing import CliRunner

from aiostipy_cli.main import (
    cli,
)  # Ensure this path is correct based on your project structure


@pytest.fixture
def runner():
    """Fixture to provide a Click testing runner."""
    return CliRunner()


def test_new_app(runner: CliRunner):
    project_name = "new_project"

    # Invoke the command with the given project name
    result = runner.invoke(cli, ["new", project_name])

    # Ensure the command exits with a code of 0 (success)
    assert result.exit_code == 0

    # Check if the main project directory was created
    assert os.path.exists(project_name)

    # Define expected file contents based on the provided file templates
    expected_files = {
        os.path.join(project_name, "README.md"): f"# {project_name}\n",
        os.path.join(
            project_name, "main.py"
        ): """from src.app_module import AppModule\nfrom aiostipy.core import AppFactory, web\n\ndef bootstrap():\n\tapp = AppFactory.create(AppModule)\n\tweb.run_app(app=app, host="0.0.0.0", port=8000)\nif __name__ == "__main__":\n\tbootstrap()
""",
        os.path.join(project_name, "src", "__init__.py"): "",
        os.path.join(
            project_name, "src", "app_module.py"
        ): """from .app_controller import AppController\nfrom .app_service import AppService\nfrom aiostipy.common import Module\n\nclass AppModule(Module):\n\tcontrollers = [AppController]\n\tservices = [AppService]\n\tpass
""",
        os.path.join(
            project_name, "src", "app_controller.py"
        ): """from aiostipy.common import Controller\n\nclass AppController(Controller):\n\tpass
""",
        os.path.join(
            project_name, "src", "app_service.py"
        ): """from aiostipy.common import Service\n\nclass AppService(Service):\n\tpass
""",
    }

    # Verify each file's existence and content
    for file_path, expected_content in expected_files.items():
        assert os.path.exists(file_path), f"{file_path} does not exist"

        with open(file_path, "r") as file:
            content = file.read().strip()
            assert (
                content == expected_content.strip()
            ), f"Content mismatch in {file_path}"

    # Cleanup: remove the created project directory
    if os.path.exists(project_name):
        shutil.rmtree(project_name)
