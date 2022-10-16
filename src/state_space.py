"""Tento modul obsahuje definici abstrakční roviny pro oproštění se od
představy bludiště a pro možnosti použití prakticky libovolného algoritmu
pro prohledávání stavového prostoru při aplikaci na hledání cesty v bludišti.
"""

# Import společného protokolu pro iterovatelné objekty
from typing import Iterable

# Import potřebných zdrojů pro napojení abstrakce na bludiště ("realitu")
from .maze import Field, Maze
from .direction import Direction


class State:
    """Stav je základní a nejdůležitější entitou abstrakce stavového prostoru.
    Kromě vlastní reprezentace světa a jeho momentálního rozložení obsahuje
    i řídící konstrukce, jako reference na svého předka či operátor, který
    byl na předka aplikován a z čehož vznikla daná instance.
    """

    def __init__(self, field: Field, parent: "State" = None,
                 operator: "Operator" = None):
        """Initor třídy, který přijímá referenci na políčko, které reprezetnuje
        dané aktuální rozložení. Dále přijímá volitelný parametr pro rodiče,
        ze kterého tato instance byla stvořena, a operátor coby přechodovou
        funkci, který to zprostředkoval (taktéž volitelný).
        """
        self._field = field
        self._parent = parent
        self._operator = operator

    @property
    def field(self) -> Field:
        """Políčko, které reprezentuje tento stav."""
        return self._field

    @property
    def field_coords(self) -> tuple[int, int]:
        """Zkrácená notace pro získání souřadnic políčka."""
        return self.field.x, self.field.y

    @property
    def maze(self) -> Maze:
        """Zkrácená notace pro získání reference na bludiště."""
        return self.field.maze

    @property
    def parent(self) -> "State":
        """Rodičovský stav, ze kterého byl tento vytvořen."""
        return self._parent

    @property
    def applied_operator(self) -> "Operator":
        """Operátor, který byl aplikován na rodiče, aby vznikl tento stav."""
        return self._operator

    @property
    def has_parent(self) -> bool:
        """Vrací True, pokud má stanoveného rodiče. Pokud stanoveného rodiče
        nemá, vrací False."""
        return self._parent is not None

    @property
    def all_parents(self) -> tuple["State"]:
        """Všichni rodiče aktuálního stavu v ntici."""
        parents = []

        # Pokud máš rodiče
        if self.has_parent:

            # Přidej všechny rodičovské stavy svého rodiče
            parents.extend(self.parent.all_parents)

            # Přidej svého aktuálního rodiče
            parents.append(self.parent)

        # Vrať svůj seznam rodičů jako ntici
        return tuple(parents)

    @property
    def whole_path(self) -> tuple["Operator"]:
        """Vrací celou cestu (sekvenci operátorů) až k tomuto stavu."""
        operators = []
        if self.has_parent:
            # Přidej celou cestu ke svému rodičovskému stavu
            operators.extend(self.parent.whole_path)

            # Přidej operátor, který byl použit pro vytvoření tohoto stavu
            operators.append(self.applied_operator)

        # Vrať seznam všech aplikovaných operátorů jako ntici
        return tuple(operators)

    def __eq__(self, other: object) -> bool:
        """Dunder metoda umožňující porovnávání objektů pomocí operátoru ==.
        Samotné porovnání je postaveno na porovnávání políčka; v první řadě
        (aby se předešlo logickým chybám) je porovnávána příslušnost dodaného
        objektu `other` k třídě `State`.
        """
        return isinstance(other, State) and self.field == other.field


