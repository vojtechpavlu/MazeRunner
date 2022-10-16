""""""

from src.algorithms.algorithm import Algorithm
from src.state_space import StateSpace, State


class DepthFirstSearch(Algorithm):
    """"""

    def __init__(self, state_space: StateSpace):
        super().__init__("Depth First Search", state_space)

    @property
    def get_from_fringe(self) -> State:
        """Implementace abstraktní metody předka.
        Tato implementace pro potřeby algoritmu DFS chápe seznam fringe jako
        zásobník (LIFO), bere tedy prvky z konce.
        """
        return self._fringe.pop()

    def run(self) -> State:
        """"""
        while len(self.fringe) > 0:
            current_state = self.get_from_fringe
            if self.state_space.is_final_state(current_state):
                return current_state
            elif self.is_in_closed(current_state):
                continue
            else:
                for o in self.state_space.available_for_state(current_state):
                    self.remember_state(o.apply(current_state))
                self.close_state(current_state)

        raise Exception("Byly prohledány všechny dosažitelné stavy a nic...")
