from modules.types.enums import Technologies

ProjectInitializationCommands: dict[str, str] = {
    Technologies.NodeJS.value: "npm init -y",
    Technologies.PYTHON_UV.value: "uv init",
    Technologies.PYTHON.value: "python3 -m venv .venv",
}

PackageInstallationCommands: dict[str, str] = {
    Technologies.NodeJS.value: "npm install {packages}",
    Technologies.PYTHON_UV.value: "uv add {packages}",
    Technologies.PYTHON.value: ".venv/bin/python -m pip install {packages}",
}