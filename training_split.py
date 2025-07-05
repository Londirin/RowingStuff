import math


def time_to_seconds(time_str: str) -> float:
    """Convert M:SS.s or MM:SS.s formatted string to seconds."""
    try:
        minutes, sec = time_str.split(":")
        return int(minutes) * 60 + float(sec)
    except (ValueError, IndexError):
        raise ValueError("Invalid time format. Please use M:SS.s or MM:SS.s")


def seconds_to_time(seconds: float) -> str:
    """Convert seconds to M:SS.s string."""
    if seconds is None or not math.isfinite(seconds):
        return "N/A"
    minutes = int(seconds // 60)
    rem = seconds % 60
    return f"{minutes}:{rem:04.1f}"


def calculate_training_split(race_distance_m: int,
                              race_time_str: str,
                              race_stroke_rate_spm: int,
                              training_stroke_rate_spm: int) -> dict:
    """Calculate training power and split while keeping EWpS constant."""
    race_time_sec = time_to_seconds(race_time_str)
    if race_time_sec <= 0:
        raise ValueError("Race time must be positive.")
    race_speed = race_distance_m / race_time_sec

    race_power = 2.8 * (race_speed ** 3)

    if race_stroke_rate_spm <= 0:
        raise ValueError("Race stroke rate must be positive.")
    ewps = (race_power * 60) / race_stroke_rate_spm

    training_power = (training_stroke_rate_spm / 60) * ewps

    if training_power <= 0:
        training_speed = 0
    else:
        training_speed = (training_power / 2.8) ** (1/3)

    if training_speed == 0:
        training_split_sec = float('inf')
    else:
        training_split_sec = 500 / training_speed

    return {
        "target_ewps_joules": round(ewps, 1),
        "training_power_watts": round(training_power, 1),
        "training_split_500m_str": seconds_to_time(training_split_sec),
        "training_split_seconds": round(training_split_sec, 1),
    }


if __name__ == "__main__":
    distance = int(input("Enter race distance (m): "))
    time_str = input("Enter target race time (M:SS.s): ")
    race_rate = int(input("Enter race stroke rate (spm): "))
    train_rate = int(input("Enter training stroke rate (spm): "))

    result = calculate_training_split(distance, time_str, race_rate, train_rate)

    print(f"\nTarget EWpS: {result['target_ewps_joules']} J")
    print(f"Required training power: {result['training_power_watts']} W")
    print(f"Training split: {result['training_split_500m_str']} per 500m")
