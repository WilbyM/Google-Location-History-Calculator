import os
import csv
import json
from datetime import datetime, timezone, timedelta

# Define a function to calculate the duration of a location visit in hours
def calculate_duration(start_timestamp, end_timestamp):
    start_time = datetime.fromtimestamp(start_timestamp / 1000, timezone.utc)
    end_time = datetime.fromtimestamp(end_timestamp / 1000, timezone.utc)
    duration = end_time - start_time
    return duration.total_seconds() / 3600

# Define a function to parse a single JSON file and return a dictionary with location names and their durations
def parse_location_history(file_path):
    with open(file_path) as file:
        data = json.load(file)

    location_durations = {}
    location_days = {}

    for place_visit in data['timelineObjects']:
        if 'placeVisit' in place_visit:
            location_info = place_visit['placeVisit']['location']
            location_name = location_info.get('name', location_info.get('address'))
            start_timestamp = datetime.fromisoformat(place_visit['placeVisit']['duration']['startTimestamp'][:-1])
            end_timestamp = datetime.fromisoformat(place_visit['placeVisit']['duration']['endTimestamp'][:-1])
            duration = calculate_duration(start_timestamp.timestamp() * 1000, end_timestamp.timestamp() * 1000)

            if location_name in location_durations:
                location_durations[location_name] += duration
            else:
                location_durations[location_name] = duration

            date_range = set()
            current_date = start_timestamp.date()
            while current_date <= end_timestamp.date():
                date_range.add(current_date)
                current_date += timedelta(days=1)

            if location_name in location_days:
                location_days[location_name].update(date_range)
            else:
                location_days[location_name] = date_range

    return location_durations, location_days

# Define a function to parse all JSON files in a directory and return a dictionary with location names and their total durations
def parse_location_history_directory(directory_path):
    location_durations = {}
    location_days = {}

    for filename in os.listdir(directory_path):
        if filename.endswith('.json'):
            file_path = os.path.join(directory_path, filename)
            file_locations, file_days = parse_location_history(file_path)
            for location, duration in file_locations.items():
                if location in location_durations:
                    location_durations[location] += duration
                    location_days[location].update(file_days[location])
                else:
                    location_durations[location] = duration
                    location_days[location] = file_days[location]

    # Sort location durations in descending order
    location_durations = dict(sorted(location_durations.items(), key=lambda item: item[1], reverse=True))

    return location_durations, location_days

# Locations
directory_path = os.path.join(os.getcwd(), 'timeline-json')
location_durations = parse_location_history_directory(directory_path)

# Output the location durations to the console and a CSV file
output_directory = os.path.join(os.getcwd(), 'output')
os.makedirs(output_directory, exist_ok=True)

# Output to console
for location, duration in location_durations[0].items():
    num_days = len(location_durations[1][location])
    print(f'{location}: {duration:.2f} hours over {num_days} days')

# Output to CSV file
csv_path = os.path.join(output_directory, 'location_durations.csv')
with open(csv_path, mode='w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['Location', 'Duration (hours)', 'Days'])
    for location, duration in location_durations.items():
        num_days = len(location_days[location])
        writer.writerow([location, f'{duration:.2f}', num_days])
print(f'Location durations written to {csv_path}')
