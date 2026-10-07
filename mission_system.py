class MissionSystem:

    def __init__(self):

        self.missions = {

            1: {
                1: {
                    "name": "First Drive",
                    "objective": "Reach the destination",
                    "type": "TIME"
                },

                2: {
                    "name": "Safe Driver",
                    "objective": "Reach the destination with no more than 2 collisions",
                    "type": "COLLISION"
                },

                3: {
                    "name": "Fuel Saver",
                    "objective": "Reach the destination while conserving fuel",
                    "type": "FUEL"
                }
            },

            2: {
                1: {
                    "name": "Traffic Challenge",
                    "objective": "Reach the destination through traffic",
                    "type": "TRAFFIC"
                },

                2: {
                    "name": "Obstacle Run",
                    "objective": "Avoid obstacles and reach the destination",
                    "type": "OBSTACLE"
                },

                3: {
                    "name": "Fast Route",
                    "objective": "Reach the destination quickly",
                    "type": "TIME"
                }
            },

            3: {
                1: {
                    "name": "Smart Route",
                    "objective": "Use an efficient route",
                    "type": "ROUTE"
                },

                2: {
                    "name": "Heavy Traffic",
                    "objective": "Survive heavy traffic",
                    "type": "TRAFFIC"
                },

                3: {
                    "name": "Safe Journey",
                    "objective": "Complete the mission with minimal collisions",
                    "type": "COLLISION"
                }
            },

            4: {
                1: {
                    "name": "Night Drive",
                    "objective": "Reach the destination safely at night",
                    "type": "TIME"
                },

                2: {
                    "name": "Weather Challenge",
                    "objective": "Drive safely through difficult weather",
                    "type": "WEATHER"
                },

                3: {
                    "name": "Precision Drive",
                    "objective": "Complete the route efficiently",
                    "type": "ROUTE"
                }
            },

            5: {
                1: {
                    "name": "Emergency Response",
                    "objective": "Navigate safely around emergency vehicles",
                    "type": "EMERGENCY"
                },

                2: {
                    "name": "City Traffic",
                    "objective": "Handle intelligent traffic",
                    "type": "TRAFFIC"
                },

                3: {
                    "name": "Fuel Management",
                    "objective": "Reach the destination using fuel efficiently",
                    "type": "FUEL"
                }
            },

            6: {
                1: {
                    "name": "AI Challenge",
                    "objective": "Complete the route against advanced AI traffic",
                    "type": "AI"
                },

                2: {
                    "name": "Survival Drive",
                    "objective": "Reach the destination while protecting all lives",
                    "type": "LIVES"
                },

                3: {
                    "name": "Expert Route",
                    "objective": "Complete an efficient route with minimal collisions",
                    "type": "ROUTE"
                }
            },

            7: {
                1: {
                    "name": "Ultimate Drive",
                    "objective": "Complete the mission under extreme conditions",
                    "type": "AI"
                },

                2: {
                    "name": "Master Driver",
                    "objective": "Reach the destination with minimal collisions and fuel usage",
                    "type": "MASTER"
                },

                3: {
                    "name": "RoadMind Champion",
                    "objective": "Complete the final challenge",
                    "type": "FINAL"
                }
            }
        }

    def get_mission(self, level, mission):

        if level in self.missions:

            if mission in self.missions[level]:

                return self.missions[level][mission]

        return {
            "name": "Unknown Mission",
            "objective": "Reach the destination",
            "type": "TIME"
        }

    # --------------------------------------------------------
    # CHECK MISSION
    # --------------------------------------------------------

    def check_mission(
        self,
        level,
        mission,
        time_left,
        collisions,
        fuel,
        route_efficiency,
        lives
    ):

        mission_data = self.get_mission(
            level,
            mission
        )

        mission_type = mission_data["type"]

        if mission_type == "TIME":
            return time_left > 0

        if mission_type == "COLLISION":
            return collisions <= 2

        if mission_type == "FUEL":
            return fuel > 10

        if mission_type == "ROUTE":
            return route_efficiency >= 60

        if mission_type == "TRAFFIC":
            return lives > 0

        if mission_type == "OBSTACLE":
            return collisions <= 3

        if mission_type == "WEATHER":
            return lives > 0

        if mission_type == "EMERGENCY":
            return lives > 0

        if mission_type == "AI":
            return (
                lives > 0
                and collisions <= 3
            )

        if mission_type == "LIVES":
            return lives == 3

        if mission_type == "MASTER":
            return (
                collisions <= 2
                and fuel > 10
                and route_efficiency >= 60
            )

        if mission_type == "FINAL":
            return (
                lives > 0
                and collisions <= 3
                and fuel > 10
            )

        return True

    # --------------------------------------------------------
    # FAILURE REASON
    # --------------------------------------------------------

    def get_failure_reason(
        self,
        level,
        mission,
        time_left,
        collisions,
        fuel,
        route_efficiency,
        lives
    ):

        mission_data = self.get_mission(
            level,
            mission
        )

        mission_type = mission_data["type"]

        if lives <= 0:

            return "All 3 lives were lost."

        if fuel <= 0:

            return "Fuel ran out."

        if time_left <= 0:

            return "Mission time expired."

        if mission_type == "COLLISION":

            if collisions > 2:
                return f"Too many collisions: {collisions}/2 allowed."

        if mission_type == "FUEL":

            if fuel <= 10:
                return f"Too much fuel used: only {int(fuel)}% remaining."

        if mission_type == "ROUTE":

            if route_efficiency < 60:
                return f"Route efficiency too low: {int(route_efficiency)}%."

        if mission_type == "OBSTACLE":

            if collisions > 3:
                return f"Too many collisions: {collisions}/3 allowed."

        if mission_type == "AI":

            if collisions > 3:
                return f"Too many collisions: {collisions}/3 allowed."

        if mission_type == "LIVES":

            if lives < 3:
                return f"You lost {3 - lives} life(s). All 3 lives were required."

        if mission_type == "MASTER":

            if collisions > 2:
                return f"Too many collisions: {collisions}/2 allowed."

            if fuel <= 10:
                return "Fuel conservation requirement was not achieved."

            if route_efficiency < 60:
                return f"Route efficiency too low: {int(route_efficiency)}%."

        if mission_type == "FINAL":

            if collisions > 3:
                return f"Too many collisions: {collisions}/3 allowed."

            if fuel <= 10:
                return "Fuel conservation requirement was not achieved."

        return "Mission objective was not completed."