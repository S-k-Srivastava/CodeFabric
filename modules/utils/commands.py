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
    
class VsCodeCommands:
    def open_vscode(self)->str:
        return "code ."
    
    def focus_a_file(self,file_path:str,line_number:int)->str:
        return f"code --goto f{file_path}:{line_number}"