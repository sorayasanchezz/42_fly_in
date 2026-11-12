from zone import Zone


class Connection:
    """A two-way link between two zones."""

    def __init__(self, zone_a: Zone, zone_b: Zone) -> None:
        """Create a connection between zone_a and zone_b that fits 1 drone.

        Args:
            zone_a: one end of the connection.
            zone_b: the other end of the connection.
        """
        self.zone_a = zone_a
        self.zone_b = zone_b
        self.max_link_capacity = 1
        self.count = 0

    def is_full(self) -> bool:
        """Tell if max_link_capacity drones already cross it this turn.

        Returns:
            True if it is full, False if one more drone fits.
        """
        return self.count >= self.max_link_capacity
