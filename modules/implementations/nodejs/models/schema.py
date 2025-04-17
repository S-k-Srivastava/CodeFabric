from pydantic import BaseModel
from modules.types.nodejs_backend.api import VariableType

class SchemaVariable(BaseModel):
    name : str
    type : VariableType
    optional : bool
    reference_of : str

class Schema(BaseModel):
    name : str
    variables:list[SchemaVariable]