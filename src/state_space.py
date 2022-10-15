""""""

from .maze import Field


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



