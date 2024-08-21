# Aiostipy CLI

Welcome to the CLI for [aiostipy](https://github.com/aarcex3/aiostipy)!\
This command-line interface allows you to quickly generate code components for your aiostipy projects.

## Installation

To use the `aiostipy` CLI, you need to have `aiostipy` installed. You can install it via pip:

```bash
pip install aiostipy
```

## Usage

### New project

```bash
aiostipy new project_name
```

Genereates the following:

```bash
project_name/
├── src/
│   ├── __init__.py
│   ├── app_module.py
│   ├── app_controller.py
│   ├── app_service.py
├── main.py
└── README.md
```

To add components you can use the following:

```bash
aiostipy generate [controller|service|module|resource] resource_name
```

### Commands

- **controller**: Generates a new controller.
- **service**: Generates a new service.
- **module**: Generates a new module.
- **resource**: Generates a new resource.

## License

This project is licensed under the MIT License. See the LICENSEfile for details.
