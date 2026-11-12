import sys

from parser import Parser
from simulation import Simulation


def main() -> None:
    """Start the program: read the map and show errors without crashing.

    Usage: python3 main.py <map_file>
    """
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <map_file>", file=sys.stderr)
        sys.exit(1)

    try:
        my_map = Parser(sys.argv[1]).parse()
        Simulation(my_map).run()
    except OSError as error:
        print(f"Error: cannot open the file: {error}",
              file=sys.stderr)
        sys.exit(1)
    except UnicodeDecodeError:
        print("Error: the file is not a text file", file=sys.stderr)
        sys.exit(1)
    except ValueError as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
