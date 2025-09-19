import time

from dataclasses import dataclass, field

@dataclass
class Event:
    timestamp: float = field(init=False)

    def __post_init__(self):
        self.timestamp = time.time()

@dataclass
class KeyPress(Event):
    key: str 

@dataclass
class MousePosition(Event):
    position: tuple[int, int]

@dataclass
class MouseClick(MousePosition):
    button: str
