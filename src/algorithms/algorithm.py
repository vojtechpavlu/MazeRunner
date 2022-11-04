"""Modul obsahuje abstraktní definici algoritmu. Díky abstrakční vrstvě, která
převádí problem virtuálního bludiště do problému reprezentovaného jako graf,
je možné použít algoritmy pro hledání cest v grafu.

Společným předkem pro všechny implementace takových grafů je (v zájmu redukce
redundance) abstraktní třída Algorithm.
"""

# Import prostředků pro definici abstraktních tříd a metod
from abc import ABC, abstractmethod

# Import tříd Stavového prostoru a stavu
from src.state_space import StateSpace, State


class Algorithm(ABC):
    """Abstraktní třída Algorithm poskytuje společné služby pro všechny své
    potomky, tedy algoritmy pro procházení grafů.

    V zásadě musí být instance této třídy schopny udržovat stavový prostor a
    poskytovat služby práce se seznamy uzlů k prohledání a již prohledaných.

    Samotný běh algoritmu je definován abstraktní metodou `run()`, abstraktní
    je dále i metoda pro poskytování dalšího uzlu k prohledání (každý
    algoritmus se liší od ostatních mimo jiné i v tomto).
    """

    def __init__(self, algo_name: str, state_space: StateSpace):
        """Initor, který přijímá název algoritmu (pro rozlišovacích schopnosti)
        a instanci stavového prostoru, v němž bude problém řešit.

        Všichni potomci mají k těmto údajům přístup.
        """
        self._algo_name = algo_name
        self._state_space = state_space
        self._fringe: list[State] = [state_space.initial_state]
        self._closed: list[State] = []

    @property
    def algorithm_name(self) -> str:
        """Vlastnost vrací název algoritmu."""
        return self._algo_name

    @property
    def state_space(self) -> StateSpace:
        """Vrací stavový prostor, ve kterém má být prohledávání prováděno."""
        return self._state_space

    @property
    def fringe(self) -> tuple[State]:
        """Vlastnost vrací celý seznam prvků k rozevření."""
        return tuple(self._fringe)

    @property
    def closed(self) -> tuple[State]:
        """Vlastnost vrací celý seznam již rozevřených prvků."""
        return tuple(self._closed)

    def remember_state(self, state: State):
        """Metoda si uloží dodaný stav do seznamu fringe (pro budoucí
        prohledání)."""
        self._fringe.append(state)

    def is_in_closed(self, state: State) -> bool:
        """Vlastnost vrací, zda-li je daný stav již obsažen v seznamu
        prohledaných (closed)."""
        return state in self.closed

    def close_state(self, state: State):
        """Metoda uloží dodaný stav do seznamu již prohledaných a uzavřených
        stavů."""
        self._closed.append(state)

    def run(self):
        """Metoda, která spouští algoritmus. Implementace této metody sama o
        sobě definuje, jak bude algoritmus postupovat při prohledávání.

        Zde je uveden obecný algoritmus pro prohledávání stavového prostoru,
        tuto metodu lze volitelně překrýt, či využít stávající implementace.

        Tato implementace funguje na principu postupného rozevírání uzlů a
        přidávání potomků těchto uzlů do seznamu stavů k budoucímu prohledání.
        Toto prohledávání je iterativně prováděno, dokud tento seznam stavů
        k prohledání je neprázdný. Jakmile se tento vyprázdní a řešení nebylo
        nalezeno, je vyhozena chyba. V opačném případě se pro každý stav
        porovnává, zda-li není cílový, což vede k úspěšnému ukončení. Není-li,
        zjišťuje se, zda-li již nebyl prohledáván. Pokud ne, jsou přidáni
        všichni jeho potomci do seznamu k dalšímu prohledání.

        Výsledkem běhu algoritmu je typicky vyhození výjimky. V pozitivním
        případě je vyhozena výjimka `Success` reprezentující úspěšné nalezení
        cílového řešení. V opačném případě výjimka `Failure`, která naopak
        značí, že algoritmus při hledání selhal.
        """
        while len(self.fringe) > 0:
            current_state = self.get_from_fringe
            if self.state_space.is_final_state(current_state):
                raise Success("Byl nalezen cílový stav!", current_state)
            elif self.is_in_closed(current_state):
                continue
            else:
                for o in self.state_space.available_for_state(current_state):
                    self.remember_state(o.apply(current_state))
                self.close_state(current_state)

        # Pokud již není co prohledávat a řešení nebylo nalezeno
        raise Failure("Byly prohledány všechny dosažitelné stavy a nic...")

    @property
    @abstractmethod
    def get_from_fringe(self) -> State:
        """Abstraktní metoda, která vrací element ze seznamu stavů k rozevření.
        """


class Success(Exception):
    """Výjimka reprezentující úspěšné vyřešení úlohy. Výjimka zde není chápána
    jako chyba, nýbrž jako úspěšné splnění cíle.

    Z povahy práce výjimek je pak snazší postoupit místu volání nejen výstup
    (i v případě rekurzivní exekuce kódu), ale i sémantiku způsobu vyřešení.
    """

    def __init__(self, message: str, final_state: State):
        """Initor, který přijímá zprávu o vyřešení úlohy a cílový stav.
        """
        Exception.__init__(self, message)
        self._final_state = final_state

    @property
    def final_state(self) -> State:
        """Stav, který byl nalezen a ze kterého lze získat řešení problému."""
        return self._final_state


class Failure(Exception):
    """Výjimka reprezentující neúspěšné řešení úlohy. V pravém slova smyslu
    zde jde o chybu způsobenou bezvýchodnou situací - například že je řešení
    nedosažitelné."""

    def __init__(self, message: str, last_valid_state: State = None):
        """Initor, který přijímá textovou zprávu o chybě a poslední validní
        nalezený stav. Ten je volitelným parametrem; defaultně `None`.
        """
        Exception.__init__(self, message)
        self._last_valid_state = last_valid_state

    @property
    def has_last_valid_state(self) -> bool:
        """Vrací, zda-li byl či nebyl dodán poslední validní stav."""
        return self._last_valid_state is not None

    @property
    def last_valid_state(self) -> State:
        """Poslední validní nalezený stav, který však není cílovým."""
        return self._last_valid_state

