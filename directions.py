"""Handles directions"""

from enum import IntEnum

class AbsoluteDirections(IntEnum):
    """Enum for absolute directions"""
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

class RelativeDirections(IntEnum):
    """Enum for relative directions"""
    AHEAD = 0
    RIGHT = 1
    LEFT = -1

def get_absolute_direction(current_absolut, relative):
    """Gets the absolute direction for a relative movement
    current_absolut -- current absolute direction
    relative -- relative direction
    """
    return (4 + int(current_absolut) + int(relative)) % 4
