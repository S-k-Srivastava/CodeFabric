import os
import pickle
from typing import Any, Dict, Optional
from pathlib import Path

MEMORY_PATH = Path(__file__).parent.parent.parent / "memories/"

class PickleMemory:
    def __init__(self, id: str):
        self.id = id
        self.memory: Dict[str, Any] = {"id": id}

    def add(self, key: str, value: Any) -> None:
        self.memory[key] = value

    def get(self, key: str) -> Optional[Any]:
        return self.memory.get(key)

    def get_all(self) -> Dict[str, Any]:
        return self.memory

    def delete(self, key: str) -> None:
        if key == "id":
            raise KeyError("Cannot delete the 'id' key")
        self.memory.pop(key)

    def clear(self) -> None:
        self.memory.clear()
        self.memory["id"] = self.id

    def __str__(self) -> str:
        return str(self.memory)

    def save_as_pkl(self) -> str:
        try:
            path = MEMORY_PATH / f"{self.id}.pkl"
            os.makedirs(path.parent, exist_ok=True)
            with open(path, "wb") as f:
                pickle.dump(self.memory, f)
            return path
        except IOError as e:
            raise IOError(f"Failed to save memory to {path}: {str(e)}")

    @staticmethod
    def load_from_pkl(id: str) -> 'PickleMemory':
        try:
            path = MEMORY_PATH / f"{id}.pkl"
            with open(path, "rb") as f:
                data = pickle.load(f)
            if not isinstance(data, dict) or "id" not in data:
                raise KeyError("Loaded data must be a dictionary containing an 'id' key")
            memory = PickleMemory(data["id"])
            memory.memory = data
            return memory
        except FileNotFoundError:
            raise FileNotFoundError(f"No file found at {path}")
        except pickle.UnpicklingError as e:
            raise pickle.UnpicklingError(f"Failed to unpickle file at {path}: {str(e)}")
        except Exception as e:
            raise Exception(f"Error loading memory from {path}: {str(e)}")
    
    @staticmethod
    def delete_pkl(id: str) -> None:
        try:
            path = MEMORY_PATH / f"{id}.pkl"
            path.unlink()
        except FileNotFoundError:
            pass