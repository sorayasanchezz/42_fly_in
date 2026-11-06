from zone import Zone
from map import Map
from connection import Connection


class Parser:
    """Lee un archivo de mapa y lo convierte en un Map."""

    def __init__(self, filename: str) -> None:
        self.filename = filename

    def parse(self) -> Map:
        """Lee el archivo entero y devuelve el Map."""
        lines = self.read_lines()
        if len(lines) == 0:
            raise ValueError("el archivo esta vacio")

        my_map = Map()
        for number, line in lines:
            try:
                self.parse_line(line, my_map)
            except ValueError as error:
                raise ValueError(f"linea {number}: {error}")

        if my_map.start is None:
            raise ValueError("falta el start_hub")
        if my_map.end is None:
            raise ValueError("falta el end_hub")
        return my_map

    def read_lines(self) -> list[tuple[int, str]]:
        """Devuelve (numero, linea) de cada linea sin vacias ni comentarios."""
        lines: list[tuple[int, str]] = []
        with open(self.filename) as file:
            for number, line in enumerate(file, start=1):
                line = line.strip()
                if line != "" and not line.startswith("#"):
                    lines.append((number, line))
        return lines

    def parse_line(self, line: str, my_map: Map) -> None:
        """Mira que tipo de linea es y llama a la funcion que toca."""
        first_word = line.split()[0]
        if my_map.nb_drones == 0:
            my_map.nb_drones = self.parse_nb_drones(line)
        elif first_word in ["start_hub:", "hub:", "end_hub:"]:
            self.parse_zone(line, my_map)
        elif first_word == "connection:":
            self.parse_connection(line, my_map)
        else:
            raise ValueError(f"linea desconocida: '{line}'")

    def parse_nb_drones(self, line: str) -> int:
        """Lee 'nb_drones: 5' y devuelve 5."""
        key, value = line.split(":")
        if key != "nb_drones":
            raise ValueError("la primera linea debe ser 'nb_drones: N'")
        return self.parse_positive(key, value)

    def parse_zone(self, line: str, my_map: Map) -> None:
        """Lee 'hub: roof1 3 4 [color=red]' y guarda la zona en el mapa."""
        parts = line.split()
        if len(parts) < 4:
            raise ValueError(f"zona incompleta: '{line}'")
        if "-" in parts[1]:
            raise ValueError(f"la zona '{parts[1]}' no puede llevar '-'")
        if parts[1] in my_map.zones:
            raise ValueError(f"la zona '{parts[1]}' esta repetida")
        zone = Zone(parts[1], int(parts[2]), int(parts[3]))

        for key, value in self.parse_metadata(parts[4:]):
            if key == "zone":
                if value not in ["normal", "blocked", "restricted",
                                 "priority"]:
                    raise ValueError(f"tipo de zona desconocido: '{value}'")
                zone.zone_type = value
            elif key == "color":
                zone.color = value
            elif key == "max_drones":
                zone.max_drones = self.parse_positive(key, value)
            else:
                raise ValueError(f"extra desconocido: '{key}'")

        my_map.add_zone(zone)
        if parts[0] == "start_hub:":
            if my_map.start is not None:
                raise ValueError("hay mas de un start_hub")
            zone.max_drones = my_map.nb_drones
            my_map.start = zone
        elif parts[0] == "end_hub:":
            if my_map.end is not None:
                raise ValueError("hay mas de un end_hub")
            zone.max_drones = my_map.nb_drones
            my_map.end = zone

    def parse_connection(self, line: str, my_map: Map) -> None:
        """Lee 'connection: a-b [max_link_capacity=2]' y la guarda."""
        parts = line.split()
        if len(parts) < 2:
            raise ValueError(f"conexion incompleta: '{line}'")
        name_a, name_b = parts[1].split("-")
        for name in [name_a, name_b]:
            if name not in my_map.zones:
                raise ValueError(f"la zona '{name}' no existe")
        for old in my_map.connections:
            if {old.zone_a.name, old.zone_b.name} == {name_a, name_b}:
                raise ValueError(f"la conexion '{parts[1]}' esta repetida")

        connection = Connection(my_map.zones[name_a], my_map.zones[name_b])
        for key, value in self.parse_metadata(parts[2:]):
            if key == "max_link_capacity":
                connection.max_link_capacity = self.parse_positive(key, value)
            else:
                raise ValueError(f"extra desconocido: '{key}'")

        my_map.add_connection(connection)

    def parse_metadata(self, pieces: list[str]) -> list[tuple[str, str]]:
        """Lee '[color=red max_drones=2]' y devuelve las parejas."""
        if len(pieces) == 0:
            return []
        text = " ".join(pieces)
        inside = text[1:-1]
        if text[0] != "[" or text[-1] != "]" or "[" in inside or "]" in inside:
            raise ValueError(f"los extras deben ir en un solo [ ]: '{text}'")
        result: list[tuple[str, str]] = []
        for piece in inside.split():
            key, value = piece.split("=")
            result.append((key, value))
        return result

    def parse_positive(self, name: str, value: str) -> int:
        """Convierte value en numero y comprueba que sea mayor que 0."""
        number = int(value)
        if number <= 0:
            raise ValueError(f"{name} debe ser mayor que 0")
        return number
