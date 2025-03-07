# Scryfall-py

An async Scryfall API wrapper written in Python

## Usage

### Installation

To get started, install `scryfall-py`

`pip install scryfall-py`

### Getting started

```py
from scryfall import Scryfall
client = Scryfall()

card = await client.search_cards_named("Arcades, the Strategist")
```

This will fetch the card Arcades, the Strategist from the Scryfall API

## Documentation

Documentation is located at [GitHub Pages](https://zevaryx.github.io/scryfall-py/)
