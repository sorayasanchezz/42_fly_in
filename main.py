import sys

from parser import Parser
from simulation import Simulation


def main() -> None:
    """Start the program: read the map and show errors without crashing.

    Usage: python3 main.py <map_file>
    """
    if len(sys.argv) != 2:
        print("Uso: python3 main.py <archivo_de_mapa>", file=sys.stderr)
        sys.exit(1)

    try:
        my_map = Parser(sys.argv[1]).parse()
        Simulation(my_map).run()
    except OSError as error:
        print(f"Error: no se puede abrir el archivo: {error}",
              file=sys.stderr)
        sys.exit(1)
    except UnicodeDecodeError:
        print("Error: el archivo no es de texto", file=sys.stderr)
        sys.exit(1)
    except ValueError as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
