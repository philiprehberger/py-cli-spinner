"""Dead-simple terminal spinners and progress indicators for CLI scripts."""

from __future__ import annotations

import sys
import threading
import time
from typing import Any, Callable, TypeVar

__all__ = ["Spinner", "spinner", "spin", "STYLES"]

F = TypeVar("F", bound=Callable[..., Any])

STYLES: dict[str, tuple[str, ...]] = {
    "dots": ("⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"),
    "line": ("-", "\\", "|", "/"),
    "bounce": ("⠁", "⠂", "⠄", "⠂"),
    "braille": ("⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷"),
    "arrow": ("←", "↖", "↑", "↗", "→", "↘", "↓", "↙"),
}

_INTERVAL = 0.08


class Spinner:
    """A terminal spinner that runs in a background thread.

    Can be used as a context manager or controlled manually with
    :meth:`start` / :meth:`stop`.
    """

    def __init__(self, text: str = "", *, style: str = "dots") -> None:
        if style not in STYLES:
            raise ValueError(
                f"Unknown style {style!r}. "
                f"Available: {', '.join(sorted(STYLES))}"
            )
        self._text = text
        self._frames = STYLES[style]
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None
        self._is_tty = hasattr(sys.stderr, "isatty") and sys.stderr.isatty()
        self._lock = threading.Lock()

    # -- public API -----------------------------------------------------------

    def start(self) -> Spinner:
        """Start the spinner animation in a background thread."""
        if self._thread is not None and self._thread.is_alive():
            return self
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._animate, daemon=True)
        self._thread.start()
        return self

    def stop(self) -> None:
        """Stop the spinner and clear the line."""
        self._stop_event.set()
        if self._thread is not None:
            self._thread.join()
            self._thread = None
        self._clear_line()

    def update(self, text: str) -> None:
        """Update the spinner text while it is running."""
        with self._lock:
            self._text = text

    def succeed(self, text: str | None = None) -> None:
        """Stop the spinner and show a success message."""
        self._finish("✔", text)

    def fail(self, text: str | None = None) -> None:
        """Stop the spinner and show a failure message."""
        self._finish("✖", text)

    def warn(self, text: str | None = None) -> None:
        """Stop the spinner and show a warning message."""
        self._finish("⚠", text)

    # -- context manager ------------------------------------------------------

    def __enter__(self) -> Spinner:
        return self.start()

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: Any,
    ) -> None:
        self.stop()

    # -- internals ------------------------------------------------------------

    def _animate(self) -> None:
        idx = 0
        while not self._stop_event.is_set():
            if self._is_tty:
                frame = self._frames[idx % len(self._frames)]
                with self._lock:
                    text = self._text
                line = f"\r{frame} {text}" if text else f"\r{frame}"
                sys.stderr.write(line)
                sys.stderr.flush()
                idx += 1
            self._stop_event.wait(_INTERVAL)

    def _clear_line(self) -> None:
        if self._is_tty:
            sys.stderr.write("\r\033[K")
            sys.stderr.flush()

    def _finish(self, symbol: str, text: str | None) -> None:
        self.stop()
        with self._lock:
            msg = text if text is not None else self._text
        if self._is_tty:
            sys.stderr.write(f"\r{symbol} {msg}\n")
            sys.stderr.flush()


def spinner(text: str = "", *, style: str = "dots") -> Spinner:
    """Create a :class:`Spinner` instance.

    Typical usage as a context manager::

        with spinner("Loading data"):
            do_work()
    """
    return Spinner(text, style=style)


def spin(text: str = "", *, style: str = "dots") -> Callable[[F], F]:
    """Decorator that shows a spinner while the wrapped function runs.

    Example::

        @spin("Computing")
        def heavy_task():
            ...
    """

    def decorator(func: F) -> F:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            with Spinner(text, style=style):
                return func(*args, **kwargs)

        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__
        wrapper.__module__ = func.__module__
        wrapper.__qualname__ = func.__qualname__
        wrapper.__wrapped__ = func  # type: ignore[attr-defined]
        return wrapper  # type: ignore[return-value]

    return decorator
