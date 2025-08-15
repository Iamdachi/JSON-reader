import argparse
from pathlib import Path
from readers import JSONReader
from writers import JSONWriter, XMLWriter
from assigner import RoomAssigner
from processor import RoomAssignmentProcessor

def main():
    parser = argparse.ArgumentParser(description="Assign students to rooms and export results.")
    parser.add_argument("--students", required=True)
    parser.add_argument("--rooms", required=True)
    parser.add_argument("--output-file", required=True)
    args = parser.parse_args()

    rooms_file = Path(args.rooms)
    students_file = Path(args.students)
    output_file = Path(args.output_file)
    extension = output_file.suffix.lower()

    writer_map = {
        ".json": JSONWriter(),
        ".xml": XMLWriter()
    }

    writer = writer_map.get(extension)
    if not writer:
        raise ValueError(f"Unsupported output format: {extension}")

    processor = RoomAssignmentProcessor(JSONReader(), writer, RoomAssigner())
    processor.assign_and_export(rooms_file, students_file, output_file)

if __name__ == "__main__":
    main()
