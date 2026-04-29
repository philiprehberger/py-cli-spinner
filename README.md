# philiprehberger-cli-spinner

[![Tests](https://github.com/philiprehberger/py-cli-spinner/actions/workflows/publish.yml/badge.svg)](https://github.com/philiprehberger/py-cli-spinner/actions/workflows/publish.yml)
[![PyPI version](https://img.shields.io/pypi/v/philiprehberger-cli-spinner.svg)](https://pypi.org/project/philiprehberger-cli-spinner/)
[![Last updated](https://img.shields.io/github/last-commit/philiprehberger/py-cli-spinner)](https://github.com/philiprehberger/py-cli-spinner/commits/main)

Dead-simple terminal spinners and progress indicators for CLI scripts.

## Installation

```bash
pip install philiprehberger-cli-spinner
```

## Usage

```python
from philiprehberger_cli_spinner import spinner

with spinner("Loading data"):
    do_work()
```

### Finish with status

```python
from philiprehberger_cli_spinner import spinner

s = spinner("Deploying")
s.start()
try:
    deploy()
    s.succeed("Deployed successfully")
except Exception:
    s.fail("Deploy failed")
```

### Decorator

```python
from philiprehberger_cli_spinner import spin

@spin("Computing")
def heavy_task():
    ...
```

### Update text

```python
from philiprehberger_cli_spinner import spinner

with spinner("Step 1") as s:
    step_one()
    s.update("Step 2")
    step_two()
```

### Styles

Five built-in animation styles are available:

```python
from philiprehberger_cli_spinner import spinner

with spinner("Working", style="braille"):
    do_work()
```

Available styles: `dots`, `line`, `bounce`, `braille`, `arrow`.

## API

| Function / Method | Description |
|---|---|
| `spinner(text, *, style)` | Create a `Spinner` (context manager) |
| `spin(text, *, style)` | Decorator that shows a spinner during execution |
| `Spinner.start()` | Start the spinner animation |
| `Spinner.stop()` | Stop the spinner and clear the line |
| `Spinner.update(text)` | Change the displayed text |
| `Spinner.succeed(text)` | Stop with a success symbol |
| `Spinner.fail(text)` | Stop with a failure symbol |
| `Spinner.warn(text)` | Stop with a warning symbol |
| `Spinner.info(text)` | Stop with an info symbol |

## Development

```bash
pip install -e .
python -m pytest tests/ -v
```

## Support

If you find this project useful:

⭐ [Star the repo](https://github.com/philiprehberger/py-cli-spinner)

🐛 [Report issues](https://github.com/philiprehberger/py-cli-spinner/issues?q=is%3Aissue+is%3Aopen+label%3Abug)

💡 [Suggest features](https://github.com/philiprehberger/py-cli-spinner/issues?q=is%3Aissue+is%3Aopen+label%3Aenhancement)

❤️ [Sponsor development](https://github.com/sponsors/philiprehberger)

🌐 [All Open Source Projects](https://philiprehberger.com/open-source-packages)

💻 [GitHub Profile](https://github.com/philiprehberger)

🔗 [LinkedIn Profile](https://www.linkedin.com/in/philiprehberger)

## License

[MIT](LICENSE)
