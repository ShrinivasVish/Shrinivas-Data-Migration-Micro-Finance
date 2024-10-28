# http://127.0.0.1:8888/lab?token=dec59d5126a4088303ace976315305ef14b373b4eaa9c027

import json
import glob

def read_json_files(file_names):
    all_customers = []
    for file_name in file_names:
        try:
            with open(f"../../data/{file_name}", 'r') as file:
                data = json.load(file)
                if isinstance(data, list):
                    all_customers.extend(data)
                else:
                    print(f"Warning: {file_name} does not contain a valid JSON array.")
        except Exception as e:
            print(f"Error reading {file_name}: {e}")
    return all_customers

def main():
    # List of customer set filenames
    customer_files = [
        'customer_set_1.json',
        'customer_set_2.json',
        'customer_set_3.json',
        'customer_set_4.json',
        'customer_set_5.json',
        'customer_set_6.json'
    ]

    # Read and combine customer data
    all_customers = read_json_files(customer_files)

    # Write combined data to customers.json
    with open(f"../../data/customers.json", 'w') as output_file:
        json.dump(all_customers, output_file, indent=4)

    print("Successfully combined customer data into customers.json")

if __name__ == "__main__":
    main()