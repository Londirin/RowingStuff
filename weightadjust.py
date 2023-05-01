# Prompt user for the distance raced
distance = float(input("Enter the distance raced (meters): "))

# Prompt user for number of rowers
num_rowers = int(input("Enter the number of rowers: "))

# Define list to store rower data
rower_data = []

# Get user inputs for rower names and data
for i in range(num_rowers):
    name = input(f"Enter name of rower {i+1}: ")
    time_min = int(input(f"Enter the time in minutes for {name}: "))
    time_sec = float(input(f"Enter the time in seconds for {name}: "))
    weight = float(input(f"Enter the weight in pounds for {name}: "))

    # Convert time to seconds and calculate weight factor
    time_seconds = 60 * time_min + time_sec
    weight_factor = (weight / 270) ** 0.222

    # Calculate corrected time and distance
    corrected_time = weight_factor * time_seconds

    # Add rower data to list
    rower_data.append((name, corrected_time))

# Sort rower data based on corrected time
rower_data_sorted = sorted(rower_data, key=lambda x: x[1])

# Print the results in order of fastest to slowest, including the difference from the fastest rower
print("Results:")
fastest_split = None
fastest_corrected_time = None
for i, rower in enumerate(rower_data_sorted):
    rank = i + 1
    name = rower[0]
    corrected_time = rower[1]
    split_seconds = corrected_time / (distance / 500.0)
    split_min = int(split_seconds // 60)
    split_sec = int(split_seconds % 60)
    corrected_time_min = int(corrected_time // 60)
    corrected_time_sec = int(corrected_time % 60)

    # Print rower data
    if i == 0:
        print(f"{rank}. {name}: Weight-adjusted split: {split_min}:{split_sec:02d}, Weight-adjusted time: {corrected_time_min}:{corrected_time_sec:02d}")
        fastest_split = split_seconds
        fastest_corrected_time = corrected_time
    else:
        split_difference = split_seconds - fastest_split
        corrected_time_difference = corrected_time - fastest_corrected_time
        print(f"{rank}. {name}: Weight-adjusted split: {split_min}:{split_sec:02d} (+{split_difference:.2f} sec), Weight-adjusted time: {corrected_time_min}:{corrected_time_sec:02d} (+{corrected_time_difference:.2f} sec)")

# Alternative output format
#print("\nResults:")
#for i, rower in enumerate(rower_data_sorted):
#    rank = i + 1
#    name = rower[0]
#    corrected_time = rower[1]
#    split_seconds = corrected_time / (distance / 500.0)
#    split_difference = split_seconds - fastest_split
#    corrected_time_difference = corrected_time - fastest_corrected_time
#    print(f"{rank}. {name} ({split_difference:+.2f}s / {corrected_time_difference:+.2f}s): {split_seconds:.2f}s / {corrected_time:.2f}s")
