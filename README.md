# Solar System Planets

A Python command-line application that stores data for the 8 planets in our solar system and answers questions about each planet, including mass, distance from the Sun, and moons.

It supports two ways of interacting:
- **Menu mode**: choose numbered options for common actions (reliable and clear).
- **Free-text mode**: ask natural questions and the program will detect what you mean (details, mass, distance, moons, membership).

## Features
- Loads planet data from `data/planets.json`
- Uses classes throughout (model + catalogue + query engine)
- Validates data and handles errors cleanly (no crashes on bad input)
- Supports case-insensitive input (for example: `saturn`, `SATURN`, `SaTuRn`)
- Offers suggestions for close matches (for example: `saturnn`)

## How to run
From the project root:

```bash
python -m src.main
```

## How to run tests
From the project root:

```bash
python -m unittest -v
```

## How to use

### Menu mode

Run the program and choose options like:

- **1** to list planets  
- **2** to show full planet details  
- **3** to show mass  
- **4** to show distance from the Sun  
- **5** to show moon count  
- **6** to check if a name is in the planet list  
- **7** to ask a free-text question  

### Free-text mode

Choose option **7** and type a question.

#### Example questions you can ask

- **Details**
  - Tell me everything about Saturn
  - Show details for Jupiter
  - What do you know about Mars

- **Mass**
  - How massive is Neptune
  - What is the mass of Earth
  - How much does Venus weigh

- **Distance**
  - How far is Mars from the Sun
  - What is the distance of Mercury from the Sun
  - Distance from the Sun for Uranus

- **Moons**
  - How many moons does Earth have
  - How many moons does Jupiter have
  - List the moons of Mars
  - What are Saturn’s moons

- **Membership**
  - Is Pluto in the list of planets
  - Is Earth a planet
  - Is Ceres in the list of planets

## Project structure

- `src/` application source code  
  - `models/` data models (for example: `Planet`)  
  - `services/` catalogue, query engine, and formatting  
  - `utils/` shared helpers and custom errors  
- `data/planets.json` planet dataset used by the program  
- `tests/` unit tests (run with `unittest`)  
- `docs/TEST_PLAN.md` written test plan  
- `docs/AI_TRANSPARENCY.md` AI transparency statement (AITS 2)  

## Data sources

- Planet mass and distance values are approximate and were taken from Wikipedia during development.
- Moon lists are intentionally not exhaustive for large planets.

## Notes

- This project does not use a relational database.
- Inputs and dataset fields are validated to keep the program predictable.

### -------------------------------------------------------------------------------------------------

## References (external)

### Python documentation
- https://docs.python.org/3/tutorial/classes.html
- https://docs.python.org/3/library/enum.html
- https://docs.python.org/3/howto/enum.html
- https://docs.python.org/3/library/unittest.html
- https://docs.python.org/3/library/unittest.mock.html
- https://docs.python.org/3/library/json.html
- https://docs.python.org/3/library/pathlib.html
- https://docs.python.org/3/library/difflib.html
- https://docs.python.org/3/library/re.html
- https://docs.python.org/3/library/cmd.html
- https://docs.python.org/3/library/typing.html

### Stack Overflow (similar patterns and discussions)
- https://stackoverflow.com/questions/58016434/inheritance-extending-a-from-json-function-in-super-but-it-makes-an-instance-of
- https://stackoverflow.com/questions/62212855/how-to-create-objects-from-jsons-in-python-with-a-complex-constructor
- https://stackoverflow.com/questions/71462500/best-way-to-use-a-json-to-create-class-objects-in-python
- https://stackoverflow.com/questions/69773539/how-do-i-convert-a-json-file-to-a-python-class
- https://stackoverflow.com/questions/40667782/techniques-other-than-regex-to-discover-intent-in-sentences
- https://stackoverflow.com/questions/64874054/whats-a-good-way-to-match-text-to-sets-of-keywords-nlp
- https://stackoverflow.com/questions/44897645/query-using-nlp-python
