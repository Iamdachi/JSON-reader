import json
import xml.etree.ElementTree as ET
import argparse
from typing import List, Dict, Any
from abc import ABC, abstractmethod


class ReaderInterface(ABC):
    @abstractmethod
    def read(self, filepath: str) -> Any:
        pass

class WriterInterface(ABC):
    @abstractmethod
    def write(self, filepath: str, data: List[Dict[str, Any]]) -> None:
        pass

class JSONReader(ReaderInterface):
    """Read JSON data from a file."""

    def read(self, filepath: str) -> Any:
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)


class JSONWriter(WriterInterface):
    """Write data to a JSON file."""

    def write(self, filepath: str, data: List[Dict[str, Any]]) -> None:
        with open(filepath + ".json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)


class XMLWriter(WriterInterface):
    """Write room data to an XML file."""

    def write(self, filepath: str, data: List[Dict[str, Any]]) -> None:
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
        tree.write(filepath + ".xml", encoding="utf-8", xml_declaration=True)


class RoomAssigner:
    """Assign students to their respective rooms."""

    def assign_students(
        self, rooms: List[Dict[str, Any]], students: List[Dict[str, str]]
    ) -> List[Dict[str, Any]]:
        """Add student names to the correct room entries."""

        for student in students:
            room_index = student["room"]
            name = student["name"]
            if "students" not in rooms[room_index]:
                rooms[room_index]["students"] = []
            rooms[room_index]["students"].append(name)
        return rooms

class RoomService:
    """Orchestrates reading, processing, and writing room data."""

    def __init__(self, reader: ReaderInterface, writers: List[WriterInterface], assigner: RoomAssigner):
        self.reader = reader
        self.writers = writers
        self.assigner = assigner

    def process(
        self,
        rooms_file: str,
        students_file: str
    ) -> None:
        rooms = self.reader.read(rooms_file)
        students = self.reader.read(students_file)

        updated_rooms = self.assigner.assign_students(rooms, students)

        for writer in self.writers:
            writer.write(f"new_rooms", updated_rooms)


def main() -> None:
    """Entry point for CLI execution."""
    parser = argparse.ArgumentParser(
        description="Assign students to rooms and export results."
    )

    parser.add_argument(
        "--students",
        required=True,
        help="Path to the students file."
    )
    parser.add_argument(
        "--rooms",
        required=True,
        help="Path to the rooms file."
    )

    parser.add_argument(
        "--format",
        choices=["json", "xml", "both"],
        default="both",
        help="Output format for the result."
    )

    args = parser.parse_args()

    writers = {
        "json": [JSONWriter()],
        "xml": [XMLWriter()],
        "both": [JSONWriter(), XMLWriter()]
    }

    reader = JSONReader()
    assigner = RoomAssigner()

    service = RoomService(reader, writers[args.format], assigner)
    service.process(args.rooms, args.students)



if __name__ == "__main__":
    main()
