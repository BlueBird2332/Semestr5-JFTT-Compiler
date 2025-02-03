# Kompilator JFTT

## Instalacja

1. Sklonuj repozytorium lub rozpakuj plik 272351.zip:
```bash
git clone https://github.com/BlueBird2332/Semestr5-JFTT-Compiler.git
cd Semestr5-JFTT-Compiler
```
2. W katalogu projektu stwórz i aktywuj środowisko wirtualne:
```bash
# Stwórz venv
python -m venv venv

# Aktywuj venv (Linux/macOS)
source venv/bin/activate
```

3. Zainstaluj wymagane pakiety pythona:
```bash
pip  install requirements.txt

# Zainstaluj pakiet kompilatora
cd src
pip install -e .
cd ..
```

## Uruchomienie kompilatora

```bash
python scripts/compile.py <plik_wejściowy> <plik_wyjściowy>
```

## W razie problemów

Jeśli występują błędy z importem modułów, upewnij się że:
1. Środowisko wirtualne jest aktywne (w konsoli powinno być widoczne `(venv)`)
2. Wszystkie pakiety zostały poprawnie zainstalowane (`pip list`)
3. Jesteś w głównym katalogu projektu

# Struktura projektu - opis katalogów

## `src/
Główny kod kompilatora

## `scripts/`
Skrypty narzędziowe:
- `compile.py` - główny skrypt kompilacji
- `comple.sh` - wrapper do kompilacji
- `rebuild_tree.sh` - skrypt do przebudowy gramatyki Tree-sitter

## `tree-sitter-jftt/`
Parser i gramatyka języka:
- `grammar.js` - definicja gramatyki
- `bindings/python/` - integracja z Pythonem (niezbędne pliki bindingów)
- `src/` - pliki źródłowe parsera
  - `parser.c`
  - `grammar.json`
  - `node-types.json`
  - `tree_sitter/` - pliki nagłówkowe parsera