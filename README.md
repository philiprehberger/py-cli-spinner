# philiprehberger-cli-spinner

[![Tests](https://github.com/philiprehberger/py-cli-spinner/actions/workflows/publish.yml/badge.svg)](https://github.com/philiprehberger/py-cli-spinner/actions/workflows/publish.yml)
[![PyPI version](https://img.shields.io/pypi/v/philiprehberger-cli-spinner.svg)](https://pypi.org/project/philiprehberger-cli-spinner/)
[![License](https://img.shields.io/github/license/philiprehberger/py-cli-spinner)](LICENSE)

Dead-simple terminal spinners and progress indicators for CLI scripts.

## Install

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

## License

MIT
