from zone import Zone, ZONE_TYPES
from map import Map
from connection import Connection


class Parser:
    """Read a map file and turn it into a Map."""

    def __init__(self, filename: str) -> None:
        """Save the name of the file to read.

        Args:
            filename: path of the map file.
        """
        self.filename = filename

    def parse(self) -> Map:
        """Read the whole file and return the Map.

        Returns:
            The map with all its zones and connections.

        Raises:
            ValueError: if the map has an error.
        """
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
        """Return (number, line) for each line, skipping empty and comments.

        Returns:
            A list of pairs (line number, line text).
        """
        lines: list[tuple[int, str]] = []
        with open(self.filename) as file:
            for number, line in enumerate(file, start=1):
                line = line.strip()
                if line != "" and not line.startswith("#"):
                    lines.append((number, line))
        return lines

    def parse_line(self, line: str, my_map: Map) -> None:
        """Check what kind of line it is and call the right method.

        Args:
            line: the line to read.
            my_map: the map where the result is saved.
        """
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
        """Read 'nb_drones: 5' and return 5.

        Args:
            line: the first line of the file.

        Returns:
            The number of drones.
        """
        if line.count(":") != 1:
            raise ValueError("la primera linea debe ser 'nb_drones: N'")
        key, value = line.split(":")
        if key != "nb_drones":
            raise ValueError("la primera linea debe ser 'nb_drones: N'")
        return self.parse_positive(key, value)

    def parse_zone(self, line: str, my_map: Map) -> None:
        """Read 'hub: roof1 3 4 [color=red]' and save the zone in the map.

        Args:
            line: the zone line.
            my_map: the map where the zone is saved.
        """
        parts = line.split()
        if len(parts) < 4:
            raise ValueError(f"zona incompleta: '{line}'")
        if "-" in parts[1]:
            raise ValueError(f"la zona '{parts[1]}' no puede llevar '-'")
        if parts[1] in my_map.zones:
            raise ValueError(f"la zona '{parts[1]}' esta repetida")
        try:
            zone = Zone(parts[1], int(parts[2]), int(parts[3]))
        except ValueError:
            raise ValueError("las coordenadas deben ser numeros enteros")

        for key, value in self.parse_metadata(parts[4:]).items():
            if key == "zone":
                if value not in ZONE_TYPES:
                    raise ValueError(f"tipo de zona no valido: '{value}'")
                zone.zone_type = value
            elif key == "color":
                zone.color = value
            elif key == "max_drones":
                if parts[0] == "hub:":
                    zone.max_drones = self.parse_positive(key, value)
            else:
                raise ValueError(f"extra no valido: '{key}={value}'")

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
        """Read 'connection: a-b [max_link_capacity=2]' and save it.

        Args:
            line: the connection line.
            my_map: the map where the connection is saved.
        """
        parts = line.split()
        if len(parts) < 2:
            raise ValueError(f"conexion incompleta: '{line}'")
        if parts[1].count("-") != 1:
            raise ValueError(f"la conexion debe ser 'a-b': '{parts[1]}'")
        name_a, name_b = parts[1].split("-")
        if name_a == name_b:
            raise ValueError("una zona no se puede conectar consigo misma")
        for name in [name_a, name_b]:
            if name not in my_map.zones:
                raise ValueError(f"la zona '{name}' no existe")
        zone_a = my_map.zones[name_a]
        zone_b = my_map.zones[name_b]
        if zone_b in my_map.get_neighbors(zone_a):
            raise ValueError(f"la conexion '{parts[1]}' esta repetida")

        connection = Connection(zone_a, zone_b)
        for key, value in self.parse_metadata(parts[2:]).items():
            if key == "max_link_capacity":
                connection.max_link_capacity = self.parse_positive(key, value)
            else:
                raise ValueError(f"extra desconocido: '{key}'")

        my_map.add_connection(connection)

    def parse_metadata(self, pieces: list[str]) -> dict[str, str]:
        """Read '[color=red max_drones=2]' and return each key with its value.

        Args:
            pieces: the parts of the line after the zone or connection.

        Returns:
            A dict like {'color': 'red', 'max_drones': '2'}.
        """
        if len(pieces) == 0:
            return {}
        text = " ".join(pieces)
        inside = text[1:-1]
        if text[0] != "[" or text[-1] != "]" or "[" in inside or "]" in inside:
            raise ValueError(f"los extras deben ir en un solo [ ]: '{text}'")
        result: dict[str, str] = {}
        for piece in inside.split():
            if piece.count("=") != 1:
                raise ValueError(f"el extra debe ser 'clave=valor': '{piece}'")
            key, value = piece.split("=")
            if key == "" or value == "":
                raise ValueError(f"al extra le falta algo: '{piece}'")
            if key in result:
                raise ValueError(f"el extra '{key}' esta repetido")
            result[key] = value
        return result

    def parse_positive(self, name: str, value: str) -> int:
        """Turn value into a number and check that it is greater than 0.

        Args:
            name: name of the value, for the error message.
            value: the text to convert.

        Returns:
            The number.
        """
        try:
            number = int(value)
        except ValueError:
            raise ValueError(f"{name} debe ser un numero: '{value.strip()}'")
        if number <= 0:
            raise ValueError(f"{name} debe ser mayor que 0")
        return number
