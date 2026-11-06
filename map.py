from zone import Zone
from connection import Connection


class Map:
    """El mapa entero: drones, zonas, conexiones, salida y llegada."""

    def __init__(self) -> None:
        """Crea un mapa vacio, que luego llena el Parser."""
        self.nb_drones: int = 0
        self.zones: dict[str, Zone] = {}
        self.connections: list[Connection] = []
        self.start: Zone | None = None
        self.end: Zone | None = None

    def add_zone(self, zone: Zone) -> None:
        """Guarda una zona en el mapa.

        Args:
            zone: la zona que hay que guardar.
        """
        self.zones[zone.name] = zone

    def add_connection(self, connection: Connection) -> None:
        """Guarda una conexion en el mapa.

        Args:
            connection: la conexion que hay que guardar.
        """
        self.connections.append(connection)
