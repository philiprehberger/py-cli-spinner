"""Tests for philiprehberger_cli_spinner."""

from __future__ import annotations

import threading
import time

import pytest

from philiprehberger_cli_spinner import STYLES, Spinner, spin, spinner


def _force_non_tty(s: Spinner) -> Spinner:
    """Disable TTY-dependent output so tests can run in CI."""
    s._is_tty = False
    return s


def test_styles_has_known_keys() -> None:
    assert {"dots", "line", "bounce", "braille", "arrow"} <= set(STYLES)


def test_unknown_style_raises() -> None:
    with pytest.raises(ValueError, match="Unknown style"):
        Spinner("hi", style="not-a-style")


def test_factory_returns_spinner() -> None:
    s = spinner("loading")
    assert isinstance(s, Spinner)


def test_start_stop_no_tty() -> None:
    s = _force_non_tty(Spinner("loading"))
    s.start()
    assert s._thread is not None
    assert s._thread.is_alive()
    s.stop()
    assert s._thread is None


def test_context_manager() -> None:
    s = _force_non_tty(Spinner("ctx"))
    with s:
        assert s._thread is not None and s._thread.is_alive()
    assert s._thread is None


def test_update_text_thread_safe() -> None:
    s = _force_non_tty(Spinner("a"))
    s.start()
    try:
        s.update("b")
        assert s._text == "b"
    finally:
        s.stop()


def test_succeed_stops_spinner() -> None:
    s = _force_non_tty(Spinner("work"))
    s.start()
    s.succeed("done")
    assert s._thread is None


def test_fail_stops_spinner() -> None:
    s = _force_non_tty(Spinner("work"))
    s.start()
    s.fail("oops")
    assert s._thread is None


def test_warn_stops_spinner() -> None:
    s = _force_non_tty(Spinner("work"))
    s.start()
    s.warn("careful")
    assert s._thread is None


def test_info_stops_spinner() -> None:
    s = _force_non_tty(Spinner("work"))
    s.start()
    s.info("note")
    assert s._thread is None


def test_double_start_is_idempotent() -> None:
    s = _force_non_tty(Spinner())
    s.start()
    first = s._thread
    s.start()
    assert s._thread is first
    s.stop()


def test_spin_decorator_runs_function() -> None:
    captured: dict[str, int] = {}

    @spin("computing")
    def compute(x: int) -> int:
        captured["called"] = x
        return x * 2

    # decorator hides the spinner under non-tty by default
    result = compute(3)
    assert result == 6
    assert captured["called"] == 3


def test_spin_decorator_preserves_metadata() -> None:
    @spin("x")
    def my_func() -> None:
        """My docstring."""

    assert my_func.__name__ == "my_func"
    assert my_func.__doc__ == "My docstring."
