from zone import Zone, BLOCKED
from connection import Connection


class Map:
    """The whole map: drones, zones, connections, start and end."""

    def __init__(self) -> None:
        """Create an empty map, later filled by the Parser."""
        self.nb_drones: int = 0
        self.zones: dict[str, Zone] = {}
        self.connections: list[Connection] = []
        self.start: Zone | None = None
        self.end: Zone | None = None

    def add_zone(self, zone: Zone) -> None:
        """Save a zone in the map.

        Args:
            zone: the zone to save.
        """
        self.zones[zone.name] = zone

    def add_connection(self, connection: Connection) -> None:
        """Save a connection in the map.

        Args:
            connection: the connection to save.
        """
        self.connections.append(connection)

    def get_neighbors(self, zone: Zone) -> list[Zone]:
        """Return the zones directly connected to zone.

        Args:
            zone: the zone whose neighbors we want.

        Returns:
            The list of neighbor zones.
        """
        neighbors: list[Zone] = []
        for connection in self.connections:
            if connection.zone_a == zone:
                neighbors.append(connection.zone_b)
            elif connection.zone_b == zone:
                neighbors.append(connection.zone_a)
        return neighbors

    def get_connection(self, zone_a: Zone, zone_b: Zone) -> Connection:
        """Return the connection that joins zone_a and zone_b.

        Args:
            zone_a: one end of the connection.
            zone_b: the other end of the connection.

        Returns:
            The connection between the two zones.

        Raises:
            ValueError: if there is no connection between them.
        """
        for connection in self.connections:
            if {connection.zone_a, connection.zone_b} == {zone_a, zone_b}:
                return connection
        raise ValueError(f"no hay conexion {zone_a.name}-{zone_b.name}")

    def find_path(self) -> list[Zone]:
        """Find the cheapest path from start to end.

        Returns:
            The zones of the path, from start to end, or [] if there is none.
        """
        if self.start is None or self.end is None:
            return []
        cost: dict[Zone, float] = {self.start: 0}
        came_from: dict[Zone, Zone] = {}
        queue: list[Zone] = [self.start]
        while len(queue) > 0:
            zone = min(queue, key=lambda other: cost[other])
            queue.remove(zone)
            for neighbor in self.get_neighbors(zone):
                if neighbor.zone_type != BLOCKED:
                    new_cost = cost[zone] + neighbor.get_cost()
                    if neighbor not in cost or new_cost < cost[neighbor]:
                        cost[neighbor] = new_cost
                        came_from[neighbor] = zone
                        if neighbor not in queue:
                            queue.append(neighbor)

        if self.end not in cost:
            return []
        zone = self.end
        path: list[Zone] = [zone]
        while zone != self.start:
            zone = came_from[zone]
            path.append(zone)
        path.reverse()
        return path
