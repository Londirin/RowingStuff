import argparse
import math
import sys


def calculate_target_watts(target_2k_time: str) -> float:
    """Return average watts required for the desired 2k time."""
    try:
        minutes, seconds = map(float, target_2k_time.split(":"))
        total_seconds = minutes * 60 + seconds
        if total_seconds <= 0:
            raise ValueError("Time must be positive.")
    except ValueError:
        print("Error: Invalid time format. Please use 'M:SS' or 'M:SS.s'.", file=sys.stderr)
        sys.exit(1)

    split_seconds = total_seconds / 4.0
    return 2.80 * (500 / split_seconds) ** 3


def calculate_weeks_to_goal(current_watts: float,
                             target_watts: float,
                             growth_percentage: float,
                             weeks_per_cycle: int) -> int:
    """Return the weeks needed to reach target watts."""
    if current_watts >= target_watts:
        return 0

    multiplier = 1 + (growth_percentage / 100.0)
    cycles = math.log(target_watts / current_watts) / math.log(multiplier)
    return int(math.ceil(cycles) * weeks_per_cycle)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Rowing Goal Planner: Calculate the time to reach a 2k erg goal.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "-p",
        "--power",
        type=float,
        required=True,
        help="Your current sustained power output in watts (e.g., 265).",
    )
    parser.add_argument(
        "-t",
        "--target",
        type=str,
        required=True,
        help="Your target 2,000-meter time in 'M:SS' format (e.g., '6:19').",
    )
    parser.add_argument(
        "-g",
        "--growth",
        type=float,
        default=3.0,
        help="The percentage of power improvement per cycle (default: 3.0).",
    )
    parser.add_argument(
        "-w",
        "--weeks",
        type=int,
        default=2,
        help="The number of weeks in each improvement cycle (default: 2).",
    )

    args = parser.parse_args()

    target_watts = calculate_target_watts(args.target)
    weeks_needed = calculate_weeks_to_goal(
        args.power,
        target_watts,
        args.growth,
        args.weeks,
    )

    print("\n--- Rowing Goal Analysis ---")
    print(f"Current Power:         {args.power:.0f} Watts")
    print(f"Target 2k Time:        {args.target}")
    print(f"Power Required for Goal: {target_watts:.0f} Watts")
    print("-" * 28)
    print("Training Plan:")
    print(f"  - Improve power by {args.growth}% every {args.weeks} weeks.")
    print("\n\U0001F3C1 RESULT:")
    if weeks_needed == 0:
        print("  Congratulations! You are already at or above the power level for your goal.")
    else:
        print(f"  It will take approximately {weeks_needed} weeks to reach your goal.")
    print("-" * 28)


if __name__ == "__main__":
    main()
