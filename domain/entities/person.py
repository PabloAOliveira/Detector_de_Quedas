from dataclasses import dataclass

@dataclass
class Person:
    id: str
    name: str
    is_fallen: bool = False