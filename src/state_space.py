""""""


from typing import Iterable

from .maze import Field, Maze
from .direction import Direction


class State:
    """"""

    def __init__(self, field: Field, parent: "State" = None, operator: "Operator" = None):
        """"""
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


class Operator:
    """"""

    def __init__(self, direction: Direction):
        """"""
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


class StateSpace:
    """"""

    def __init__(self, available_ops: Iterable[Operator], initial_state: State):
        """"""
        self._operators = available_ops
        self._initial_state = initial_state

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

