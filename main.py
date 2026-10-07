import pygame
import random
import math
import json
import os
import time

from pedestrian import PedestrianSystem
from emergency_vehicles import EmergencyVehicleSystem
from mission_system import MissionSystem

from analytics import (
    save_mission_result,
    create_performance_graph,
    load_history
)


# ============================================================
# INITIALIZATION
# ============================================================

pygame.init()

WIDTH = 1000
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(
    "AI RoadMind - Intelligent Driving & Route Planning"
)

clock = pygame.time.Clock()
FPS = 60


# ============================================================
# COLORS
# ============================================================

WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
GRAY = (100, 100, 100)
LIGHT_GRAY = (200, 200, 200)

ROAD_COLOR = (55, 55, 60)
GRASS_COLOR = (45, 130, 60)

BLUE = (60, 160, 255)
RED = (230, 60, 60)
GREEN = (60, 200, 100)
YELLOW = (255, 210, 50)
ORANGE = (255, 150, 50)
PURPLE = (180, 80, 255)
CYAN = (50, 220, 220)


# ============================================================
# GAME STATES
# ============================================================

MENU = "MENU"
GARAGE = "GARAGE"
PLAYING = "PLAYING"
MISSION_COMPLETE = "MISSION_COMPLETE"
GAME_OVER = "GAME_OVER"
REPORT = "REPORT"

game_state = MENU


# ============================================================
# FONTS
# ============================================================

font_small = pygame.font.SysFont("arial", 18)
font_medium = pygame.font.SysFont("arial", 24)
font_large = pygame.font.SysFont("arial", 34)
font_title = pygame.font.SysFont("arial", 46, bold=True)


# ============================================================
# SAVE FILE
# ============================================================

SAVE_FILE = "roadmind_save.json"


# ============================================================
# GAME DATA
# ============================================================

current_level = 1
current_mission = 1

score = 0
coins = 0
xp = 0

selected_car = 1

lives = 3
fuel = 100.0
collisions = 0

mission_time = 90
time_left = mission_time

mission_start_time = time.time()

player_distance = 0.0
route_efficiency = 100.0
shortest_route_distance = 1.0

mission_completed = False

last_report = {}

last_collision_time = 0


# ============================================================
# AI DATA
# ============================================================

ai_difficulty = 1.0
ai_speed_multiplier = 1.0
ai_traffic_count = 8

previous_ai_difficulty = 1.0

ai_learning_message = "AI is learning..."


# ============================================================
# CARS
# ============================================================

cars = {

    1: {
        "name": "Starter Car",
        "speed": 5,
        "fuel_efficiency": 1.0,
        "cost": 0,
        "unlocked": True,
        "color": (60, 160, 255)
    },

    2: {
        "name": "Speed Car",
        "speed": 7,
        "fuel_efficiency": 0.8,
        "cost": 500,
        "unlocked": False,
        "color": (255, 80, 80)
    },

    3: {
        "name": "Eco Car",
        "speed": 5,
        "fuel_efficiency": 1.3,
        "cost": 350,
        "unlocked": False,
        "color": (70, 220, 100)
    },

    4: {
        "name": "Pro Car",
        "speed": 8,
        "fuel_efficiency": 1.0,
        "cost": 800,
        "unlocked": False,
        "color": (180, 80, 255)
    }
}


# ============================================================
# GAME OBJECTS
# ============================================================

player = pygame.Rect(
    475,
    560,
    45,
    70
)

destination = pygame.Rect(
    475,
    50,
    50,
    70
)

traffic = []
obstacles = []
route_points = []


# ============================================================
# SYSTEMS
# ============================================================

mission_system = MissionSystem()

pedestrian_system = PedestrianSystem(
    WIDTH,
    HEIGHT
)

emergency_system = EmergencyVehicleSystem(
    WIDTH,
    HEIGHT
)


# ============================================================
# UTILITY
# ============================================================

def draw_text(
    text,
    font,
    color,
    x,
    y
):

    surface = font.render(
        str(text),
        True,
        color
    )

    screen.blit(
        surface,
        (x, y)
    )


def calculate_distance(
    x1,
    y1,
    x2,
    y2
):

    return math.sqrt(
        (x2 - x1) ** 2 +
        (y2 - y1) ** 2
    )


# ============================================================
# SAVE GAME
# ============================================================

