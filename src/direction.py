""""""


class Direction:
    """"""

    def __init__(self, name: str, x_diff: int, y_diff: int):
        """"""
        self._name = name
        self._x_diff = x_diff
        self._y_diff = y_diff

    @property
    def direction_name(self) -> str:
        """Název směru"""
        return self._name

    @property
    def x_diff(self) -> int:
        """Posun v ose x"""
        return self._x_diff

    @property
    def y_diff(self):
        """Posun v ose y"""
        return self._y_diff


DEFAULT_DIRECTIONS = (
    Direction("EAST", 1, 0),
    Direction("NORTH", 0, 1),
    Direction("WEST", -1, 0),
    Direction("SOUTH", 0, -1),
)
