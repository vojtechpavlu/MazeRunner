"""Modul obsahuje definici směru coby základního nástroje pro vyjádření
posunu ve 2D světě."""


class Direction:
    """Instance této třídy reprezentují nástroj pro popis posunu ve 2D světě.
    Směry jsou zamýšleny jako ortogonální a globální (E-N-W-S).

    Způsob posunu je pak chápán jako vektorové vyjádření změny souřadnic
    aplikací daného směru (x_diff a y_diff).
    """

    def __init__(self, name: str, x_diff: int, y_diff: int):
        """Initor třídy, který přijímá název směru a velikost posunů v
        osách x a y.
        """
        self._name = name
        self._x_diff = x_diff
        self._y_diff = y_diff

    @property
    def direction_name(self) -> str:
        """Název směru"""
        return self._name

    @property
    def x_diff(self) -> int:
        """Velikost posunu v ose x"""
        return self._x_diff

    @property
    def y_diff(self):
        """Velikost posunu v ose y"""
        return self._y_diff

    def neighbour_coordinates(self, x: int, y: int) -> tuple[int, int]:
        """Funkce vrací souřadnice po posunu v tomto směru.
        Ve skutečnosti nemusí dané souřadnice v daném bludišti vůbec
        existovat."""
        return x + self.x_diff, y + self.y_diff

    @staticmethod
    def get_all_directions() -> "tuple[Direction]":
        """Statická funkce, která vrací instance všech ortogonálních směrů,
        které jsou ve 2D světě dostupné."""
        return (Direction("EAST", 1, 0), Direction("NORTH", 0, 1),
                Direction("WEST", -1, 0), Direction("SOUTH", 0, -1),)