def save_game():

    data = {

        "current_level": current_level,

        "current_mission": current_mission,

        "score": score,

        "coins": coins,

        "xp": xp,

        "selected_car": selected_car,

        "cars": cars
    }

    try:

        with open(
            SAVE_FILE,
            "w"
        ) as file:

            json.dump(
                data,
                file,
                indent=4
            )

    except Exception as e:

        print(
            "Save error:",
            e
        )


# ============================================================
# LOAD GAME
# ============================================================

def load_game():

    global current_level
    global current_mission
    global score
    global coins
    global xp
    global selected_car
    global cars

    if not os.path.exists(
        SAVE_FILE
    ):

        save_game()

        return

    try:

        with open(
            SAVE_FILE,
            "r"
        ) as file:

            data = json.load(
                file
            )

        current_level = int(
            data.get(
                "current_level",
                1
            )
        )

        current_mission = int(
            data.get(
                "current_mission",
                1
            )
        )

        score = int(
            data.get(
                "score",
                0
            )
        )

        coins = int(
            data.get(
                "coins",
                0
            )
        )

        xp = int(
            data.get(
                "xp",
                0
            )
        )

        selected_car = int(
            data.get(
                "selected_car",
                1
            )
        )

        saved_cars = data.get(
            "cars",
            {}
        )

        if isinstance(
            saved_cars,
            dict
        ):

            for car_id in cars:

                saved = saved_cars.get(
                    str(car_id),
                    saved_cars.get(
                        car_id,
                        {}
                    )
                )

                if isinstance(
                    saved,
                    dict
                ):

                    cars[car_id].update(
                        saved
                    )

        if selected_car not in cars:

            selected_car = 1

        if not cars[
            selected_car
        ].get(
            "unlocked",
            False
        ):

            selected_car = 1

    except Exception as e:

        print(
            "Load error:",
            e
        )

        selected_car = 1


# ============================================================
# ADAPTIVE AI LEARNING
# ============================================================

def calculate_ai_difficulty():

    global ai_difficulty
    global ai_speed_multiplier
    global ai_traffic_count
    global previous_ai_difficulty
    global ai_learning_message

    base_difficulty = (
        1.0 +
        (current_level - 1) * 0.15
    )

    previous_ai_difficulty = ai_difficulty

    history = load_history()

    if not isinstance(
        history,
        list
    ):

        history = []

    recent_history = history[-5:]


    # --------------------------------------------------------
    # NO PREVIOUS HISTORY
    # --------------------------------------------------------

    if not recent_history:

        ai_difficulty = base_difficulty

        ai_learning_message = (
            "AI is using default difficulty."
        )

    else:

        total_collisions = 0
        total_efficiency = 0

        valid_count = 0

        for result in recent_history:

            try:

                result_collisions = float(
                    result.get(
                        "collisions",
                        0
                    )
                )

                result_efficiency = float(
                    result.get(
                        "route_efficiency",
                        100
                    )
                )

                total_collisions += (
                    result_collisions
                )

                total_efficiency += (
                    result_efficiency
                )

                valid_count += 1

            except Exception:

                continue


        if valid_count > 0:

            average_collisions = (
                total_collisions /
                valid_count
            )

            average_efficiency = (
                total_efficiency /
                valid_count
            )

        else:

            average_collisions = 0

            average_efficiency = 100


        ai_difficulty = base_difficulty


        # VERY GOOD PERFORMANCE
        if (
            average_collisions <= 1
            and
            average_efficiency >= 85
        ):

            ai_difficulty += 0.35

            ai_learning_message = (
                "AI learned: You are performing very well!"
            )


        # GOOD PERFORMANCE
        elif (
            average_collisions <= 2
            and
            average_efficiency >= 70
        ):

            ai_difficulty += 0.15

            ai_learning_message = (
                "AI learned: Increasing challenge."
            )


        # AVERAGE PERFORMANCE
        elif (
            average_collisions <= 3
            and
            average_efficiency >= 55
        ):

            ai_learning_message = (
                "AI learned: Maintaining difficulty."
            )


        # STRUGGLING
        elif (
            average_collisions >= 3
            or
            average_efficiency < 55
        ):

            ai_difficulty -= 0.20

            ai_learning_message = (
                "AI learned: Reducing difficulty."
            )


        # VERY STRUGGLING
        if (
            average_collisions >= 4
            or
            average_efficiency < 45
        ):

            ai_difficulty -= 0.20

            ai_learning_message = (
                "AI learned: Player needs more support."
            )


    # Clamp difficulty

    ai_difficulty = max(
        0.75,
        min(
            ai_difficulty,
            2.50
        )
    )


    # AI speed

    ai_speed_multiplier = (
        0.85 +
        ai_difficulty * 0.20
    )


    # AI traffic count

    ai_traffic_count = int(
        6 +
        ai_difficulty * 2
    )

    ai_traffic_count = max(
        6,
        min(
            ai_traffic_count,
            12
        )
    )


