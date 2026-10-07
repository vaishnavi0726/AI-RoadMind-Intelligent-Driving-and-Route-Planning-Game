import json
import os
import matplotlib.pyplot as plt


ANALYTICS_FILE = "mission_history.json"


# ============================================================
# LOAD MISSION HISTORY
# ============================================================

def load_history():

    if not os.path.exists(
        ANALYTICS_FILE
    ):

        return []

    try:

        with open(
            ANALYTICS_FILE,
            "r"
        ) as file:

            data = json.load(file)

        if isinstance(data, list):

            return data

        return []

    except Exception:

        return []


# ============================================================
# SAVE MISSION RESULT
# ============================================================

def save_mission_result(
    level,
    mission,
    time_taken,
    collisions,
    fuel_used,
    route_efficiency,
    score,
    ai_difficulty
):

    history = load_history()

    result = {

        "level": int(level),

        "mission": int(mission),

        "time_taken": round(
            float(time_taken),
            2
        ),

        "collisions": int(
            collisions
        ),

        "fuel_used": round(
            float(fuel_used),
            2
        ),

        "route_efficiency": round(
            float(route_efficiency),
            2
        ),

        "score": int(
            score
        ),

        "ai_difficulty": float(
            ai_difficulty
        )
    }

    history.append(
        result
    )

    try:

        with open(
            ANALYTICS_FILE,
            "w"
        ) as file:

            json.dump(
                history,
                file,
                indent=4
            )

    except Exception as e:

        print(
            "Analytics save error:",
            e
        )

    return result


# ============================================================
# CREATE PERFORMANCE GRAPH
# ============================================================

def create_performance_graph():

    history = load_history()

    if not history:

        return False

    missions = []
    scores = []
    collisions = []
    efficiency = []

    for i, data in enumerate(
        history
    ):

        missions.append(
            i + 1
        )

        scores.append(
            data.get(
                "score",
                0
            )
        )

        collisions.append(
            data.get(
                "collisions",
                0
            )
        )

        efficiency.append(
            data.get(
                "route_efficiency",
                0
            )
        )

    plt.figure(
        figsize=(10, 6)
    )

    plt.plot(
        missions,
        scores,
        marker="o",
        label="Score"
    )

    plt.plot(
        missions,
        efficiency,
        marker="o",
        label="Route Efficiency"
    )

    plt.plot(
        missions,
        collisions,
        marker="o",
        label="Collisions"
    )

    plt.title(
        "AI RoadMind - Player Performance Analytics"
    )

    plt.xlabel(
        "Mission"
    )

    plt.ylabel(
        "Performance"
    )

    plt.legend()

    plt.grid(
        True
    )

    plt.tight_layout()

    try:

        plt.savefig(
            "roadmind_performance.png"
        )

    except Exception as e:

        print(
            "Graph creation error:",
            e
        )

        plt.close()

        return False

    plt.close()

    return True


# ============================================================
# GET PERFORMANCE SUMMARY
# ============================================================

def get_performance_summary():

    history = load_history()

    if not history:

        return {

            "missions": 0,

            "average_score": 0,

            "average_collisions": 0,

            "average_efficiency": 0,

            "total_fuel_used": 0
        }

    total_score = sum(
        item.get(
            "score",
            0
        )
        for item in history
    )

    total_collisions = sum(
        item.get(
            "collisions",
            0
        )
        for item in history
    )

    total_efficiency = sum(
        item.get(
            "route_efficiency",
            0
        )
        for item in history
    )

    total_fuel = sum(
        item.get(
            "fuel_used",
            0
        )
        for item in history
    )

    count = len(
        history
    )

    return {

        "missions": count,

        "average_score": round(
            total_score / count,
            2
        ),

        "average_collisions": round(
            total_collisions / count,
            2
        ),

        "average_efficiency": round(
            total_efficiency / count,
            2
        ),

        "total_fuel_used": round(
            total_fuel,
            2
        )
    }