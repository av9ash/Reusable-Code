import csv
import os


def write_headers_to_csv(column_names, target_file):
    # If file doesn't exist create a new one and add headers to file.
    if not os.path.exists(target_file):
        with open(target_file, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=column_names)
            writer.writeheader()


def write_row_to_csv(column_names, row_data, target_file):
    # Add a new row
    with open(target_file, 'a+', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=column_names)
        writer.writerow(row_data)


def write_dict_to_csv(column_names, data, filename):
    # Add data each in a new row
    with open(filename, 'a+', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=column_names)
        for row_data in data:
            writer.writerow(row_data)
