import webcolors  # type: ignore[import, unused-ignore]

NORMAL = "normal"
BLOCKED = "blocked"
RESTRICTED = "restricted"
PRIORITY = "priority"
ZONE_TYPES = [NORMAL, BLOCKED, RESTRICTED, PRIORITY]


class Zone:
    """A zone (a place) of the map where drones can be."""

    def __init__(self, name: str, x: int, y: int) -> None:
        """Create a normal zone, with no color, that fits 1 drone.

        Args:
            name: name of the zone.
            x: x coordinate.
            y: y coordinate.
        """
        self.name = name
        self.x = x
        self.y = y
        self.zone_type = NORMAL
        self.color: str | None = None
        self.max_drones = 1
        self.count = 0
        self.load = 0

    def is_full(self) -> bool:
        """Tell if the zone already has max_drones drones.

        Returns:
            True if it is full, False if one more drone fits.
        """
        return self.count >= self.max_drones

    def paint(self, text: str) -> str:
        """Return text painted with the color of the zone.

        Args:
            text: the text to paint.

        Returns:
            The colored text, or the same text if the color is unknown.
        """
        if self.color is None:
            return text
        try:
            red, green, blue = webcolors.name_to_rgb(self.color)
        except ValueError:
            return text
        return f"\033[38;2;{red};{green};{blue}m{text}\033[0m"

    def get_cost(self) -> float:
        """Tell how much it costs to enter this zone.

        Returns:
            The cost of the zone type, plus the drones already using it.
        """
        extra = self.load / self.max_drones
        if self.zone_type == RESTRICTED:
            return 2 + extra
        if self.zone_type == PRIORITY:
            return 0.9 + extra
        return 1 + extra
