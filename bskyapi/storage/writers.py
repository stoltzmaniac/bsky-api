import typing as t
from abc import ABC, abstractmethod


class DataWriter(ABC):
    """Abstract base class for writing data."""
    
    @abstractmethod
    def write(self, data: t.List[dict]):
        """Write the provided data."""
        pass


class JsonFileWriter(DataWriter):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def write(self, data: t.List[dict]):
        import json
        with open(self.file_path, 'w') as file:
            json.dump(data, file, indent=2)
