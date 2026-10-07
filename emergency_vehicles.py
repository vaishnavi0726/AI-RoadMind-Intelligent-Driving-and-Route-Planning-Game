import pygame
import random
import math


class EmergencyVehicleSystem:

    def __init__(self, width, height):

        self.width = width
        self.height = height

        self.vehicles = []

        self.colors = {
            "AMBULANCE": (245, 245, 245),
            "FIRE": (220, 40, 40),
            "POLICE": (40, 80, 220)
        }

        self.create_vehicles()

    # --------------------------------------------------
    # CREATE EMERGENCY VEHICLES
    # --------------------------------------------------

    def create_vehicles(self):

        self.vehicles = []

        vehicle_types = [
            "AMBULANCE",
            "FIRE",
            "POLICE"
        ]

        for i in range(2):

            vehicle_type = random.choice(vehicle_types)

            direction = random.choice([1, -1])

            if direction == 1:

                x = random.randint(250, 700)
                y = -100

            else:

                x = random.randint(250, 700)
                y = self.height + 100

            vehicle = {

                "x": float(x),
                "y": float(y),

                "width": 40,
                "height": 70,

                "direction": direction,

                "speed": random.uniform(6.0, 8.0),

                "type": vehicle_type,

                "siren": True,

                # Advanced AI values
                "priority": True,
                "nearby_traffic": 0,
                "overtaking": False
            }

            self.vehicles.append(vehicle)

    # --------------------------------------------------
    # RESET
    # --------------------------------------------------

    def reset(self):

        self.create_vehicles()

    # --------------------------------------------------
    # GET RECTANGLE
    # --------------------------------------------------

    def get_rect(self, vehicle):

        return pygame.Rect(
            int(vehicle["x"]),
            int(vehicle["y"]),
            vehicle["width"],
            vehicle["height"]
        )

    # --------------------------------------------------
    # EMERGENCY VEHICLE AI
    # --------------------------------------------------

    def update(self, traffic):

        for vehicle in self.vehicles:

            emergency_rect = self.get_rect(vehicle)

            nearby_count = 0

            # ------------------------------------------
            # CHECK NORMAL TRAFFIC
            # ------------------------------------------

            for normal_vehicle in traffic:

                normal_rect = normal_vehicle["rect"]

                distance_x = abs(
                    normal_rect.centerx -
                    emergency_rect.centerx
                )

                distance_y = abs(
                    normal_rect.centery -
                    emergency_rect.centery
                )

                distance = math.sqrt(
                    distance_x ** 2 +
                    distance_y ** 2
                )

                # --------------------------------------
                # EMERGENCY VEHICLE APPROACHING
                # --------------------------------------

                if distance < 220:

                    nearby_count += 1

                    # Emergency vehicle moving DOWN
                    if vehicle["direction"] == 1:

                        if normal_rect.centery < emergency_rect.centery:

                            normal_vehicle["speed"] *= 0.90

                    # Emergency vehicle moving UP
                    else:

                        if normal_rect.centery > emergency_rect.centery:

                            normal_vehicle["speed"] *= 0.90

                # --------------------------------------
                # FAR AWAY TRAFFIC RETURNS TO NORMAL
                # --------------------------------------

                else:

                    if normal_vehicle["speed"] < 4.0:

                        normal_vehicle["speed"] += 0.03

            vehicle["nearby_traffic"] = nearby_count

            # ------------------------------------------
            # EMERGENCY VEHICLE SPEED AI
            # ------------------------------------------

            base_speed = 7.0

            if nearby_count >= 3:

                vehicle["speed"] = min(
                    vehicle["speed"] + 0.05,
                    9.0
                )

            else:

                if vehicle["speed"] > base_speed:

                    vehicle["speed"] -= 0.02

            # ------------------------------------------
            # MOVE EMERGENCY VEHICLE
            # ------------------------------------------

            vehicle["y"] += (
                vehicle["direction"] *
                vehicle["speed"]
            )

            # ------------------------------------------
            # OVERTAKING DETECTION
            # ------------------------------------------

            vehicle["overtaking"] = False

            for normal_vehicle in traffic:

                normal_rect = normal_vehicle["rect"]

                distance = abs(
                    normal_rect.centery -
                    emergency_rect.centery
                )

                if distance < 100:

                    vehicle["overtaking"] = True

                    break

            # ------------------------------------------
            # RESPAWN
            # ------------------------------------------

            if vehicle["direction"] == 1:

                if vehicle["y"] > self.height + 120:

                    vehicle["y"] = -120

                    vehicle["x"] = random.randint(
                        250,
                        700
                    )

            else:

                if vehicle["y"] < -120:

                    vehicle["y"] = self.height + 120

                    vehicle["x"] = random.randint(
                        250,
                        700
                    )

    # --------------------------------------------------
    # PLAYER COLLISION
    # --------------------------------------------------

    def check_player_collision(self, player_rect):

        for vehicle in self.vehicles:

            emergency_rect = self.get_rect(vehicle)

            if player_rect.colliderect(
                emergency_rect
            ):

                return True

        return False

    # --------------------------------------------------
    # DRAW EMERGENCY VEHICLES
    # --------------------------------------------------

    def draw(self, screen):

        for vehicle in self.vehicles:

            rect = self.get_rect(vehicle)

            color = self.colors[
                vehicle["type"]
            ]

            # Vehicle body
            pygame.draw.rect(
                screen,
                color,
                rect,
                border_radius=6
            )

            # Dark middle stripe
            pygame.draw.rect(
                screen,
                (30, 30, 30),
                (
                    rect.x,
                    rect.y + 25,
                    rect.width,
                    10
                )
            )

            # ------------------------------------------
            # SIREN LIGHTS
            # ------------------------------------------

            if vehicle["siren"]:

                # Red light
                pygame.draw.circle(
                    screen,
                    (255, 40, 40),
                    (
                        rect.centerx - 8,
                        rect.y + 12
                    ),
                    5
                )

                # Blue light
                pygame.draw.circle(
                    screen,
                    (40, 100, 255),
                    (
                        rect.centerx + 8,
                        rect.y + 12
                    ),
                    5
                )

            # ------------------------------------------
            # WHEELS
            # ------------------------------------------

            pygame.draw.rect(
                screen,
                (20, 20, 20),
                (
                    rect.x - 4,
                    rect.y + 12,
                    5,
                    15
                )
            )

            pygame.draw.rect(
                screen,
                (20, 20, 20),
                (
                    rect.right - 1,
                    rect.y + 12,
                    5,
                    15
                )
            )

            pygame.draw.rect(
                screen,
                (20, 20, 20),
                (
                    rect.x - 4,
                    rect.bottom - 27,
                    5,
                    15
                )
            )

            pygame.draw.rect(
                screen,
                (20, 20, 20),
                (
                    rect.right - 1,
                    rect.bottom - 27,
                    5,
                    15
                )
            )

            # ------------------------------------------
            # PRIORITY INDICATOR
            # ------------------------------------------

            if vehicle["priority"]:

                pygame.draw.circle(
                    screen,
                    (255, 220, 50),
                    (
                        rect.centerx,
                        rect.y - 7
                    ),
                    3
                )