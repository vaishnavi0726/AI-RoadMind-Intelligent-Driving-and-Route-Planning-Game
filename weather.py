import random
import pygame


class WeatherSystem:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.conditions = [
            "CLEAR",
            "RAIN",
            "FOG",
            "HEAVY RAIN"
        ]

        self.current = "CLEAR"

        self.rain_particles = []

        self.create_rain()

    def create_rain(self):
        self.rain_particles = []

        for _ in range(180):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)

            speed = random.randint(7, 14)

            self.rain_particles.append({
                "x": x,
                "y": y,
                "speed": speed
            })

    def set_random_weather(self):
        self.current = random.choice(self.conditions)

        if self.current == "CLEAR":
            self.create_rain()

        elif self.current == "RAIN":
            self.create_rain()

        elif self.current == "FOG":
            self.create_rain()

        elif self.current == "HEAVY RAIN":
            self.create_rain()

    def set_weather(self, weather):
        if weather in self.conditions:
            self.current = weather

    def update(self):
        if self.current not in ["RAIN", "HEAVY RAIN"]:
            return

        for particle in self.rain_particles:
            particle["y"] += particle["speed"]

            if particle["y"] > self.height:
                particle["y"] = random.randint(-100, -10)
                particle["x"] = random.randint(0, self.width)

    def draw(self, screen):

        # -----------------------------
        # FOG
        # -----------------------------

        if self.current == "FOG":

            fog_surface = pygame.Surface(
                (self.width, self.height),
                pygame.SRCALPHA
            )

            fog_surface.fill((210, 210, 210, 120))

            screen.blit(fog_surface, (0, 0))

        # -----------------------------
        # RAIN
        # -----------------------------

        elif self.current == "RAIN":

            for particle in self.rain_particles:

                x = particle["x"]
                y = particle["y"]

                pygame.draw.line(
                    screen,
                    (170, 200, 255),
                    (x, y),
                    (x - 2, y + 10),
                    1
                )

        # -----------------------------
        # HEAVY RAIN
        # -----------------------------

        elif self.current == "HEAVY RAIN":

            for particle in self.rain_particles:

                x = particle["x"]
                y = particle["y"]

                pygame.draw.line(
                    screen,
                    (130, 180, 255),
                    (x, y),
                    (x - 3, y + 18),
                    2
                )

            dark_surface = pygame.Surface(
                (self.width, self.height),
                pygame.SRCALPHA
            )

            dark_surface.fill((30, 40, 60, 45))

            screen.blit(dark_surface, (0, 0))

    def get_control_multiplier(self):

        if self.current == "CLEAR":
            return 1.0

        if self.current == "RAIN":
            return 0.85

        if self.current == "FOG":
            return 0.95

        if self.current == "HEAVY RAIN":
            return 0.70

        return 1.0

    def get_traffic_multiplier(self):

        if self.current == "CLEAR":
            return 1.0

        if self.current == "RAIN":
            return 0.85

        if self.current == "FOG":
            return 0.75

        if self.current == "HEAVY RAIN":
            return 0.65

        return 1.0

    def get_visibility(self):

        if self.current == "CLEAR":
            return 1.0

        if self.current == "RAIN":
            return 0.85

        if self.current == "FOG":
            return 0.55

        if self.current == "HEAVY RAIN":
            return 0.70

        return 1.0