# ============================================================
# CREATE TRAFFIC
# ============================================================

def create_traffic():

    global traffic

    traffic = []

    for i in range(
        ai_traffic_count
    ):

        x = random.randint(
            260,
            700
        )

        y = random.randint(
            -500,
            650
        )

        width = 40
        height = 70

        base_speed = random.uniform(
            2.5,
            4.5
        )

        speed = (
            base_speed *
            ai_speed_multiplier
        )

        vehicle = {

            "rect": pygame.Rect(
                x,
                y,
                width,
                height
            ),

            "speed": speed,

            "color": random.choice(
                [
                    (220, 70, 70),
                    (70, 150, 230),
                    (240, 180, 60),
                    (180, 80, 200),
                    (70, 200, 120)
                ]
            )
        }

        traffic.append(
            vehicle
        )


# ============================================================
# UPDATE TRAFFIC
# ============================================================

def update_traffic():

    for vehicle in traffic:

        vehicle["rect"].y += int(
            vehicle["speed"]
        )

        if (
            vehicle["rect"].y
            > HEIGHT + 100
        ):

            vehicle["rect"].y = random.randint(
                -500,
                -80
            )

            vehicle["rect"].x = random.randint(
                260,
                700
            )


# ============================================================
# CREATE OBSTACLES
# ============================================================

def create_obstacles():

    global obstacles

    obstacles = []

    obstacle_count = (
        4 +
        current_level
    )

    obstacle_count = min(
        obstacle_count,
        10
    )

    for i in range(
        obstacle_count
    ):

        x = random.randint(
            260,
            700
        )

        y = random.randint(
            50,
            620
        )

        obstacle = pygame.Rect(
            x,
            y,
            35,
            35
        )

        obstacles.append(
            obstacle
        )


# ============================================================
# CREATE ROUTE
# ============================================================

def create_route():

    global route_points
    global shortest_route_distance

    start_x = player.centerx
    start_y = player.centery

    end_x = destination.centerx
    end_y = destination.centery

    shortest_route_distance = calculate_distance(
        start_x,
        start_y,
        end_x,
        end_y
    )

    if shortest_route_distance <= 0:

        shortest_route_distance = 1

    route_points = []

    for i in range(12):

        progress = i / 11

        x = (
            start_x +
            (end_x - start_x)
            * progress
        )

        y = (
            start_y +
            (end_y - start_y)
            * progress
        )

        route_points.append(
            (
                int(x),
                int(y)
            )
        )


# ============================================================
# ROUTE EFFICIENCY
# ============================================================

def calculate_route_efficiency():

    global route_efficiency

    if player_distance <= 0:

        route_efficiency = 100.0

        return

    route_efficiency = (
        shortest_route_distance /
        player_distance
    ) * 100

    route_efficiency = max(
        0,
        min(
            route_efficiency,
            100
        )
    )


# ============================================================
# RESET MISSION
# ============================================================

def reset_mission():

    global lives
    global fuel
    global collisions
    global time_left
    global player_distance
    global route_efficiency
    global mission_completed
    global mission_start_time
    global last_collision_time

    lives = 3

    fuel = 100.0

    collisions = 0

    time_left = mission_time

    player_distance = 0.0

    route_efficiency = 100.0

    mission_completed = False

    last_collision_time = 0

    player.x = 475
    player.y = 560

    destination.x = random.randint(
        420,
        530
    )

    destination.y = 50

    # IMPORTANT:
    # AI learns from previous mission history
    calculate_ai_difficulty()

    create_traffic()

    create_obstacles()

    create_route()

    pedestrian_system.reset()

    emergency_system.reset()

    # IMPORTANT:
    # Reset timer every time mission starts
    mission_start_time = time.time()


# ============================================================
# UPDATE PLAYER
# ============================================================

