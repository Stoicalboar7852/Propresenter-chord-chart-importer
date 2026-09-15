"""PyInstaller entry point.

PyInstaller needs a script, not a module, so this is the one line that turns the
``pcci`` package into a frozen executable.
"""

from pcci.cli import main

if __name__ == "__main__":
    main()
