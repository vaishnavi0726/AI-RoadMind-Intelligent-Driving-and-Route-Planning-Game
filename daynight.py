import pygame


class DayNightSystem:

    def __init__(self, width, height):

        self.width = width
        self.height = height

        self.time = 0.0

        self.phase = "DAY"

        # Full cycle = 60 seconds
        self.cycle_duration = 60.0

    def reset(self):

        self.time = 0.0
        self.phase = "DAY"

    def update(self, dt):

        self.time += dt

        if self.time >= self.cycle_duration:
            self.time = 0.0

        progress = self.time / self.cycle_duration

        # ------------------------------------------------
        # DAY
        # 0 - 25 seconds
        # ------------------------------------------------

        if progress < 0.42:

            self.phase = "DAY"

        # ------------------------------------------------
        # EVENING
        # 25 - 40 seconds
        # ------------------------------------------------

        elif progress < 0.67:

            self.phase = "EVENING"

        # ------------------------------------------------
        # NIGHT
        # 40 - 60 seconds
        # ------------------------------------------------

        else:

            self.phase = "NIGHT"

    def is_night(self):

        return self.phase == "NIGHT"

    def is_evening(self):

        return self.phase == "EVENING"

    def get_phase_name(self):

        return self.phase

    # ====================================================
    # BACKGROUND OVERLAY
    # ====================================================

    def draw_overlay(self, screen):

        overlay = pygame.Surface(
            (
                self.width,
                self.height
            ),
            pygame.SRCALPHA
        )

        # ------------------------------------------------
        # DAY
        # ------------------------------------------------

        if self.phase == "DAY":

            # No darkness
            return

        # ------------------------------------------------
        # EVENING
        # ------------------------------------------------

        elif self.phase == "EVENING":

            overlay.fill(
                (
                    255,
                    110,
                    30,
                    75
                )
            )

            screen.blit(
                overlay,
                (0, 0)
            )

        # ------------------------------------------------
        # NIGHT
        # ------------------------------------------------

        elif self.phase == "NIGHT":

            overlay.fill(
                (
                    5,
                    10,
                    45,
                    185
                )
            )

            screen.blit(
                overlay,
                (0, 0)
            )

    # ====================================================
    # STREET LIGHTS
    # ====================================================

    def draw_street_lights(self, screen):

        if self.phase == "DAY":

            return

        # Evening = lights start turning on
        # Night = stronger lights

        for y in range(
            70,
            self.height,
            120
        ):

            self.draw_single_light(
                screen,
                245,
                y
            )

            self.draw_single_light(
                screen,
                755,
                y
            )

    def draw_single_light(
        self,
        screen,
        x,
        y
    ):

        # Pole

        pygame.draw.line(
            screen,
            (
                80,
                80,
                80
            ),
            (
                x,
                y
            ),
            (
                x,
                y + 65
            ),
            5
        )

        # Light glow

        glow = pygame.Surface(
            (
                120,
                120
            ),
            pygame.SRCALPHA
        )

        if self.phase == "EVENING":

            glow_alpha = 35

        else:

            glow_alpha = 75

        pygame.draw.circle(
            glow,
            (
                255,
                220,
                90,
                glow_alpha
            ),
            (
                60,
                60
            ),
            55
        )

        screen.blit(
            glow,
            (
                x - 60,
                y - 20
            )
        )

        # Lamp

        pygame.draw.circle(
            screen,
            (
                255,
                230,
                100
            ),
            (
                x,
                y
            ),
            8
        )

    # ====================================================
    # PLAYER HEADLIGHT
    # ====================================================

    def draw_headlight(
        self,
        screen,
        x,
        y,
        direction=-1
    ):

        if not self.is_night():

            return

        light = pygame.Surface(
            (
                self.width,
                self.height
            ),
            pygame.SRCALPHA
        )

        if direction == -1:

            points = [

                (
                    x - 15,
                    y
                ),

                (
                    x + 15,
                    y
                ),

                (
                    x + 100,
                    y - 150
                ),

                (
                    x - 100,
                    y - 150
                )

            ]

        else:

            points = [

                (
                    x - 15,
                    y
                ),

                (
                    x + 15,
                    y
                ),

                (
                    x + 100,
                    y + 150
                ),

                (
                    x - 100,
                    y + 150
                )

            ]

        pygame.draw.polygon(
            light,
            (
                255,
                245,
                180,
                50
            ),
            points
        )

        screen.blit(
            light,
            (0, 0)
        )