def update_player():

    global player_distance
    global fuel

    keys = pygame.key.get_pressed()

    old_x = player.x
    old_y = player.y

    speed = cars[
        selected_car
    ]["speed"]

    if keys[
        pygame.K_LEFT
    ]:

        player.x -= speed

    if keys[
        pygame.K_RIGHT
    ]:

        player.x += speed

    if keys[
        pygame.K_UP
    ]:

        player.y -= speed

    if keys[
        pygame.K_DOWN
    ]:

        player.y += speed


    # Road boundaries

    if player.left < 230:

        player.left = 230

    if player.right > 770:

        player.right = 770

    if player.top < 0:

        player.top = 0

    if player.bottom > HEIGHT:

        player.bottom = HEIGHT


    movement = calculate_distance(
        old_x,
        old_y,
        player.x,
        player.y
    )

    player_distance += movement


    # Fuel

    fuel_efficiency = cars[
        selected_car
    ]["fuel_efficiency"]

    fuel -= (
        movement *
        0.008 /
        fuel_efficiency
    )

    fuel = max(
        0,
        fuel
    )

    calculate_route_efficiency()


# ============================================================
# COLLISION
# ============================================================

def handle_collision():

    global lives
    global collisions
    global last_collision_time

    current_time = time.time()

    if (
        current_time -
        last_collision_time
        < 1.0
    ):

        return

    lives -= 1

    collisions += 1

    last_collision_time = current_time

    player.x = 475
    player.y = 560


# ============================================================
# UPDATE GAME
# ============================================================

def update_game():

    global time_left
    global game_state

    update_player()

    update_traffic()

    pedestrian_system.update(
        player,
        traffic
    )

    emergency_system.update(
        traffic
    )


    # Traffic collision

    for vehicle in traffic:

        if player.colliderect(
            vehicle["rect"]
        ):

            handle_collision()

            break


    # Obstacle collision

    for obstacle in obstacles:

        if player.colliderect(
            obstacle
        ):

            handle_collision()

            break


    # Pedestrian collision

    if pedestrian_system.check_player_collision(
        player
    ):

        handle_collision()


    # Emergency vehicle collision

    if emergency_system.check_player_collision(
        player
    ):

        handle_collision()


    # Timer

    elapsed = (
        time.time() -
        mission_start_time
    )

    time_left = max(
        0,
        mission_time -
        elapsed
    )


    # Game over

    if lives <= 0:

        game_state = GAME_OVER

        return

    if fuel <= 0:

        game_state = GAME_OVER

        return

    if time_left <= 0:

        game_state = GAME_OVER

        return


    # Destination

    if player.colliderect(
        destination
    ):

        complete_mission()


# ============================================================
# COMPLETE MISSION
# ============================================================

def complete_mission():

    global game_state
    global score
    global coins
    global xp
    global mission_completed
    global last_report

    if mission_completed:

        return

    mission_completed = True

    mission_data = mission_system.get_mission(
        current_level,
        current_mission
    )

    mission_success = mission_system.check_mission(
        current_level,
        current_mission,
        time_left,
        collisions,
        fuel,
        route_efficiency,
        lives
    )

    if not mission_success:

        game_state = GAME_OVER

        return


    # Rewards

    score += 500

    coins += (
        100 +
        current_level * 25
    )

    xp += (
        100 +
        current_level * 50
    )


    time_taken = (
        mission_time -
        time_left
    )

    fuel_used = (
        100 -
        fuel
    )


    # Analytics

    save_mission_result(

        current_level,

        current_mission,

        time_taken,

        collisions,

        fuel_used,

        route_efficiency,

        score,

        ai_difficulty
    )

    create_performance_graph()


    last_report = {

        "level": current_level,

        "mission": current_mission,

        "name": mission_data["name"],

        "time_taken": time_taken,

        "collisions": collisions,

        "fuel_used": fuel_used,

        "route_efficiency": route_efficiency,

        "score": score,

        "ai_difficulty": ai_difficulty,

        "ai_learning": ai_learning_message
    }

    save_game()

    game_state = MISSION_COMPLETE


# ============================================================
# DRAW ROAD
# ============================================================

def draw_road():

    screen.fill(
        GRASS_COLOR
    )

    pygame.draw.rect(
        screen,
        ROAD_COLOR,
        (
            220,
            0,
            560,
            HEIGHT
        )
    )

    pygame.draw.line(
        screen,
        WHITE,
        (220, 0),
        (220, HEIGHT),
        5
    )

    pygame.draw.line(
        screen,
        WHITE,
        (780, 0),
        (780, HEIGHT),
        5
    )

    for y in range(
        -50,
        HEIGHT,
        80
    ):

        pygame.draw.rect(
            screen,
            YELLOW,
            (
                495,
                y,
                10,
                45
            )
        )


# ============================================================
# DRAW ROUTE
# ============================================================

