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