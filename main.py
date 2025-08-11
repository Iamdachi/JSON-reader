import json
import xml.etree.ElementTree as ET
import argparse
from abc import ABC, abstractmethod
from pathlib import Path
from typing import TypedDict, NotRequired


class Room(TypedDict):
    id: int
    name: str
    students: NotRequired[list[str]]


class Student(TypedDict):
    id: int
    name: str
    room: int

class ReaderInterface(ABC):
    @abstractmethod
    def read(self, filepath: str) -> list[Student] | list[Room]:
        """Read students or rooms data from a file.

        Args:
            filepath: Path to the file.

        Returns:
            The parsed list of students or rooms.
        """
        pass

class WriterInterface(ABC):
    @abstractmethod
    def write(self, filepath: str, data: list[Room]) -> None:
        """Write room data to a file.

        Args:
            filepath: Path to the output file.
            data: The data to be written.
        """
        pass

class JSONReader(ReaderInterface):
    """Read JSON data from a file."""

    def read(self, filepath: str) -> list[Student] | list[Room]:
        """Read and parse JSON from a file.

        Args:
            filepath: Path to the JSON file.

        Returns:
            The parsed JSON content.
        """
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)


class JSONWriter(WriterInterface):
    """Write data to a JSON file."""

    def write(self, filepath: str, data: list[Room]) -> None:
        """Write room data to a JSON file.

        Args:
            filepath: Path to the output file.
            data: A list of dictionaries to write as JSON.
        """
        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)


class XMLWriter(WriterInterface):
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

    def write(self, filepath: str, data: list[Room]) -> None:
        """Write data to an XML file.

        Args:
            filepath: Path to the output XML file.
            data: A list of room dictionaries.
        """

        tree = self.build_tree(data)
        tree.write(filepath, encoding="utf-8", xml_declaration=True)


class RoomAssigner:
    """Assign students to their respective rooms."""

    @staticmethod
    def assign_students(
        rooms: list[Room], students: list[Student]
    ) -> list[Room]:
        """Add each student to the list of students in their assigned room.

        Args:
            rooms: A list of room dictionaries.
            students: A list of student dictionaries, each with 'name' and 'room' keys.

        Returns:
            The list of rooms, each with an added 'students' list.
        """

        for student in students:
            room_index = student["room"]
            name = student["name"]
            if "students" not in rooms[room_index]:
                rooms[room_index]["students"] = []
            rooms[room_index]["students"].append(name)
        return rooms

class RoomService:
    """Orchestrates reading, processing, and writing room data."""

    def __init__(self, reader: ReaderInterface, writer: WriterInterface, assigner: RoomAssigner):
        """Initialize the RoomService.

            Args:
                reader: An object implementing ReaderInterface.
                writer: An object implementing WriterInterface.
                assigner: A RoomAssigner instance.
        """
        self.reader = reader
        self.writer = writer
        self.assigner = assigner

    def process(self, rooms_file: str, students_file: str, output_file: str
    ) -> None:
        """Read input files, assign students to rooms, and write the result.

            Args:
                rooms_file: Path to the rooms JSON file.
                students_file: Path to the students JSON file.
                output_file: Path to the output file (.json or .xml).
        """
        rooms = self.reader.read(rooms_file)
        students = self.reader.read(students_file)
        assigned_rooms = self.assigner.assign_students(rooms, students)
        self.writer.write(output_file, assigned_rooms)


def main() -> None:
    """Entry point for CLI execution.

    Parses command-line arguments, sets up dependencies, and runs the
    room assignment process.
    """
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
        "--output-file",
        required=True,
        help="Path to the output file. Provide .json or .xml extension."
    )

    args = parser.parse_args()

    writers = {
        ".json": JSONWriter(),
        ".xml": XMLWriter(),
    }

    reader = JSONReader()
    assigner = RoomAssigner()

    extension = Path(args.output_file).suffix.lower()
    writer = writers.get(extension)

    if not writer:
        raise ValueError(f"Unsupported output format: {extension}")

    service = RoomService(reader, writer, assigner)
    service.process(args.rooms, args.students, args.output_file)


if __name__ == "__main__":
    main()