def draw_route():

    if len(
        route_points
    ) < 2:

        return

    pygame.draw.lines(
        screen,
        CYAN,
        False,
        route_points,
        4
    )


# ============================================================
# DRAW PLAYER
# ============================================================

def draw_player():

    color = cars[
        selected_car
    ]["color"]

    pygame.draw.rect(
        screen,
        color,
        player,
        border_radius=8
    )

    pygame.draw.rect(
        screen,
        (30, 30, 30),
        (
            player.x + 8,
            player.y + 10,
            player.width - 16,
            18
        ),
        border_radius=4
    )

    pygame.draw.circle(
        screen,
        WHITE,
        (
            player.centerx,
            player.y + 8
        ),
        4
    )


# ============================================================
# DRAW TRAFFIC
# ============================================================

def draw_traffic():

    for vehicle in traffic:

        rect = vehicle["rect"]

        pygame.draw.rect(
            screen,
            vehicle["color"],
            rect,
            border_radius=6
        )

        pygame.draw.rect(
            screen,
            (30, 30, 30),
            (
                rect.x + 7,
                rect.y + 10,
                rect.width - 14,
                18
            ),
            border_radius=3
        )


# ============================================================
# DRAW OBSTACLES
# ============================================================

def draw_obstacles():

    for obstacle in obstacles:

        pygame.draw.rect(
            screen,
            ORANGE,
            obstacle,
            border_radius=5
        )

        pygame.draw.line(
            screen,
            WHITE,
            obstacle.topleft,
            obstacle.bottomright,
            3
        )

        pygame.draw.line(
            screen,
            WHITE,
            obstacle.topright,
            obstacle.bottomleft,
            3
        )


# ============================================================
# DRAW DESTINATION
# ============================================================

def draw_destination():

    pygame.draw.rect(
        screen,
        GREEN,
        destination,
        border_radius=8
    )

    draw_text(
        "GOAL",
        font_small,
        BLACK,
        destination.x + 5,
        destination.y + 25
    )


# ============================================================
# HUD
# ============================================================

def draw_hud():

    pygame.draw.rect(
        screen,
        (25, 25, 25),
        (
            0,
            0,
            WIDTH,
            75
        )
    )

    draw_text(
        f"Level: {current_level}",
        font_small,
        WHITE,
        15,
        10
    )

    draw_text(
        f"Mission: {current_mission}",
        font_small,
        WHITE,
        15,
        38
    )

    draw_text(
        f"Lives: {lives}",
        font_small,
        RED,
        150,
        10
    )

    draw_text(
        f"Fuel: {int(fuel)}%",
        font_small,
        YELLOW,
        150,
        38
    )

    draw_text(
        f"Time: {int(time_left)}",
        font_small,
        WHITE,
        270,
        10
    )

    draw_text(
        f"Collisions: {collisions}",
        font_small,
        WHITE,
        270,
        38
    )

    draw_text(
        f"Route: {int(route_efficiency)}%",
        font_small,
        CYAN,
        410,
        10
    )

    draw_text(
        f"AI Difficulty: {ai_difficulty:.2f}",
        font_small,
        PURPLE,
        410,
        38
    )

    draw_text(
        f"Coins: {coins}",
        font_small,
        YELLOW,
        600,
        10
    )

    draw_text(
        f"XP: {xp}",
        font_small,
        GREEN,
        600,
        38
    )

    draw_text(
        f"Score: {score}",
        font_small,
        WHITE,
        760,
        10
    )


# ============================================================
# PLAYING SCREEN
# ============================================================

def draw_playing():

    draw_road()

    draw_route()

    draw_destination()

    draw_obstacles()

    draw_traffic()

    pedestrian_system.draw(
        screen
    )

    emergency_system.draw(
        screen
    )

    draw_player()

    draw_hud()


# ============================================================
# BUTTON HELPER
# ============================================================

def draw_button(
    rect,
    text,
    color
):

    pygame.draw.rect(
        screen,
        color,
        rect,
        border_radius=10
    )

    text_surface = font_medium.render(
        text,
        True,
        WHITE
    )

    text_rect = text_surface.get_rect(
        center=rect.center
    )

    screen.blit(
        text_surface,
        text_rect
    )


# ============================================================
# MAIN MENU
# ============================================================

