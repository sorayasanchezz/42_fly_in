class Zone:
    """Una zona (un sitio) del mapa donde pueden estar los drones."""

    def __init__(self, name: str, x: int, y: int,
                 zone_type: str = "normal",
                 color: str | None = None,
                 max_drones: int = 1) -> None:
        """Crea una zona.

        Args:
            name: nombre de la zona, sin '-' ni espacios.
            x: coordenada x (horizontal).
            y: coordenada y (vertical).
            zone_type: 'normal', 'blocked', 'restricted' o 'priority'.
            color: color para dibujarla, o None si no tiene.
            max_drones: cuantos drones caben a la vez.
        """
        self.name = name
        self.x = x
        self.y = y
        self.zone_type = zone_type
        self.color = color
        self.max_drones = max_drones
