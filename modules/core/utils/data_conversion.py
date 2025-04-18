import json
from pydantic import BaseModel, create_model
from typing import Any, Type
from uuid import uuid4

def create_dynamic_base_model(data: dict, model_name: str = "DynamicModel") -> Type[BaseModel]:
    try:
        # Infer field types from values, default to Any if None
        fields = {key: (type(value) if value is not None else Any, ...) for key, value in data.items()}
        # Create a new BaseModel class dynamically
        dynamic_model = create_model(model_name, **fields)
        # Instantiate and validate the model with the data
        return dynamic_model(**data)
    except Exception as e:
        raise ValueError(f"Failed to create dynamic BaseModel: {str(e)}")

def serialize_pydantic_model(value: BaseModel) -> str:
    if not isinstance(value, BaseModel):
        raise ValueError("Value is not a Pydantic model")
    serialized = {
        'value': value.model_dump_json(),
        'type': 'pydantic',
        'model_name': value.__class__.__name__,  # Unique ID for model instance
    }
    return json.dumps(serialized)

def deserialize_pydantic_model(value: str) -> BaseModel:
    value_dict = json.loads(value)
    if not isinstance(value_dict, dict) or value_dict.get('type') != 'pydantic':
        raise ValueError("Value is not a serialized Pydantic model")
    data = json.loads(value_dict['value'])
    model_instance = create_dynamic_base_model(data,model_name=value_dict['model_name'])
    return model_instance

def serialize_typedict(value: dict) -> str:
    if not isinstance(value, dict):
        raise ValueError("Value is not a dict")
    serialized = {
        'value': {
            key: (
                serialize_pydantic_model(val) if isinstance(val, BaseModel) else
                serialize_typedict(val) if isinstance(val, dict) else
                serialize_other_values(val)
            )
            for key, val in value.items()
        },
        'type': 'typedict'
    }
    return json.dumps(serialized)

def deserialize_typedict(value: str) -> dict:
    value_dict = json.loads(value)
    if not isinstance(value_dict, dict) or value_dict.get('type') != 'typedict':
        raise ValueError("Value is not a serialized typedict")
    result = {}
    for key, val in value_dict['value'].items():
        val_dict = json.loads(val) if isinstance(val, str) else val
        if isinstance(val_dict, dict) and 'type' in val_dict:
            if val_dict['type'] == 'pydantic':
                result[key] = deserialize_pydantic_model(val)
            elif val_dict['type'] == 'typedict':
                result[key] = deserialize_typedict(val)
            else:
                result[key] = deserialize_other_values(val)
        else:
            result[key] = val_dict
    return result

def serialize_other_values(value: Any) -> str:
    try:
        return json.dumps({
            'value': value,
            'type': type(value).__name__
        })
    except Exception as e:
        raise ValueError(f"Failed to serialize value: {str(e)}")

def deserialize_other_values(value: str) -> Any:
    value_dict = json.loads(value)
    if not isinstance(value_dict, dict) or 'value' not in value_dict:
        raise ValueError("Invalid serialized value")
    return value_dict['value']

def serialize_data(data: Any) -> str:
    if isinstance(data, BaseModel):
        return serialize_pydantic_model(data)
    elif isinstance(data, dict):
        return serialize_typedict(data)
    else:
        return serialize_other_values(data)

def deserialize_data(data: str) -> Any:
    if not isinstance(data, str):
        raise ValueError("Input must be a serialized string")
    value = json.loads(data)
    if value['type'] == 'pydantic':
        return deserialize_pydantic_model(data)
    elif value['type'] == 'typedict':
        return deserialize_typedict(data)
    else:
        return deserialize_other_values(data)