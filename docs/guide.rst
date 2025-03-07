Usage
===============

Installation
************

To get started, install ``scryfall-py``::

    pip install scryfall-py


Getting Started
***************

.. code-block:: python

    from scryfall import Scryfall
    client = Scryfall()

    card = await client.search_cards_named("Arcades, the Strategist")

This will fetch the card Arcades, the Strategist from the Scryfall API
