# Python JSON Reader - Assignment #2

## Task
You are given two files:
- students.json
- rooms.json

Your task is to write a Python script that:
- Loads data from both files.
- Combines the data into a list of rooms, where each room includes the students assigned to it.
- Exports the resulting structure in the specified format: JSON or XML.
- Accepts input parameters via the command line (CLI).

Note: Follow SOLID principles.

## Usage

```bash
python main.py --students students.json --rooms rooms.json --output-file result.xml

python main.py --students students.json --rooms rooms.json --output-file result.json
```

## Explanation
This is a simple script that reads two json files and outputs either a json or xml.
Naturally, used json and xml libraries for that. I tried everything to write the code
according to SOLID principles.

Created general interfaces for reader and 
writer classes to handle different JSON/XML read/write operations.

Created Assigner classes that handle room assignment logic.

Created RoomService class that handles the reading, processing, and writing flow.

Main function handles initializing dependencies and handling cli logic. Output file type (JSON/XML)
will be dependent upon the extension of --output-file argument.
