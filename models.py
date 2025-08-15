from typing import TypedDict, NotRequired

class BaseEntity(TypedDict):
    id: int
    name: str

class Room(BaseEntity):
    students: NotRequired[list[str]]

class Student(BaseEntity):
    room: int
