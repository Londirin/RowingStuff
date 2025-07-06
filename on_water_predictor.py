import math

# --- Helper Functions for Time Conversion ---

def time_to_seconds(time_str: str) -> float:
    """Converts a time string in M:SS.s or MM:SS.s format to total seconds."""
    try:
        parts = time_str.split(':')
        minutes = int(parts[0])
        seconds = float(parts[1])
        return minutes * 60 + seconds
    except (ValueError, IndexError):
        raise ValueError("Invalid time format. Please use M:SS.s or MM:SS.s")


def seconds_to_time(seconds: float) -> str:
    """Converts a total number of seconds to a M:SS.s formatted string."""
    if seconds is None or not math.isfinite(seconds):
        return "N/A"
    minutes = int(seconds // 60)
    remaining_seconds = seconds % 60
    return f"{minutes}:{remaining_seconds:04.1f}"


# --- Boat Parameters ---
# Contains number of rowers, standard boat weight (kg), and a calibrated
# boat efficiency constant (c_boat) derived from world-class performances.
BOAT_DATA = {
    "1x": {"rowers": 1, "boat_weight_kg": 14, "c_boat": 1.47},
    "2-": {"rowers": 2, "boat_weight_kg": 27, "c_boat": 1.54},
    "2x": {"rowers": 2, "boat_weight_kg": 27, "c_boat": 1.57},
    "4-": {"rowers": 4, "boat_weight_kg": 50, "c_boat": 1.63},
    "4x": {"rowers": 4, "boat_weight_kg": 52, "c_boat": 1.66},
    "8+": {"rowers": 8, "boat_weight_kg": 96, "c_boat": 1.76},
}


# --- Core Calculator Function ---

def predict_on_water_speed(erg_score_2k: str, avg_crew_weight_kg: float, boat_type: str) -> dict:
    """Predicts on-water rowing speed based on erg score, crew weight, and boat."""
    if boat_type not in BOAT_DATA:
        raise ValueError(
            f"Boat type '{boat_type}' not recognized. Use one of {list(BOAT_DATA.keys())}"
        )

    # 1. Calculate the rower's power output from the erg score
    erg_time_sec = time_to_seconds(erg_score_2k)
    avg_500m_split_sec = erg_time_sec / 4.0  # 2k score -> avg 500m split

    # pace (s/m) = split / 500. Power = 2.8 / pace^3
    pace = avg_500m_split_sec / 500.0
    power_watts = 2.80 / (pace ** 3)

    # 2. Get boat parameters and calculate total system mass
    boat_info = BOAT_DATA[boat_type]
    num_rowers = boat_info["rowers"]
    boat_weight = boat_info["boat_weight_kg"]

    total_crew_weight = avg_crew_weight_kg * num_rowers
    # Add weight for the coxswain in an 8+, standard is 55kg
    if boat_type == "8+":
        total_crew_weight += 55

    total_mass_kg = total_crew_weight + boat_weight

    # 3. Apply the physics model to predict on-water speed
    c_boat = boat_info["c_boat"]
    total_power = power_watts * num_rowers

    # Speed(m/s) = C_boat * (Total_Power)^(1/3) * (Total_Mass)^(-1/6)
    predicted_speed_ms = c_boat * (total_power ** (1/3)) * (total_mass_kg ** (-1/6))

    # 4. Convert speed back to a 500m split time
    predicted_500m_split_sec = 500 / predicted_speed_ms

    return {
        "input_erg_score_2k": erg_score_2k,
        "input_avg_weight_kg": avg_crew_weight_kg,
        "input_boat_type": boat_type,
        "calculated_power_per_rower_w": round(power_watts),
        "predicted_on_water_speed_ms": round(predicted_speed_ms, 2),
        "predicted_on_water_500m_split": seconds_to_time(predicted_500m_split_sec),
    }


# --- Example Usage ---
# You can change these values to test the calculator
if __name__ == "__main__":
    erg_score = "6:40.0"  # A good heavyweight 2k erg score
    weight = 90.0  # in kg
    boat = "8+"  # An eight-person shell

    result = predict_on_water_speed(erg_score, weight, boat)
    print(result)
