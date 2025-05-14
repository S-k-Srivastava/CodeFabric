from enum import Enum

class Technologies(Enum):
    PYTHON = "python"
    PYTHON_UV = "python-uv"
    NodeJS = "nodejs"
    other = "other"

class PatchType(Enum):
    ADD = "add-a-new-file"
    REMOVE = "remove-a-file"
    MODIFY = "override-a-file"
    MOVE = "move-a-file-to-another-location"