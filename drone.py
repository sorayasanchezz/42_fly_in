from zone import Zone


class Drone:
    """A drone that moves across the map."""

    def __init__(self, drone_id: int, path: list[Zone]) -> None:
        """Create a drone.

        Args:
            drone_id: number of the drone (1 for D1, 2 for D2...).
            path: the path it must follow, from start to end.
        """
        self.drone_id = drone_id
        self.path = path
        self.zone = path[0]
        self.step = 0
        self.flying_to: Zone | None = None

    def next_zone(self) -> Zone:
        """Return the next zone of its path.

        Returns:
            The zone it has to go to now.
        """
        return self.path[self.step + 1]
