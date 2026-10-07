import pygame
import random
import math


class PedestrianSystem:

    def __init__(self, width, height):

        self.width = width
        self.height = height

        self.pedestrians = []

        self.crossing_y = 350

        self.colors = [
            (255, 200, 120),
            (120, 180, 255),
            (255, 150, 180),
            (150, 255, 180),
            (220, 180, 255)
        ]

        self.create_pedestrians()

    def create_pedestrians(self):

        self.pedestrians = []

        for i in range(6):

            side = random.choice(
                ["left", "right"]
            )

            if side == "left":

                x = random.randint(40, 180)
                direction = 1

            else:

                x = random.randint(820, 960)
                direction = -1

            y = (
                self.crossing_y +
                random.randint(-25, 25)
            )

            pedestrian = {
                "x": float(x),
                "y": float(y),
                "direction": direction,
                "speed": random.uniform(0.7, 1.3),
                "color": random.choice(self.colors),
                "stopped": False
            }

            self.pedestrians.append(
                pedestrian
            )

    def reset(self):

        self.create_pedestrians()

    def distance_to_vehicle(
        self,
        pedestrian,
        vehicle
    ):

        px = pedestrian["x"]
        py = pedestrian["y"]

        vx = vehicle.centerx
        vy = vehicle.centery

        return math.sqrt(
            (px - vx) ** 2 +
            (py - vy) ** 2
        )

    def pedestrian_decision(
        self,
        pedestrian,
        player_rect,
        traffic
    ):

        pedestrian["stopped"] = False

        # Check player vehicle

        distance = self.distance_to_vehicle(
            pedestrian,
            player_rect
        )

        if distance < 100:

            pedestrian["stopped"] = True

            return

        # Check traffic vehicles

        for vehicle in traffic:

            distance = self.distance_to_vehicle(
                pedestrian,
                vehicle["rect"]
            )

            if distance < 85:

                pedestrian["stopped"] = True

                return

    def update(
        self,
        player_rect,
        traffic
    ):

        for pedestrian in self.pedestrians:

            self.pedestrian_decision(
                pedestrian,
                player_rect,
                traffic
            )

            if pedestrian["stopped"]:

                continue

            pedestrian["x"] += (
                pedestrian["direction"] *
                pedestrian["speed"]
            )

            # Respawn from left

            if pedestrian["direction"] == 1:

                if pedestrian["x"] > self.width + 30:

                    pedestrian["x"] = -30

                    pedestrian["y"] = (
                        self.crossing_y +
                        random.randint(-25, 25)
                    )

            # Respawn from right

            else:

                if pedestrian["x"] < -30:

                    pedestrian["x"] = (
                        self.width + 30
                    )

                    pedestrian["y"] = (
                        self.crossing_y +
                        random.randint(-25, 25)
                    )

    def check_player_collision(
        self,
        player_rect
    ):

        for pedestrian in self.pedestrians:

            pedestrian_rect = pygame.Rect(
                int(pedestrian["x"] - 8),
                int(pedestrian["y"] - 12),
                16,
                24
            )

            if player_rect.colliderect(
                pedestrian_rect
            ):

                return True

        return False

    def draw(self, screen):

        for pedestrian in self.pedestrians:

            x = int(pedestrian["x"])
            y = int(pedestrian["y"])

            # Shadow

            pygame.draw.ellipse(
                screen,
                (30, 30, 30),
                (
                    x - 8,
                    y + 8,
                    16,
                    6
                )
            )

            # Body

            pygame.draw.rect(
                screen,
                pedestrian["color"],
                (
                    x - 6,
                    y - 2,
                    12,
                    15
                ),
                border_radius=3
            )

            # Head

            pygame.draw.circle(
                screen,
                (235, 190, 150),
                (
                    x,
                    y - 8
                ),
                6
            )

            # Legs

            pygame.draw.line(
                screen,
                (40, 40, 40),
                (x - 3, y + 12),
                (x - 6, y + 20),
                3
            )

            pygame.draw.line(
                screen,
                (40, 40, 40),
                (x + 3, y + 12),
                (x + 6, y + 20),
                3
            )

            # Stopped indicator

            if pedestrian["stopped"]:

                pygame.draw.circle(
                    screen,
                    (255, 220, 50),
                    (
                        x,
                        y - 22
                    ),
                    3
                )
                