from modules.core.commands.commands import TechSpecificCommands

class NodeJsCommands(TechSpecificCommands):
    def project_setup_command(self)->str:
        return "npm init -y"

    def package_install_command(self,packages:list[str])->str:
        return f"npm install {' '.join(packages)}"
    