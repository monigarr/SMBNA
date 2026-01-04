def test_run_simulation_imports():
    """
    Smoke test: ensure simulation entrypoint imports cleanly.
    Execution behavior is validated via experiment artifacts,
    not unit-level assertions.
    """
    import smbna.simulation.run_simulation
