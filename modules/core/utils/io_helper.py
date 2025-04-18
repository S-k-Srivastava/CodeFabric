import json
import os
import re
from typing import TypedDict
from pydantic import BaseModel

class IOHelper:
    @staticmethod
    def stream_code_to_file(streamer, cwd:str, filepath:str) -> str:
        """
        Streams the code, cleans it using regex filter and writes to a given filepath
        """
        path = os.path.join(cwd, filepath)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        # Store all chunks for returning the complete response
        all_text = ""
        
        # First, collect all the content
        for chunk in streamer:
            all_text += str(chunk.content)
        
        # Pattern to extract code between backticks, including language identifier
        # This handles multiline content properly
        pattern = r'```(?:javascript|js)?\s*([\s\S]*?)```'
        match = re.search(pattern, all_text)
        code_content = match.group(1)
        if match:
            # Write the code to the file
            with open(path, "w", encoding="utf-8") as f:
                f.write(code_content)
        
        return code_content
    
    @staticmethod
    def serialize_value(value):
        try:
            if isinstance(value, BaseModel):
                data = value.model_dump_json()
                return json.dumps({
                    'value': data,
                    'type': type(value).__name__
                })
            elif isinstance(value, dict):
                serialised = {key: IOHelper.serialize_value(val) for key, val in value.items()}
                return json.dumps({
                    'value': serialised,
                    'type': type(value).__name__
                })
            else:
                return json.dumps({
                    'value': value,
                    'type': type(value).__name__
                })
        except Exception as e:
            raise ValueError(f"Failed to serialize value: {str(e)}")