def draw_menu():

    screen.fill(
        (18, 25, 35)
    )

    draw_text(
        "AI ROAD MIND",
        font_title,
        CYAN,
        300,
        100
    )

    draw_text(
        "Intelligent Driving & Route Planning Game",
        font_medium,
        WHITE,
        245,
        165
    )


    # START BUTTON

    start_rect = pygame.Rect(
        350,
        260,
        300,
        65
    )

    draw_button(
        start_rect,
        "START MISSION",
        BLUE
    )


    # GARAGE BUTTON

    garage_rect = pygame.Rect(
        350,
        350,
        300,
        65
    )

    draw_button(
        garage_rect,
        "GARAGE",
        PURPLE
    )


    # QUIT BUTTON

    quit_rect = pygame.Rect(
        350,
        440,
        300,
        65
    )

    draw_button(
        quit_rect,
        "QUIT",
        GRAY
    )


    draw_text(
        "Click a button or use keyboard controls",
        font_small,
        LIGHT_GRAY,
        350,
        560
    )

    draw_text(
        "ENTER = Start     G = Garage     ESC = Quit",
        font_small,
        LIGHT_GRAY,
        335,
        590
    )


# ============================================================
# GARAGE
# ============================================================

def draw_garage():

    screen.fill(
        (20, 25, 35)
    )

    draw_text(
        "GARAGE",
        font_title,
        WHITE,
        400,
        40
    )

    draw_text(
        f"Coins: {coins}",
        font_medium,
        YELLOW,
        420,
        105
    )


    y = 160

    for car_id in cars:

        car = cars[
            car_id
        ]

        unlocked = car[
            "unlocked"
        ]

        if unlocked:

            border_color = GREEN

        else:

            border_color = GRAY


        car_rect = pygame.Rect(
            170,
            y,
            660,
            90
        )

        pygame.draw.rect(
            screen,
            border_color,
            car_rect,
            2,
            border_radius=8
        )


        draw_text(
            f"{car_id}. {car['name']}",
            font_medium,
            WHITE,
            195,
            y + 12
        )

        draw_text(
            f"Speed: {car['speed']}",
            font_small,
            WHITE,
            195,
            y + 50
        )

        draw_text(
            f"Fuel Efficiency: {car['fuel_efficiency']}",
            font_small,
            WHITE,
            330,
            y + 50
        )


        if unlocked:

            if selected_car == car_id:

                draw_text(
                    "SELECTED",
                    font_medium,
                    GREEN,
                    680,
                    y + 25
                )

            else:

                draw_text(
                    "CLICK TO SELECT",
                    font_small,
                    CYAN,
                    650,
                    y + 25
                )

        else:

            draw_text(
                f"LOCKED - {car['cost']} coins",
                font_small,
                RED,
                600,
                y + 25
            )


        y += 110


    draw_text(
        "Click a car to select/unlock | ESC = Back",
        font_small,
        LIGHT_GRAY,
        330,
        625
    )


# ============================================================
# MISSION COMPLETE
# ============================================================

def draw_mission_complete():

    screen.fill(
        (18, 35, 25)
    )

    draw_text(
        "MISSION COMPLETE!",
        font_title,
        GREEN,
        315,
        70
    )

    draw_text(
        f"Level {current_level} - Mission {current_mission}",
        font_medium,
        WHITE,
        390,
        140
    )

    draw_text(
        f"Score: {score}",
        font_medium,
        YELLOW,
        410,
        200
    )

    draw_text(
        f"Coins: {coins}",
        font_medium,
        YELLOW,
        410,
        240
    )

    draw_text(
        f"XP: {xp}",
        font_medium,
        CYAN,
        410,
        280
    )

    draw_text(
        f"Route Efficiency: {int(route_efficiency)}%",
        font_medium,
        WHITE,
        350,
        340
    )

    draw_text(
        f"Collisions: {collisions}",
        font_medium,
        WHITE,
        410,
        380
    )

    draw_text(
        f"AI Difficulty: {ai_difficulty:.2f}",
        font_medium,
        PURPLE,
        390,
        420
    )

    draw_text(
        ai_learning_message,
        font_small,
        CYAN,
        300,
        465
    )


    # NEXT MISSION BUTTON

    next_rect = pygame.Rect(
        350,
        510,
        300,
        60
    )

    draw_button(
        next_rect,
        "NEXT MISSION",
        GREEN
    )


    # REPLAY BUTTON

    replay_rect = pygame.Rect(
        400,
        585,
        200,
        50
    )

    draw_button(
        replay_rect,
        "REPLAY",
        BLUE
    )


# ============================================================
# GAME OVER
# ============================================================

