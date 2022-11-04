# Maze Runner

Projekt pro demonstraci principů symbolických metod pro řešení 
problémů ve stavovém prostoru. Tento projekt byl vyvinut jako studijní
pomůcka pro výuku umělé inteligence při [Smíchovské střední průmyslové škole
a gymnáziu](https://www.ssps.cz/).

---

Samotný projekt se zaměřuje na řešení úlohy hledání cesty v bludišti. Problém
je zde rozdělen do 3 hlavních domén:

- **Bludiště**, coby virtuální, leč hypoteticky skutečná, pozorovaná entita
- **Stavový prostor**, coby nástroj pro abstrakci problému
- **Algoritmy prohledávání grafů**, coby nástroj řešení abstraktních problémů

Díky této struktuře je možné navrhovat *víceméně* univerzální a velmi obecné
algoritmy (obecně algoritmy pro prohledávání grafů) a aplikovat je na takřka
libovolný problém, v tomto případě na problém hledání cesty v bludišti.

Jinými slovy je možné díky stavovému prostoru chápat definici problému jen 
jako parametr pro tyto obecné algoritmy.

<br />

**Zajímavé odkazy:**
- [Graf na Wikipedii](https://en.wikipedia.org/wiki/Graph_(discrete_mathematics))
- [Stavový prostor na Wikipedii](https://en.wikipedia.org/wiki/State_space)
- [Studijní materiály na Google Drive](https://tinyurl.com/ssps-umela-inteligence)


---

## Bludiště

Bludiště chápejme jako dvoudimenzionální (2D) ortogonální prostor sestavený
čtvercových souřadnicových (uspořádaných) políček, která mohou být dvou 
hlavních typů:

- **Cesta** - políčko, na kterém může pohyblivý kurzor stát
- **Zeď** - políčko, které v průchodu (stání na políčku) brání


Cesta dále může mít dva základní archetypy:

- **Start** - počáteční políčko, ze kterého hledání cesty započíná
- **Cíl** - políčko, do kterého ze startu hledáme cestu


Kód odpovědný za práci s bludištěm na této úrovni je uveden 
[zde](https://github.com/vojtechpavlu/MazeRunner/blob/master/src/maze.py).
Důležité jsou zde především definice políčka (třída `Field`), definice 
bludiště (třída `Maze`) a tovární funkce pro vybudování bludiště z názvu 
souboru `load_maze(str)`, která vyhledá soubor daného názvu v adresáři pro
definici bludišť (adresář `mazes`, resp. 
[zde](https://github.com/vojtechpavlu/MazeRunner/tree/master/mazes)).


V projektu je bludiště načítáno ze statických textových souborů. Ty jsou 
sestaveny jako matice znaků:

- '` `' (znak mezery) pro cestu
- '`█`' (znak vybarveného bloku) pro zeď
- '`S`' pro označení počátečního políčka
- '`G`' pro označení cílového políčka

Je-li třeba, lze toto bludiště *naklikat* pomocí připojené [statické webové 
aplikace](https://github.com/vojtechpavlu/MazeRunner/tree/master/misc), 
ke které lze přistupovat na cestě (od kořene projektu) `./misc/index.html`. 
Ta umožňuje vytvoření bludiště o rozměrech mezi `3x3` a `100x100` políček.

Jediné, co uživatel musí pro připravení udělat, jsou tyto kroky:

1. Naklikat bludiště o specifikovaných rozměrech
2. Stáhnout soubor reprezentující bludiště
3. Zahrnout bludiště do projektu (přesunout do adresáře `./mazes/`)
4. Přidat políčka reprezentující počátek ('`S`') a cíl ('`G`') nahrazením
některých dvou políček
   
Pochopitelně projekt předpokládá existenci **právě jednoho** startu a 
**právě jednoho** cíle v jednom bludišti, stejně jako že se bludiště sestává
z alespoň dvou políček (startu a cíle). Stejně tak by projekt neměl obsahovat
jiných znaků.

## Stavový prostor

Stavový prostor je obecně chápán jako symbolická metoda - abstrakce, 
kterou lze použít pro řešení libovolného problému, který lze reprezenovat
jako graf a soubor WFFs (Well-Formed Formulas).

V tomto projektu je tento nástroj chápán jako celá vrstva (rozhraní) 
mezi definicí problému (bludiště) a jeho řešením (obecné algoritmy pro 
prohledávání grafů).

Důležitými jsou především tři entity:

### Stav
Reprezentace libovolného rozložení sledovaného systému, v jakém se validně 
může nácházet. V našem pojetí je to pak políčko, na kterém může náš pohyblivý 
kurzor stát.

Důležitou složkou stavu je tedy políčko (instance třídy `Field`). 
Jeho definici lze nalézt v 
[tomto modulu](https://github.com/vojtechpavlu/MazeRunner/blob/master/src/maze.py).
  

### Operátor
Přechodová funkce, která umožňuje tvořit při prohledávání
následníky stavů. V tomto pojetí je chápáno jako jeden ze 4 absolutistických 
ortogonálních směrů (východ, sever, západ a jih, resp. `EAST`, `NORTH`, 
`WEST` a `SOUTH`). Definice směrů je uvedena 
[zde](https://github.com/vojtechpavlu/MazeRunner/blob/master/src/direction.py).

Na každý stav může být aplikováno více operátorů, čimž vzniká 
potenciálně více následníků ve stromu prohledávání, resp. z každého
políčka se můžeme vydat více směry, tedy můžeme navštívit více sousedů.
Aplikací operárotu na aktuální stav nám vzniká potomek aktuálního stavu,
resp. se přesouváme z aktuálního políčka na políčko v daném směru.


### Stavový prostor
Samotná abstrakce sestávající se z množiny stavů a aplikovatelných operátorů. 
V tomto pojetí je chápán jako mezivrstva (rozhraní) mezi bludištěm a 
algoritmy pro hledání cest. Poskytuje především pomocné služby, jako 
vyhodnocování cílovosti daného stavu nebo výše zmíněnou sadu všech
aplikovatelných směrů.

---  

## Algoritmy

Algoritmy zde chápejme jako řešitel modelu problému, který je abstrakcí od
hledání cesty v bludišti.

Samotné algoritmy hledají cestu (tedy sekvenci operátorů, směrů), které 
vedou z počátečního políčka do cílového, resp. sekvenci hran, které vedou 
z počátečního uzlu grafu do toho cílového, resp. sekvenci rozhodnutí, která
ve stromu stavového prostoru vedou ke kýženému cílovému listu od svého kořene.

Aktuální verze obsahuje implementace čtyř algoritmů, které jsou všechny
(z implementačních důvodů) potomky abstraktní třídy `Algorithm`, jejíž 
definici lze nalézt 
[zde](https://github.com/vojtechpavlu/MazeRunner/blob/master/src/algorithms/algorithm.py).

Tato abstraktní třída sdružuje metody společné pro všechny ostatní algoritmy.

Obecně tyto algoritmy prochází stavový prostor pomocí dvou datových struktur:

- `fringe`, do které si ukládá stavy, které mají být dále prohledány
- `closed`, do které si ukládá stavy, které již byly prohledány. Pokud je již
daný stav v této struktuře uložen, již ho neprohledává, neboť by se točil v
  kruhu.

Samotný obecný algoritmus postupuje (v pseudo-*python*-kódu) následovně:

````python

fringe = [initial_state]

while len(fringe) > 0:
  # Připrav si aktuální stav
  current_state = fringe.remove_and_return()
  
  # Zkontroluj, zda není konečný
  if is_final_state(current_state):
    raise Success("Nalezeno řešení", current_state)
  
  # Zkontroluj, zda již nebyl prohledáván
  elif is_in_closed(current_state):
    continue

  # Jinak přidej jeho potomky
  else:
    for operator in available_operators(current_state):
      fringe.append(operator.apply(current_state))
    closed.append(current_state)

# Pokud byly prohledány všechny stavy z fringe a řešení nenalezeno
raise Failure("Řešení neexistuje")
````

Většina algoritmů se pak v praxi liší jen v přístupu k poskytování dalšího
prvku k prohledání (reprezentováno řádkem 
`current_state = fringe.remove_and_return()`).

### Slepé algoritmy prohledávání grafů

Slepé algoritmy prohledávání stavového prostoru stojí na principu rozevírání
uzlů z `fringe` postupně, ignoruje jejich vhodnost. Nepoužívají ke svému
rozhodování žádných dodaných informací, proto se jim také mnohdy říká tzv.
***neinformované algoritmy pro prohledávání stavového prostoru***.

Mezi základní zástupce bez pochyby patří prohledávání do hloubky a do šířky.

#### Depth-First Search (DFS)

Jednoduchá implementace algoritmu pro slepé (**neinformované**) prohledávání
grafu do hloubky. Tato implementace je poplatná obecnému pojetí tohoto obecného
algoritmu, který si udržuje sadu stavů k prohledání (`fringe`) realizovaný 
jako zásobník (`LIFO`). Díky tomu je schopen algoritmus procházet strom stavového 
prostoru tzv. *po větvích*. 

Na obecné úrovni negarantuje nalezení řešení (je-li stavový prostor nekonečný, 
resp. je-li jeho "levá" větev nekonečná). V tomto případě (v konečném bludišti)
je však tato možnost vyloučena.

Algoritmus ovšem negarantuje ani nalezení optimální cesty. V našem pojetí
chápeme optimalitu jen jako počet kroků k cíli.


#### Breath-First Search (BFS)

Algoritmus prakticky identický k DFS; s tím rozdílem, že jeho `fringe` je
chápána jako fronta (`FIFO`). Díky tomu je schopen algoritmus procházet
strom stavového prostoru tzv. *po vrstvách*. A díky tomu ostatně algoritmus
garantuje nejen nalezení řešení, ale garantuje i nalezení optimální cesty.

Jeho slabinou jsou ovšem vysoké nároky na paměť (velikost `fringe`). Ty rostou
exponenciálně s prohledávanou hloubkou 

$$branching^{depth}$$

kde `branching` (branching factor) odpovídá počtu operátorů aplikovatelných
na stav a `depth` odpovídá hloubce stavu.


### Heuristické algoritmy prohledávání grafů

Heuristické algoritmy pro prohledávání stavového prostoru narozdíl od algoritmů
neinformovaných ke svému rozhodování dodané informace používají. Typicky tato
informace pramení z vlastností problému.

Samotnou heuristickou funkcí, která poskytuje službu ohodnocení bonity stavu,
často bývá nějaká metrika, pro kterou platí následující pravidla:

Pro všechny stavy `s` z množiny všech stavů `S` při zobrazení kartézského
součinu mezi množinami `S` a `S` na reálná čísla 
( $s \in S, S \times S \rightarrow \mathbb{R}$ ) existuje hodnotící funkce `d`
taková, že:

1. $\forall s_{1}, s_{2} \in S, d(s_{1}, s_{2}) \geq 0$
2. $\forall s_{1}, s_{2} \in S, d(s_{1}, s_{2}) = d(s_{2}, s_{1})$
3. $\forall s_{1}, s_{2} \in S, d(s_{1}, s_{2}) = 0 \Leftrightarrow s_{1} = s_{2}$
4. $\forall s_{1}, s_{2}, s_{3} \in S, d(s_{1}, s_{2}) + d(s_{2}, s_{3}) \geq d(s_{1}, s_{3})$


V bludišti je preferována metrika euklidovské vzdálenosti, ale podobně by bylo
možné použít např. *Manhattonské vzdálenosti* (nebo také tzv. *Taxicab Distance*),
poněkud specificky by bylo možné užít *cosinové* či *hammingovy vzdálenosti*.


#### Greedy algoritmus

Hladový algoritmus je algoritmus pro uspořádané prohledávání stavového prostoru.
Jeho podstata spočívá na snaze preferovat některé cesty, které se zdají být
perspektivními před těmi, které se tak nezdají. Toho je dosaženo pomocí výběru
vždy nejvýhodnější další cesty z `fringe`.

Proto dokáže již od počátku směřovat správným směrem, ovšem za cenu poměrně 
vysokých nároků na čas a na paměť.


#### Algoritmus pro gradientní prohledávání

Gradientní prohledávání je podobný přístup, jako je u hladového algoritmu, jen
s tím rozdílem, že má pouze jednoprvkovou `fringe`. Jakmile dojde do bodu, kdy
již neexistuje zlepšení, algoritmus končí.

Tím však vzniká riziko uvíznutí v lokálním extrému. V bludišti k tomu pak dojde,
zajde-li algoritmus do slepé uličky.


#### A Star (A*)

Algoritmus prochází stavový prostor obdobně, jako předchozí dva, ale opět se
liší ve způsobu poskytování následujícího stavu k prohledání.

Algoritmus `A*` se řadí mezi algoritmy heuristické (**informované**), jeho
heuristickou (v tomto případě nákladovou) funkcí je cena cesty k dosažení
daného stavu a dolní odhad ceny k dosažení cíle.

V tomto případě je cena cesty k dosažení daného stavu chápána jako počet
aplikovaných operátorů (kroků) k dosažení daného stavu a dolní odhad ceny
k dosažení cíle je minimální možná délka cesty, v našem pojetí 2D 
ortogonálního a pravidelného prostoru tedy euklidovská vzdálenost 
(tedy délka úsečka mezi dvěma body) počítaná tradičně - pomocí pythagorovy věty
pro výpočet délky přepony.

Součet těchto cen pro každý ze stavů ve `fringe` (sady stavů k prohledání)
nám determinuje dle minima ten, který má být prohledán v další iteraci.
Jinými slovy takto vybereme ten stav, jehož prohledání nejspíš vede k cíli
nejrychleji.

Nalezení optimální cesty algoritmus `A*` v zásadě negarantuje, ale jeho výhody
v rychlosti výpočtu či ořezání již z prvu správně rozpoznaných neperspektivních
větví ho typicky řadí jako jeden z nejvýznaměnjších pro hledání cest.


### Random algoritmus

Tento algoritmus bychom mohli zařadit mezi nesystematické - své operátory
(tedy směry, kterými se dále vydá) volí na základě náhody. Často se tedy vrací.
Délka jím nalezených cest je typicky kvalitativně nesrovnatelná s ostatními, 
systematickými algoritmy; mnohdy je horší i o více řádů.

Jeho uvedení je podmíněno potřebou vymezením významu systematického 
prohledávání.