from zone import Zone


class Connection:
    """Un camino de ida y vuelta entre dos zonas."""

    def __init__(self, zone_a: Zone, zone_b: Zone,
                 max_link_capacity: int = 1) -> None:
        """Crea una conexion.

        Args:
            zone_a: una punta del camino.
            zone_b: la otra punta del camino.
            max_link_capacity: cuantos drones pueden ir a la vez por el.
        """
        self.zone_a = zone_a
        self.zone_b = zone_b
        self.max_link_capacity = max_link_capacity
