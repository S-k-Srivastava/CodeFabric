from abc import ABC

class TechSpecificCommands(ABC):
    def project_setup_command(self)->str:
        pass
    
    def package_install_command(self,packages:list[str])->str:
        pass
    
class VsCodeCommands:
    @staticmethod
    def open_vscode()->str:
        return "code ."
    
    @staticmethod
    def focus_a_file(file_path:str,line_number:int=0)->str:
        return f"code --goto {file_path}:{line_number}"
