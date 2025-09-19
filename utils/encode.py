import numpy as np

from models.event import Event

TYPE_INDEX = {
    'KeyPress': 0,
    'MousePosition': 1,
    'MouseClick': 2
}

KEYS = ['W', 'A', 'S', 'D', 'Space', 'Shift', 'Q', 'E', 'R', 'F', 'C', 'V']

MOUSE_BUTTONS = ['left', 'right']

def encode_event(event: Event):
    vector = np.full(5, -1.0, dtype=np.float32)
    event_type = event.__class__.__name__

    vector[0] = TYPE_INDEX.get(event_type, -1)

    if event_type == 'KeyPress':
        if event.key in KEYS:
            vector[1] = float(KEYS.index(event.key))

    elif event_type in ('MousePosition', 'MouseClick'):
        vector[2] = float(event.position[0])
        vector[3] = float(event.position[1])

        if event_type == 'MouseClick' and event.button in MOUSE_BUTTONS:
            vector[4] = float(MOUSE_BUTTONS.index(event.button))

    return vector

