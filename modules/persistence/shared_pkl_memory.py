import os
import pickle
from typing import Any, Dict, Optional
from pathlib import Path

MEMORY_PATH = Path(__file__).parent.parent.parent / "memories"

class SharedPKLMemory:
    def __init__(self, id: str):
        self.id = id
        self.path = MEMORY_PATH / f"{id}.pkl"
        os.makedirs(self.path.parent, exist_ok=True)
        self.memory: Dict[str, Any] = self._load_memory()

    def _load_memory(self) -> Dict[str, Any]:
        if self.path.exists():
            with open(self.path, "rb") as f:
                data = pickle.load(f)
                if isinstance(data, dict) and "id" in data:
                    return data
        return {"id": self.id}

    def _save(self) -> None:
        with open(self.path, "wb") as f:
            pickle.dump(self.memory, f)

    @property
    def file_path(self) -> str:
        return str(self.path)

    def get_memory(self, memory_for: str) -> 'ScopedMemory':
        if memory_for not in self.memory:
            self.memory[memory_for] = {}
            self._save()
        return ScopedMemory(self, memory_for)

    def _add_key(self, memory_for: str, key: str, value: Any) -> None:
        if memory_for not in self.memory:
            self.memory[memory_for] = {}
        self.memory[memory_for][key] = value
        self._save()

    def _get_key(self, memory_for: str, key: str) -> Optional[Any]:
        return self.memory.get(memory_for, {}).get(key)

    def _has_key(self, memory_for: str, key: str) -> bool:
        return key in self.memory.get(memory_for, {})

    def _get_all(self, memory_for: str) -> Dict[str, Any]:
        return dict(self.memory.get(memory_for, {}))

    def _delete_key(self, memory_for: str, key: str) -> None:
        if key in self.memory.get(memory_for, {}):
            del self.memory[memory_for][key]
            self._save()

    def _clear_memory_for(self, memory_for: str) -> None:
        self.memory[memory_for] = {}
        self._save()

    @staticmethod
    def delete_pkl(id: str) -> None:
        path = MEMORY_PATH / f"{id}.pkl"
        try:
            path.unlink()
        except FileNotFoundError:
            pass


class ScopedMemory:
    def __init__(self, manager: SharedPKLMemory, memory_for: str):
        self.manager = manager
        self.memory_for = memory_for

    def add(self, key: str, value: Any) -> None:
        self.manager._add_key(self.memory_for, key, value)

    def get(self, key: str) -> Optional[Any]:
        return self.manager._get_key(self.memory_for, key)

    def has_key(self, key: str) -> bool:
        return self.manager._has_key(self.memory_for, key)

    def get_all(self) -> Dict[str, Any]:
        return self.manager._get_all(self.memory_for)

    def delete(self, key: str) -> None:
        self.manager._delete_key(self.memory_for, key)

    def clear(self) -> None:
        self.manager._clear_memory_for(self.memory_for)

    def __str__(self) -> str:
        return str(self.get_all())