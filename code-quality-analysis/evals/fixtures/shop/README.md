# Small shop fixture

Preferred customers receive a 10% discount both in previews and at checkout.
`receipt` is a plugin loaded by name through `loader.py`; it is not imported directly.
The command-line UI intentionally calls the order service directly. There is only
one service implementation and no requirement to swap it. This fixture uses only
the Python standard library. To inspect current behavior, run:

```sh
python3 -c 'from orders import preview_total, checkout_total; print(preview_total(100, True), checkout_total(100, True))'
```

No network, database, or installed application is needed. The disagreement between
preview and checkout is intentional evaluation data, not production code.
