import sys

from map import Map
from drone import Drone
from zone import RESTRICTED


class Simulation:
    """Move the drones turn by turn from start to end."""

    def __init__(self, my_map: Map) -> None:
        """Create the drones and find a path for each one.

        Args:
            my_map: the map already read by the Parser.

        Raises:
            ValueError: if there is no path from start to end.
        """
        self.my_map = my_map
        self.drones: list[Drone] = []
        for number in range(1, my_map.nb_drones + 1):
            path = my_map.find_path()
            if len(path) == 0:
                raise ValueError("there is no path from start to end")
            for zone in path:
                zone.load = zone.load + 1
            path[0].count = path[0].count + 1
            self.drones.append(Drone(number, path))

    def play_turn(self) -> list[str]:
        """Play one turn and return the moves, like 'D1-waypoint1'.

        Returns:
            The list of moves of this turn.
        """
        moves: list[str] = []
        for connection in self.my_map.connections:
            connection.count = 0
        for drone in self.drones:
            if drone.flying_to is not None:
                link = self.my_map.get_connection(drone.zone, drone.flying_to)
                link.count = link.count + 1
        waiting = list(self.drones)
        moved = True
        while moved:
            moved = False
            for drone in list(waiting):
                text = self.move_drone(drone)
                if text is not None:
                    moves.append(text)
                    waiting.remove(drone)
                    moved = True
        return moves

    def move_drone(self, drone: Drone) -> str | None:
        """Move a drone one step and return the text, or None if it waits.

        Args:
            drone: the drone to move.

        Returns:
            The move, like 'D1-roof1', or None if the drone waits.
        """
        if drone.flying_to is not None:
            text = drone.flying_to.paint(
                f"D{drone.drone_id}-{drone.flying_to.name}")
            drone.zone = drone.flying_to
            drone.flying_to = None
            return text
        if drone.zone == self.my_map.end:
            return None
        next_zone = drone.next_zone()
        connection = self.my_map.get_connection(drone.zone, next_zone)
        if next_zone.is_full() or connection.is_full():
            return None
        drone.zone.count = drone.zone.count - 1
        next_zone.count = next_zone.count + 1
        connection.count = connection.count + 1
        drone.step = drone.step + 1
        if next_zone.zone_type == RESTRICTED:
            drone.flying_to = next_zone
            name = drone.zone.name + "-" + next_zone.name
        else:
            name = next_zone.name
            drone.zone = next_zone
        return next_zone.paint(f"D{drone.drone_id}-{name}")

    def all_arrived(self) -> bool:
        """Tell if every drone is already at end.

        Returns:
            True if all of them arrived, False if one is missing.
        """
        for drone in self.drones:
            if drone.zone != self.my_map.end:
                return False
        return True

    def run(self) -> None:
        """Play turns until every drone arrives and print them.

        Raises:
            ValueError: if no drone can move in a turn.
        """
        while not self.all_arrived():
            moves = self.play_turn()
            if len(moves) == 0:
                raise ValueError("the drones are stuck")
            print(" ".join(moves))
            print(self.zone_states(), file=sys.stderr)

    def zone_states(self) -> str:
        """Return how many drones are in each zone that has drones.

        Returns:
            A line like 'zones: start:2 roof1:1 goal:3', with colors.
        """
        states: list[str] = []
        for zone in self.my_map.zones.values():
            if zone.count > 0:
                states.append(zone.paint(f"{zone.name}:{zone.count}"))
        return "    zones: " + " ".join(states)
