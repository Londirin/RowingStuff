# Get user input for the split time
split_min = int(input("Enter the split time (minutes): "))
split_sec = int(input("Enter the split time (seconds): "))

# Convert the split time to seconds per 500m
split_seconds = 60*split_min + split_sec
split_seconds_per_500m = split_seconds/500.0

# Calculate the equivalent watt output using the formula: W = 2.8 / (s/500)^3
watt_output = 2.8 / (split_seconds_per_500m**3)

# Print the results
print(f"The equivalent watt output for a split time of {split_min}:{split_sec:02d} per 500m is {watt_output:.2f} watts.")
