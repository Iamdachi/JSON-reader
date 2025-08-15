from pathlib import Path

from readers import BaseReader
from writers import BaseWriter
from assigner import RoomAssigner


class RoomAssignmentProcessor:
    """Orchestrates reading, processing, and writing room data."""

    def __init__(self, reader: BaseReader, writer: BaseWriter, assigner: RoomAssigner):
        """Initialize the RoomService.

            Args:
                reader: An object implementing ReaderInterface.
                writer: An object implementing WriterInterface.
                assigner: A RoomAssigner instance.
        """
        self.reader = reader
        self.writer = writer
        self.assigner = assigner

    def assign_and_export(self, rooms_file: Path, students_file: Path, output_file: Path
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
