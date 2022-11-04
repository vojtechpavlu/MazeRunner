"""Modul obsahuje definici algoritmu, který prochází stavový prostor náhodně,
bez uvažování modelu či již projitých cest - nesystematicky. V pravém slova
smyslu nejde o 'prohledávání'.

Jeho zařazení mezi ostatní algoritmy je jen z čistě demonstračních důvodů.
"""

from src.algorithms.algorithm import Algorithm, Success, Failure
from src.state_space import StateSpace, State
from random import choice


class Random(Algorithm):
    """Instance této třídy reprezentují algoritmy striktně nesystematické.
    Výběr následovníků je zcela náhodný. Může se i vracet ve svém průchodu
    na políčka, která již navštívil."""

    def __init__(self, state_space: StateSpace):
        """Initor, který přijímá instanci stavového prostoru, v němž řešení
        bude hledat.
        """
        super().__init__("Random Algorithm", state_space)
        self._limit = 30_000

    @property
    def get_from_fringe(self) -> State:
        """Implementace abstraktní metody předka.
        Ve skutečnosti je tato implementace uvedena jen z praktických důvodů.
        Proto při zavolání funkce obalené jako vlastnost vyhazuje výjimku.
        """
        raise Exception(
            "Náhodný algoritmus nevybírá systematicky následníka "
            "aktuálního stavu.")

    @property
    def limit(self) -> int:
        """Limit, kolik iterací je možné provést."""
        return self._limit

    @limit.setter
    def limit(self, new_limit: int):
        """Limit, kolik iterací je možné provést."""
        self._limit = new_limit

    def run(self):
        """Implementace náhodného nesystematického algoritmu.
        """
        # Jako aktuální stav nastav počáteční
        current_state = self.state_space.initial_state
        iteration = 0

        # Dokud není aktuální stav koncovým
        while not self.state_space.is_final_state(current_state):

            # Zvýšení iterace
            iteration += 1

            # Pokud je počet iterací větší, než limit, ukonči běh
            if iteration > self.limit:
                raise Failure(f"Byl překročen limit iterací: {self.limit}",
                              current_state)

            # Vlož aktuální stav jako prohledávaný (do closed) - pro
            # potřeby pozdějšího vyhodnocování efektivity
            self.close_state(current_state)

            # Ulož si všechny dostupné operátory
            all_available = self.state_space.available_for_state(current_state)

            # Náhodně vyber operátor pomocí funkce random.choice(Sequence)
            # a aplikuj ho na aktuální stav a výsledek prohlaš jako nový
            # aktuální stav; konec dané iterace a prokačuj znovu od while
            current_state = choice(all_available).apply(current_state)

        # Byl nalezen cílový stav (byl ukončen cyklus while)
        raise Success("Náhodně nalezen cílový stav", current_state)
