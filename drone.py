from zone import Zone


class Drone:
    """Un dron que se mueve por el mapa."""

    def __init__(self, drone_id: int, zone: Zone) -> None:
        """Crea un dron.

        Args:
            drone_id: numero del dron (1 para D1, 2 para D2...).
            zone: la zona donde esta ahora.
        """
        self.drone_id = drone_id
        self.zone = zone