def draw_game_over():

    screen.fill(
        (45, 15, 15)
    )

    draw_text(
        "GAME OVER",
        font_title,
        RED,
        380,
        70
    )


    if lives <= 0:

        reason = "All 3 lives were lost."

    elif fuel <= 0:

        reason = "Fuel ran out."

    elif time_left <= 0:

        reason = "Mission time expired."

    else:

        reason = "Mission failed."


    draw_text(
        reason,
        font_medium,
        WHITE,
        350,
        160
    )

    draw_text(
        f"Collisions: {collisions}",
        font_medium,
        WHITE,
        400,
        220
    )

    draw_text(
        f"Fuel: {int(fuel)}%",
        font_medium,
        WHITE,
        430,
        265
    )

    draw_text(
        f"Route Efficiency: {int(route_efficiency)}%",
        font_medium,
        WHITE,
        350,
        310
    )


    # REPLAY BUTTON

    replay_rect = pygame.Rect(
        350,
        400,
        300,
        60
    )

    draw_button(
        replay_rect,
        "REPLAY MISSION",
        BLUE
    )


    # MENU BUTTON

    menu_rect = pygame.Rect(
        350,
        490,
        300,
        60
    )

    draw_button(
        menu_rect,
        "MAIN MENU",
        GRAY
    )


# ============================================================
# REPORT
# ============================================================

def draw_report():

    screen.fill(
        (20, 25, 35)
    )

    draw_text(
        "PERFORMANCE REPORT",
        font_title,
        CYAN,
        275,
        50
    )

    if not last_report:

        draw_text(
            "No report available.",
            font_medium,
            WHITE,
            390,
            250
        )

        return


    y = 140

    report_items = [

        (
            "Mission",
            last_report.get(
                "name",
                "Unknown"
            )
        ),

        (
            "Time Taken",
            f"{last_report.get('time_taken', 0):.1f} sec"
        ),

        (
            "Collisions",
            last_report.get(
                "collisions",
                0
            )
        ),

        (
            "Fuel Used",
            f"{last_report.get('fuel_used', 0):.1f}%"
        ),

        (
            "Route Efficiency",
            f"{last_report.get('route_efficiency', 0):.1f}%"
        ),

        (
            "AI Difficulty",
            f"{last_report.get('ai_difficulty', 1):.2f}"
        )
    ]


    for label, value in report_items:

        draw_text(
            f"{label}:",
            font_medium,
            WHITE,
            250,
            y
        )

        draw_text(
            value,
            font_medium,
            CYAN,
            520,
            y
        )

        y += 55


    draw_text(
        last_report.get(
            "ai_learning",
            ""
        ),
        font_small,
        PURPLE,
        250,
        y + 20
    )

    draw_text(
        "ENTER = Continue",
        font_medium,
        GREEN,
        390,
        600
    )


# ============================================================
# START MISSION
# ============================================================

def start_mission():

    global game_state

    reset_mission()

    game_state = PLAYING


# ============================================================
# NEXT MISSION
# ============================================================

def next_mission():

    global current_level
    global current_mission

    current_mission += 1

    if current_mission > 3:

        current_mission = 1

        current_level += 1

        if current_level > 7:

            current_level = 7
            current_mission = 3

            save_game()

            game_state = REPORT

            return

    save_game()

    start_mission()


# ============================================================
# GARAGE CAR SELECTION
# ============================================================

def select_car(
    car_id
):

    global selected_car
    global coins

    if car_id not in cars:

        return

    car = cars[
        car_id
    ]

    if car[
        "unlocked"
    ]:

        selected_car = car_id

        save_game()

    else:

        cost = car[
            "cost"
        ]

        if coins >= cost:

            coins -= cost

            car[
                "unlocked"
            ] = True

            selected_car = car_id

            save_game()


# ============================================================
# KEYBOARD GARAGE
# ============================================================

def handle_garage_key(
    key
):

    car_map = {

        pygame.K_1: 1,

        pygame.K_2: 2,

        pygame.K_3: 3,

        pygame.K_4: 4
    }

    if key in car_map:

        select_car(
            car_map[key]
        )


# ============================================================
# MAIN LOOP
# ============================================================

load_game()

running = True


