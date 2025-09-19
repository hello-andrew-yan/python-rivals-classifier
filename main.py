import os
import sys
import time
import json
import types
import signal

from dataclasses import asdict
from pynput import keyboard, mouse
from models.event import Event, KeyPress, MouseClick, MousePosition

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

_filename = None
_events: list[Event] = []
_last_mouse_move_time = 0

def _on_press(key: keyboard.Key | keyboard.KeyCode):
    try:
        _events.append(KeyPress(key=str(key)))
    except Exception as e:
        print(f"❌ Failed to process keyboard event: {e}")

def _on_click(x: int, y: int, button: mouse.Button, pressed: bool):
    if pressed:
        _events.append(MouseClick(position=(x, y), button=str(button)))

def _on_move(x: int, y: int):
    global _last_mouse_move_time
    now = time.time()
    
    if now - _last_mouse_move_time >= 1.0:
        _last_mouse_move_time = now
        _events.append(MousePosition(position=(x, y)))

def _export_events(filename: str):
    try:
        if not filename.lower().endswith(".json"):
            filename += ".json"
        
        path = os.path.join(CURRENT_DIR, filename)
        with open(path, "w") as f:
            # Clears the Ctrl + C termination from the event list
            json.dump([asdict(e) for e in _events[:-2]], f, indent=2)
        
        print(f"\n✅ Exported {len(_events)} events to {path}")
    except Exception as e:
        print(f"\n❌ Failed to export events: {e}")


def _handle_exit(signum: int, frame: types.FrameType):
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    _export_events(f"{_filename}_{timestamp}.json".lower().replace(" ", "_"))
    sys.exit(0)

def main():
    global _filename
    _filename = input("Type the hero to track events for: ")

    signal.signal(signal.SIGINT, _handle_exit)
    signal.signal(signal.SIGTERM, _handle_exit)

    with keyboard.Listener(on_press=_on_press) as k_listener, \
            mouse.Listener(on_move=_on_move, on_click=_on_click) as m_listener:
        
        print("🔴 Recording events. Press Ctrl+C to stop and export.")

        k_listener.join()
        m_listener.join()

if __name__ == "__main__":
    main()
