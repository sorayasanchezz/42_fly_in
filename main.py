import sys

from parser import Parser


def main() -> None:
    """Arranca el programa: lee el mapa y ensena los errores sin romperse.

    Uso: python3 main.py <archivo_de_mapa>
    """
    if len(sys.argv) != 2:
        print("Uso: python3 main.py <archivo_de_mapa>", file=sys.stderr)
        sys.exit(1)

    try:
        my_map = Parser(sys.argv[1]).parse()
    except OSError as error:
        print(f"Error: no se puede abrir el archivo: {error}",
              file=sys.stderr)
        sys.exit(1)
    except ValueError as error:
        print(f"Error en el mapa: {error}", file=sys.stderr)
        sys.exit(1)

    print(f"Mapa leido: {my_map.nb_drones} drones, "
          f"{len(my_map.zones)} zonas, "
          f"{len(my_map.connections)} conexiones")


if __name__ == "__main__":
    main()