class Operator:
    """Operátor plní roli přechodové funkce pro převod z jednoho stavu do
    druhého. V rámci reprezentace grafu pak operátor plní roli hrany grafu
    mezi uzly (stavy).
    """

    def __init__(self, direction: Direction):
        """Initor, který přijímá směr, kterým se lze v bludišti vydat. Samotná
        instance pak plní roli abstrakce nad skutečností posunu v bludišti.
        """
        self._direction = direction

    @property
    def direction(self) -> Direction:
        """Vrací směr, který reprezentuje daný operátor."""
        return self._direction

    def can_be_applied(self, state: State) -> bool:
        """Metoda vrací informaci o tom, zda-li je možné aplikovat tento
        operátor na daný stav.

        Z vysokoúrovňového pohledu musí políčko v daném bludišti existovat
        a nesmí být zdí. Pokud že jsou tyto dvě podmínky splněny, pak vrací
        True, jinak False.
        """
        # Souřadnice nového políčka
        x, y = self.direction.neighbour_coordinates(*state.field_coords)

        # Pokud neexistuje políčko s takovými souřadnicemi
        if not state.maze.has_field(x, y):
            return False

        # Pokud je na zadaném políčku zeď
        elif state.maze.field(x, y).is_wall:
            return False

        # Jinak
        return True

    def apply(self, state: State) -> State:
        """Metoda, která aplikuje tento operátor na dodaný stav, čímž vytvoří
        stav nový. Ten je metodou vrácen.

        Pokud nelze tento operátor na daný stav aplikovat, je vyhozena výjimka.
        """

        # Pokud nelze aplikovat musí být tento pokus přerušen chybou
        if not self.can_be_applied(state):
            raise Exception(f"Nelze aplikovat operátor {self} na stav {state}")

        # Souřadnice nového políčka
        x, y = self.direction.neighbour_coordinates(*state.field_coords)

        # Získá referenci na vyhledanou instanci políčka o daných souřadnicích
        destination = state.maze.field(x, y)

        # Vrátí nově vytvořenou instanci stavu s dodaným novým políčkem,
        # referencí na stav, ze kterého byl vytvořen, a na operátor, který
        # byl k tvorbě použit (self)
        return State(field=destination, parent=state, operator=self)

    def __repr__(self) -> str:
        """Metoda vrací textovou reprezentaci operátoru založenou na názvu
        směru, který operátor představuje."""
        return self.direction.direction_name


class StateSpace:
    """Stavový prostor plní roli pomocné přepravky pro důležité objekty.
    Sám o sobě je abstrakcí nad úlohou prohledávání prostoru stavů a operátorů,
    s cílem nalézt cestu mezi počátečním a cílovým políčkem v bludišti.
    """

    def __init__(self, available_ops: Iterable[Operator], initial_state: State,
                 final_state: State):
        """"""
        self._operators = available_ops
        self._initial_state = initial_state
        self._final_state = final_state

    @property
    def available_operators(self) -> tuple[Operator]:
        """Dostupné operátory, které lze pro prohledávání stavového prostoru
        použít."""
        return tuple(self._operators)

    @property
    def initial_state(self) -> State:
        """Vrací výchozí stav, ze kterého je prohledávání započato. Typicky
        ho lze chápat dvojím způsobem:

            - Jako starovní políčko v bludišti
            - Na obecné úrovni jako kořen stromu stavového prostoru, který
              nemá žádného předka (podstata stromu)
        """
        return self._initial_state

    @property
    def final_state(self) -> State:
        """Vrací referenci na dodaný hypotetický stav, který má reprezentovat
        cíl. Ten je vytvořen uměle, ještě před spuštěním algoritmu pro nalezení
        cesty mezi výchozím a cílovým stavem."""
        return self._final_state

    def is_final_state(self, state: State) -> bool:
        """Metoda, která vrací booleovskou informaci o tom, zda-li je dodaný
        stav cílový či nikoliv.
        Pokud je cílem, musí být totožný se stavem finálním.
        """
        return self.final_state == state

    def available_for_state(self, state: State) -> tuple[Operator]:
        """Metoda vrací ntici všech operátorů, které lze aplikovat na dodaný
        stav. O možnostech aplikace se rozhoduje autonomně každý původně
        dodaný operátor sám.
        """
        # Vrací ntici vytvořenou z profiltrované sady operátorů
        return tuple(filter(

            # Lambda funkce, která pro každý operátor ověří aplikovatelnost
            lambda operator: operator.can_be_applied(state),

            # Vstupní soubor operátorů, který se má profiltrovat
            self.available_operators))