while running:

    clock.tick(
        FPS
    )


    # ========================================================
    # EVENTS
    # ========================================================

    for event in pygame.event.get():


        # ----------------------------------------------------
        # WINDOW CLOSE
        # ----------------------------------------------------

        if event.type == pygame.QUIT:

            save_game()

            running = False


        # ====================================================
        # MOUSE BUTTONS
        # ====================================================

        if event.type == pygame.MOUSEBUTTONDOWN:

            mouse_x, mouse_y = event.pos


            # =================================================
            # MAIN MENU
            # =================================================

            if game_state == MENU:


                # START MISSION

                if (
                    350 <= mouse_x <= 650
                    and
                    260 <= mouse_y <= 325
                ):

                    start_mission()


                # GARAGE

                elif (
                    350 <= mouse_x <= 650
                    and
                    350 <= mouse_y <= 415
                ):

                    game_state = GARAGE


                # QUIT

                elif (
                    350 <= mouse_x <= 650
                    and
                    440 <= mouse_y <= 505
                ):

                    save_game()

                    running = False


            # =================================================
            # GARAGE
            # =================================================

            elif game_state == GARAGE:


                # CAR 1

                if (
                    170 <= mouse_x <= 830
                    and
                    160 <= mouse_y <= 250
                ):

                    select_car(1)


                # CAR 2

                elif (
                    170 <= mouse_x <= 830
                    and
                    270 <= mouse_y <= 360
                ):

                    select_car(2)


                # CAR 3

                elif (
                    170 <= mouse_x <= 830
                    and
                    380 <= mouse_y <= 470
                ):

                    select_car(3)


                # CAR 4

                elif (
                    170 <= mouse_x <= 830
                    and
                    490 <= mouse_y <= 580
                ):

                    select_car(4)


            # =================================================
            # MISSION COMPLETE
            # =================================================

            elif game_state == MISSION_COMPLETE:


                # NEXT MISSION

                if (
                    350 <= mouse_x <= 650
                    and
                    510 <= mouse_y <= 570
                ):

                    next_mission()


                # REPLAY

                elif (
                    400 <= mouse_x <= 600
                    and
                    585 <= mouse_y <= 635
                ):

                    start_mission()


            # =================================================
            # GAME OVER
            # =================================================

            elif game_state == GAME_OVER:


                # REPLAY

                if (
                    350 <= mouse_x <= 650
                    and
                    400 <= mouse_y <= 460
                ):

                    start_mission()


                # MAIN MENU

                elif (
                    350 <= mouse_x <= 650
                    and
                    490 <= mouse_y <= 550
                ):

                    game_state = MENU


        # ====================================================
        # KEYBOARD
        # ====================================================

        if event.type == pygame.KEYDOWN:

            key = event.key


            # =================================================
            # MENU
            # =================================================

            if game_state == MENU:

                if key == pygame.K_RETURN:

                    start_mission()

                elif key == pygame.K_g:

                    game_state = GARAGE

                elif key == pygame.K_ESCAPE:

                    save_game()

                    running = False


            # =================================================
            # GARAGE
            # =================================================

            elif game_state == GARAGE:

                if key in [
                    pygame.K_1,
                    pygame.K_2,
                    pygame.K_3,
                    pygame.K_4
                ]:

                    handle_garage_key(
                        key
                    )

                elif key == pygame.K_ESCAPE:

                    game_state = MENU


            # =================================================
            # PLAYING
            # =================================================

            elif game_state == PLAYING:

                if key == pygame.K_ESCAPE:

                    game_state = MENU

                    save_game()


            # =================================================
            # MISSION COMPLETE
            # =================================================

            elif game_state == MISSION_COMPLETE:

                if key == pygame.K_RETURN:

                    next_mission()

                elif key == pygame.K_r:

                    start_mission()

                elif key == pygame.K_ESCAPE:

                    game_state = MENU


            # =================================================
            # GAME OVER
            # =================================================

            elif game_state == GAME_OVER:

                if key == pygame.K_r:

                    start_mission()

                elif key == pygame.K_m:

                    game_state = MENU


            # =================================================
            # REPORT
            # =================================================

            elif game_state == REPORT:

                if key == pygame.K_RETURN:

                    game_state = MENU


    # ========================================================
    # UPDATE
    # ========================================================

    if game_state == PLAYING:

        update_game()


    # ========================================================
    # DRAW
    # ========================================================

    if game_state == MENU:

        draw_menu()

    elif game_state == GARAGE:

        draw_garage()

    elif game_state == PLAYING:

        draw_playing()

    elif game_state == MISSION_COMPLETE:

        draw_mission_complete()

    elif game_state == GAME_OVER:

        draw_game_over()

    elif game_state == REPORT:

        draw_report()


    # ========================================================
    # DISPLAY
    # ========================================================

    pygame.display.flip()


# ============================================================
# EXIT
# ============================================================

save_game()

pygame.quit()