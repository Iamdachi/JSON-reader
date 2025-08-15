import json
import xml.etree.ElementTree as ET
from pathlib import Path
from abc import ABC, abstractmethod
from models import Room

class BaseWriter(ABC):
    @abstractmethod
    def write(self, filepath: Path, data: list[Room]) -> None:
        """Write room data to a file.

        Args:
            filepath: Path to the output file.
            data: The data to be written.
        """
        pass

class JSONWriter(BaseWriter):
    """Write data to a JSON file."""

    def write(self, filepath: Path, data: list[Room]) -> None:
        """Write room data to a JSON file.

        Args:
            filepath: Path to the output file.
            data: A list of dictionaries to write as JSON.
        """
        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)


class XMLWriter(BaseWriter):
    """Write room data to an XML file."""

    @staticmethod
    def build_tree(data: list[Room]) -> ET.ElementTree:
        """Build an XML tree from the provided room data.

        Args:
            data: A list of room dictionaries, each possibly containing a
                'students' key with a list of names.

        Returns:
            An ElementTree object representing the rooms and students.
        """

        root = ET.Element("rooms")
        for room_id, room_info in enumerate(data):
            room_elem = ET.SubElement(root, "room", id=str(room_id))
            for key, value in room_info.items():
                if key == "students":
                    students_elem = ET.SubElement(room_elem, "students")
                    for student_name in value:
                        ET.SubElement(students_elem, "student").text = student_name
                else:
                    ET.SubElement(room_elem, key).text = str(value)

        tree = ET.ElementTree(root)
        return tree

    def write(self, filepath: Path, data: list[Room]) -> None:
        """Write data to an XML file.

        Args:
            filepath: Path to the output XML file.
            data: A list of room dictionaries.
        """

        tree = self.build_tree(data)
        tree.write(filepath, encoding="utf-8", xml_declaration=True)

