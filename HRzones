# Get user input for age or HRmax
input_type = input("Enter 'age' or 'HRmax': ")
if input_type == 'age':
    age = int(input("Enter your age: "))
    HRmax = round(207 - (0.7 * age))
elif input_type == 'HRmax':
    HRmax = int(input("Enter your HRmax: "))
else:
    print("Invalid input type.")
    exit()

# Define 5 heart rate zones based on intensity levels
zone1 = [round(HRmax * 0.5), round(HRmax * 0.6)]
zone2 = [round(HRmax * 0.6), round(HRmax * 0.7)]
zone3 = [round(HRmax * 0.7), round(HRmax * 0.8)]
zone4 = [round(HRmax * 0.8), round(HRmax * 0.9)]
zone5 = [round(HRmax * 0.9), HRmax]

# Create a list of zones, intensities, and corresponding ranges
zones = ['Zone 1', 'Zone 2', 'Zone 3', 'Zone 4', 'Zone 5']
intensities = ['Very light', 'Light', 'Moderate', 'Hard', 'Maximum']
ranges = [zone1, zone2, zone3, zone4, zone5]

# Calculate the width required for the range header
range_header_width = max([len(str(r[1])) for r in ranges] + [5]) + 3

# Print table header
print('| Heart rate zone | Intensity  |   Range  |'.format(' ' * (range_header_width-5)))
print('|-----------------|------------|----------|'.format('-' * (range_header_width+1)))

# Print heart rate zones, intensities, and ranges in a table
for zone, intensity, r in zip(zones, intensities, ranges):
    print('|{:^17}|{:^12}|{:>4} - {:<3}|'.format(zone, intensity, r[0], r[1]))

# Print HRmax data point
print('\nYour HRmax is: {} bpm'.format(HRmax))
