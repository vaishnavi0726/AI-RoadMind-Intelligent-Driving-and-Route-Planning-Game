import pygame


class TrafficLightSystem:

    def __init__(self):

        # Traffic light position
        self.intersection_y = 350

        # Traffic light cycle
        self.timer = 0

        self.red_time = 6
        self.yellow_time = 2
        self.green_time = 6

        self.cycle_time = (
            self.red_time +
            self.yellow_time +
            self.green_time
        )

        self.state = "RED"

    # ---------------------------------------------------------
    # UPDATE TRAFFIC LIGHT
    # ---------------------------------------------------------

    def update(self, dt):

        self.timer += dt

        if self.timer >= self.cycle_time:
            self.timer = 0

        if self.timer < self.red_time:

            self.state = "RED"

        elif self.timer < self.red_time + self.yellow_time:

            self.state = "YELLOW"

        else:

            self.state = "GREEN"

    # ---------------------------------------------------------
    # GET CURRENT STATE
    # ---------------------------------------------------------

    def get_state(self):

        return self.state

    # ---------------------------------------------------------
    # TRAFFIC DECISION
    # ---------------------------------------------------------

    def should_stop(self, vehicle):

        if self.state == "GREEN":
            return False

        vehicle_rect = vehicle["rect"]

        direction = vehicle["direction"]

        # Vehicles moving DOWN
        if direction == 1:

            distance = self.intersection_y - vehicle_rect.bottom

            if 0 < distance < 120:
                return True

        # Vehicles moving UP
        else:

            distance = vehicle_rect.top - self.intersection_y

            if 0 < distance < 120:
                return True

        return False

    # ---------------------------------------------------------
    # DRAW INTERSECTION
    # ---------------------------------------------------------

    def draw_intersection(self, screen):

        # Horizontal cross road

        pygame.draw.rect(
            screen,
            (55, 55, 55),
            (0, self.intersection_y - 45, 1000, 90)
        )

        # Road markings

        for x in range(0, 1000, 50):

            pygame.draw.rect(
                screen,
                (220, 220, 220),
                (
                    x,
                    self.intersection_y - 3,
                    30,
                    6
                )
            )

    # ---------------------------------------------------------
    # DRAW TRAFFIC LIGHTS
    # ---------------------------------------------------------

    def draw(self, screen, font):

        # Draw intersection first
        self.draw_intersection(screen)

        # Traffic light positions
        light_positions = [
            (205, self.intersection_y - 120),
            (770, self.intersection_y + 20)
        ]

        for x, y in light_positions:

            # Signal box

            pygame.draw.rect(
                screen,
                (25, 25, 25),
                (x, y, 45, 120),
                border_radius=8
            )

            pygame.draw.rect(
                screen,
                (90, 90, 90),
                (x, y, 45, 120),
                2,
                border_radius=8
            )

            # Default colors

            red_color = (80, 20, 20)
            yellow_color = (80, 70, 20)
            green_color = (20, 80, 30)

            # Active light

            if self.state == "RED":
                red_color = (255, 40, 40)

            elif self.state == "YELLOW":
                yellow_color = (255, 220, 40)

            elif self.state == "GREEN":
                green_color = (40, 255, 90)

            # Red

            pygame.draw.circle(
                screen,
                red_color,
                (x + 22, y + 22),
                12
            )

            # Yellow

            pygame.draw.circle(
                screen,
                yellow_color,
                (x + 22, y + 60),
                12
            )

            # Green

            pygame.draw.circle(
                screen,
                green_color,
                (x + 22, y + 98),
                12
            )

        # State text

        state_color = (255, 80, 80)

        if self.state == "YELLOW":
            state_color = (255, 220, 50)

        elif self.state == "GREEN":
            state_color = (50, 255, 100)

        text = font.render(
            "TRAFFIC LIGHT: " + self.state,
            True,
            state_color
        )

        screen.blit(
            text,
            (720, 15)
        )