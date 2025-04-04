from abc import ABC
from modules.enums.technologies import Technologies

class TechSpecificCommands(ABC):
    def project_setup_command(self)->str:
        pass
    
    def package_install_command(self,packages:list[str])->str:
        pass

class NodeJsCommands(TechSpecificCommands):
    def project_setup_command(self)->str:
        return "npm init -y"

    def package_install_command(self,packages:list[str])->str:
        return f"npm install {' '.join(packages)}"
    
class VsCodeCommands(TechSpecificCommands):
    def project_setup_command(self)->str:
        return "code ."