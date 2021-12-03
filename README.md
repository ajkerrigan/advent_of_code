# Advent of Code

Some fumbling and experimenting with [Advent of Code](https://adventofcode.com/) challenges.

## Usage

To play with these solutions yourself...

### Install dependencies

* [Python](https://realpython.com/installing-python/) 3.10+
* [Poetry](https://python-poetry.org/docs/#installation)
* [Just](https://github.com/casey/just#installation)

### Install Python packages

```bash
poetry install
```

### Play

Run `just` to see available commands. Most are for preparing to _solve_ challenges, but some
also run existing solutions. To run the Python-based solution for day 1:

```bash
just run 1
```

To run the [VisiData](https://www.visidata.org/) solution for day 2, part 1:

```bash
just run_vd 2 1
```
