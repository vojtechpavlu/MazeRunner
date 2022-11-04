"""Modul obsahující definici pomocné funkce pro vytištění bludiště do konzole.
"""
from src.maze import Maze


def print_maze(maze: Maze, coords: list[tuple[int, int]], char: str = "*"):
    """Funkce, která přijímá umožňuje vytisknout bludiště.

    Přijímá k tomu referenci na bludiště jako takové, seznam zvýrazněných
    políček (reprezentovaných jako dvojice souřadnic `x` a `y`), a volitelný
    znak, který má dané políčko zvýraznit.
    """
    # Připravení výstupního řetězce
    result = ""

    # Pro každý řádek (obrácený)
    for y in reversed(range(maze.height)):

        # Pro každé políčko v řádku
        for x in range(maze.width):

            # Pokud je zvýrazňované políčko, vrať dodaný znak, jinak defaultní
            # znak daného políčka
            result += char if (x, y) in coords else maze.field(x, y).character

        # Zakonči řádek posunem na nový řádek
        result += "\n"

    # Vytiskni celý výsledek
    print(result)
