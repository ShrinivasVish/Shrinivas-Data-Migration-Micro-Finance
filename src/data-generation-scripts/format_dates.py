import json
from datetime import datetime, timedelta, timezone


def convert_to_utc_iso8601(date_str):
    """Convert a date string in 'yyyy-mm-dd' format to ISO 8601 UTC format adjusted to IST."""
    # Check if the date string is not None
    if date_str is not None:
        # Parse the date string
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")

        # Set time to midnight (00:00:00) and make it timezone aware in UTC
        utc_time = date_obj.replace(tzinfo=timezone.utc)

        # Adjust to IST (UTC+5:30)
        ist_time = utc_time + timedelta(hours=5, minutes=30)

        # Return ISO 8601 formatted string
        return ist_time.isoformat()

    # Return None if the date string is None
    return None


def process_json(input_file, output_file, keys_to_transform):
    """Process the JSON file and convert specified date keys to ISO 8601 UTC format."""
    # Read the input JSON file
    with open(input_file, "r") as file:
        data = json.load(file)

    # Loop through each object in the array
    for item in data:
        for key in keys_to_transform:
            if key in item:
                # Convert the date format
                item[key] = convert_to_utc_iso8601(item[key])

    # Write the updated data back to a new JSON file
    with open(output_file, "w") as file:
        json.dump(data, file, indent=4)


input_json_file = "../../data/customer_set_7.json"  # Replace with your input JSON file
output_json_file = "../../data/customer_set_7_with_UTC_dates.json"  # Updated output file to avoid overwriting
keys_to_convert = ["joined_date"]  # Replace with the keys you want to transform

process_json(input_json_file, output_json_file, keys_to_convert)
print(f"Processed JSON written to {output_json_file}.")
