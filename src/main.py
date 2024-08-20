import os

import click


@click.group()
def cli():
    """Main CLI tool."""
    pass


@cli.group(name="new")
def new():
    pass


@cli.group(name="generate")
def generate():
    """Generate commands."""
    pass


def create_folder_if_not_exists(folder_name: str):
    os.makedirs(folder_name)


def write_file(file_path: str, content: str):
    with open(file_path, "w") as f:
        f.write(content.strip())


def generate_file_content(
    file_type: str, name: str, additional_imports: str = ""
) -> str:
    title_name = name.title()
    if file_type == "controller":
        return f"""from aiostipy.common import Controller\nclass {title_name}Controller(Controller):\n\tpass"""
    elif file_type == "service":
        return f"""from aiostipy.common import Service\nclass {title_name}Service(Service):\n\tpass"""
    elif file_type == "module":
        return f"""from src.{name} import {title_name}Controller, {title_name}Service\nfrom aiostipy.common import Module\nclass {title_name}Module(Module):\n\tcontrollers = [{title_name}Controller]\n\tservices = [{title_name}Service]\n\tpass"""
    return ""


@generate.command(name="resource")
@click.argument("resource_name")
def generate_resource(resource_name: str):
    """
    Generate a resource folder and files.
    RESOURCE_NAME is the name of the folder to be created.
    """
    contents = [
        generate_file_content("controller", resource_name),
        generate_file_content("service", resource_name),
        generate_file_content("module", resource_name),
    ]
    resource_path = os.path.join(os.getcwd(), resource_name)

    try:
        create_folder_if_not_exists(resource_path)
        click.echo(f"Folder '{resource_name}' created")
        files = ["controller.py", "service.py", "module.py"]

        for file, content in zip(files, contents):
            file_name = f"{resource_name}_{file}"
            file_path = os.path.join(resource_path, file_name)
            write_file(file_path, content)
    except FileExistsError:
        click.echo(f"Folder '{resource_name}' already exists!")
    except Exception as e:
        click.echo(f"An error occurred: {e}")


@generate.command(name="controller")
@click.argument("controller_name")
def generate_controller(controller_name: str):
    """
    Generate a controller file.
    CONTROLLER_NAME is the name of the controller to be created.
    """
    folder_name = controller_name.lower()
    file_name = f"{controller_name}_controller.py"
    create_folder_if_not_exists(folder_name)
    file_path = os.path.join(folder_name, file_name)
    content = generate_file_content("controller", controller_name)
    write_file(file_path, content)


@generate.command(name="service")
@click.argument("service_name")
def generate_service(service_name: str):
    """
    Generate a service file.
    SERVICE_NAME is the name of the service to be created.
    """
    folder_name = service_name.lower()
    file_name = f"{service_name}_service.py"
    create_folder_if_not_exists(folder_name)
    file_path = os.path.join(folder_name, file_name)
    content = generate_file_content("service", service_name)
    write_file(file_path, content)


@generate.command(name="module")
@click.argument("module_name")
def generate_module(module_name: str):
    """
    Generate a module file.
    MODULE_NAME is the name of the module to be created.
    """
    folder_name = module_name.lower()
    file_name = f"{module_name}_module.py"
    create_folder_if_not_exists(folder_name)
    file_path = os.path.join(folder_name, file_name)
    content = generate_file_content("module", module_name)
    write_file(file_path, content)


if __name__ == "__main__":
    cli()
