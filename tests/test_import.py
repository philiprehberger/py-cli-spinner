"""Basic import test."""


def test_import():
    """Verify the package can be imported."""
    import philiprehberger_cli_spinner
    assert hasattr(philiprehberger_cli_spinner, "__name__") or True
