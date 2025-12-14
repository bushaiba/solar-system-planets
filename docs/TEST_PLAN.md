# Test Plan: Solar System Planets

## Purpose
Verify that the program correctly answers planet queries, validates inputs, and behaves predictably for invalid inputs.

## Scope
In scope:
- Data loading and validation from JSON
- Planet lookup and membership checks
- Menu usability (numbers and keywords)
- Free-text question mode (intent detection + planet extraction)
- Error handling and user prompts

Out of scope:
- GUI features
- Network calls

## Test environment
- Python 3.x
- Run app: `python -m src.main`
- Run tests: `python -m unittest`

## Test cases

| ID | Area | Scenario | Input | Expected result | Type |
|---|---|---|---|---|---|
| TC01 | Data | Valid JSON loads | start app | menu shows, planets available | Automated |
| TC02 | Data | Missing field rejected | remove `mass_kg` from one planet | clear validation error | Automated |
| TC03 | Menu | List planets | option `1` | prints 8 planet names | Manual |
| TC04 | Menu | Invalid option | `99` | shows invalid option message, no crash | Manual |
| TC05 | Query | Details | `Tell me everything about Saturn` | full formatted details | Automated |
| TC06 | Query | Mass | `How massive is Neptune` | prints Neptune mass | Automated |
| TC07 | Query | Moon count | `How many moons does Earth have` | prints 1 | Automated |
| TC08 | Query | Moon list | `List the moons of Mars` | prints Phobos, Deimos | Automated |
| TC09 | Query | Membership (not in list) | `Is Pluto in the list of planets` | says No | Automated |
| TC10 | Query | Misspelling suggestion | `How massive is saturnn` | suggests Saturn or answers via suggestion flow | Automated |
| TC11 | Validation | Empty question | empty input in question mode | prompts user or returns message | Manual |
| TC12 | Resilience | Unknown planet | `Tell me about Krypton` | helpful error + list or suggestions | Automated |
