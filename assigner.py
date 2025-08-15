from models import Room, Student

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

