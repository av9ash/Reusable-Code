import csv
import os
from tempfile import NamedTemporaryFile
import shutil


def read_csv(target_file):
    """
    Read rows from csv file.
    :param target_file: path where file is saved
    :return: list
    """
    rows = []
    with open(target_file) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            rows.append(row)
    return rows


def write_headers_to_csv(column_names, target_file):
    """
    Write column names to target csv file.
    :param column_names: list of column headers
    :param target_file: path where file is saved
    :return: None
    """
    # If file doesn't exist create a new one and add headers to file.
    if not os.path.exists(target_file):
        with open(target_file, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=column_names)
            writer.writeheader()


def write_row_to_csv(column_names, row_data, target_file):
    """
    Write one row of data to target file
    :param column_names: list of column headers
    :param row_data: data dictionary
    :param target_file: path where file is saved
    :return: None
    """
    # Add a new row
    with open(target_file, 'a+', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=column_names)
        writer.writerow(row_data)


def write_dict_to_csv(column_names, data, target_file):
    """
    Write rows of data to target file
    :param column_names: list of column headers
    :param data: list of data dictionary
    :param target_file: path where file is saved
    :return: None
    """
    # Add data each in a new row
    with open(target_file, 'a+', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=column_names)
        for row_data in data:
            writer.writerow(row_data)


def update_rows_in_csv(column_names, data, target_file):
    """
    Update existing rows in csv file
    :param column_names: list of column headers
    :param data: list of data dictionary
    :param target_file: path where file is saved
    :return: None
    """
    if os.path.exists(target_file):
        # Create a new temporary CSV file
        tempfile = NamedTemporaryFile(mode='w', delete=False)

        # Read values from existing CSV file
        with open(target_file, 'r') as csvfile, tempfile:
            reader = csv.DictReader(csvfile, fieldnames=column_names)
            writer = csv.DictWriter(tempfile, fieldnames=column_names)
            # Update and write rows to the temporary file
            for row in reader:
                # # Code to update values here
                # row = {'column1': row['column1'], 'column2': row['column2'],
                #        'column3': row['column3'], 'column4': row['column4'],
                #        'column5': row['column5'], 'column6': row['column6'], 'column7': row['column7']}
                writer.writerow(row)

        # Replace original file with temporary file
        shutil.move(tempfile.name, target_file)
    else:
        print('File to update does not exist.')
