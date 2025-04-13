import os
import re

class IOHelper:
    @staticmethod
    def stream_code_to_file(streamer, cwd:str, filepath:str) -> str:
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