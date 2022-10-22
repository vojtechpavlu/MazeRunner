"""Definice bludiště a všech potřebných prostředků pro jeho budování."""

# Import knihovny pro potřeby čtení souborů
import os

# Import společného předka (nadtypu) pro TypeHints kontejnerů
from typing import Iterable


# Znak reprezentující zeď, defaultně znak █
WALL_CHARACTER = '█'

# Znak reprezentující cestu, defaultně znak mezery
PATH_CHARACTER = ' '

# Znak reprezentující startovní políčko
START = "S"

# Znak reprezentující cílové políčko
GOAL = "G"


class Field:
    """Instance této třídy slouží k vyjádření políčka (cesty nebo stěny)
    na zadaných souřadnicích."""

    def __init__(self, x: int, y: int, character: str):
        """Initor, který přijímá souřadnice x a y reprezentující dané políčko.
        Dále přijímá znak, který políčko reprezentuje. Z něj odvozuje, zda-li
        je či není políčko stěnou.
        """
        self._x = x
        self._y = y
        self._character = character

        # Z praktických důvodů může mít políčko referenci na bludiště
        self._maze: Maze = None

    @property
    def x(self) -> int:
        """Souřadnice osy x tohoto políčka."""
        return self._x

    @property
    def y(self) -> int:
        """Souřadnice osy y tohoto políčka."""
        return self._y

    @property
    def xy(self) -> tuple[int, int]:
        """Souřadnice os x a y tvořené jako ntice příslušných hodnot."""
        return self.x, self.y

    @property
    def character(self) -> str:
        """Znak, který reprezentuje dané políčko."""
        return self._character

    @property
    def is_wall(self) -> bool:
        """Zda-li je toto políčko stěnou či nikoliv."""
        return self.character == WALL_CHARACTER

    @property
    def is_goal(self) -> bool:
        """Zda-li je toto políčko cílové či nikoliv."""
        return self.character == GOAL

    @property
    def is_start(self) -> bool:
        """Zda-li je toto políčko počátečním či nikoliv."""
        return self.character == START

    @property
    def maze(self) -> "Maze":
        """Bludiště, jehož je toto políčko součástí."""
        return self._maze

    @maze.setter
    def maze(self, maze: "Maze"):
        """Setter pro bludiště, kterého má být toto políčko součástí."""
        self._maze = maze

    def __str__(self):
        """Dunder metoda vracející textovou reprezentaci instance."""
        return f"[{self.x}, {self.y}]"

    def __eq__(self, other: object) -> bool:
        """Metoda porovnává dodaný objekt, zda-li je políčkem na stejných
        souřadnicích. Tím je umožněno porovnávání pomocí operátoru ==.
        Vrací True pokud jsou pro obě políčka stejné souřadnice os x i y.
        Pochopitelně by nemělo být používáno pro porovnávání políček různých
        bludišť.
        """
        return isinstance(other, Field) and other.xy == self.xy


class Maze:
    """Instance této třídy jsou odpovědné za udržování informace o bludišti
    coby souboru políček. Nad rámec poskytování této funkce plní instance
    této třídy i roli vyhledávače mezi políčky.
    """

    def __init__(self, fields: Iterable[Field]):
        """Initor, který přijímá libovolnou iterovatelnou sadu sestavenou
        z políček (instancí třídy Field).

        Ta jsou dále převedena na seznam pro snazší manipulaci.
        """

        # Dodaná políčka se převádí na seznam
        self._fields = list(fields)

        # Pro každé své políčko nastav sebe jako bludiště
        for field in self.fields:
            field.maze = self

    @property
    def fields(self) -> tuple[Field]:
        """Políčka daného bludiště převedená na ntici."""
        return tuple(self._fields)

    @property
    def start_field(self) -> Field:
        """Startovní políčko, ze kterého se má začít."""
        for field in self.fields:
            if field.is_start:
                return field
        # Pokud nebylo nalezeno startovní políčko
        raise Exception("Startovní políčko nebylo nalezeno")

    @property
    def goal_field(self) -> Field:
        """Cílové políčko, na kterém je cílem skončit."""
        for field in self.fields:
            if field.is_goal:
                return field
        # Pokud nebylo nalezeno cílové políčko
        raise Exception("Cílové políčko nebylo nalezeno")

    def has_field(self, x: int, y: int) -> bool:
        """Metoda vrací, zda-li má bludiště políčko o daných souřadnicích.
        """
        # Pokud políčko na daných souřadnicích je nalezeno (není None)
        return self.field(x, y) is not None

    def field(self, x: int, y: int) -> Field:
        """Metoda se pokusí vyhledat políčko, které by odpovídalo dodaným
        souřadnicím."""
        for field in self.fields:
            if field.x == x and field.y == y:
                return field


def filter_empty_lines(lines: Iterable[str]) -> tuple[str]:
    """Funkce přijímá seznam řádků, ty ořízne o počáteční a koncové bílé znaky
    a vybere jen ty, které jsou neprázdné.
    """
    # Převod každého řádku na řetězec s odříznutými mezerami na obou koncích
    stripped_lines = tuple(map(lambda line: str(line.strip()), lines))

    # Navrácení ntice, která neobsahuje řádky, které mají délku 0
    return tuple(filter(lambda line: len(line), stripped_lines))


def load_maze(filename: str) -> Maze:
    """Funkce, která se pokusí najít soubor ve standardním adresáři a vytvořit
    z něj bludiště.
    """

    # Cesta ke kořeni projektu
    project_dir = os.path.dirname(os.path.dirname(__file__))

    # Cesta k souboru, ve kterém je definice bludiště
    maze_path = os.path.join(project_dir, "mazes", filename)

    # Seznam políček, ze kterých se má bludiště sestávat
    fields: list[Field] = []

    # Čti soubor v kódování UTF-8
    with open(maze_path, "r", encoding="utf-8") as reader:

        # Filtrace řádků, aby zbyly pouze neprázdné
        lines = reversed(filter_empty_lines(reader.readlines()))

        # Pro každý řádek souboru reprezentující řádek mapy
        for row_number, row in enumerate(lines):

            # Pro každý znak na řádku reprezentující políčko
            for column_number, character in enumerate(tuple(row)):

                # Přidej políčko do seznamu políček
                fields.append(Field(column_number, row_number, character))

    # Ze seznamu políček vytvoř instanci bludiště a vrať ji
    return Maze(fields)
