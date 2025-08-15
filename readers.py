import json
from pathlib import Path
from abc import ABC, abstractmethod
from typing import Union
from models import Student, Room

class BaseReader(ABC):
    @abstractmethod
    def read(self, filepath: Path) -> list[Student] | list[Room]:
        """Read students or rooms data from a file.

        Args:
            filepath: Path to the file.

        Returns:
            The parsed list of students or rooms.
        """
        pass

class JSONReader(BaseReader):
    """Read JSON data from a file."""

    def read(self, filepath: Path) -> list[Student] | list[Room]:
        """Read and parse JSON from a file.

        Args:
            filepath: Path to the JSON file.

        Returns:
            The parsed JSON content.
        """
        with filepath.open("r", encoding="utf-8") as file:
            return json.load(file)
