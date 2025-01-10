import os
import csv

def process_csv_files(folder_path):
    if not os.path.isdir(folder_path):
        print(f"Error: {folder_path} is not a valid directory.")
        return

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)

        if os.path.isfile(file_path) and file_name.endswith('.csv'):
            print(f"Processing file: {file_name}")
            if file_name != "patients.csv":
                process_csv_file(file_path)


def process_csv_file(file_path):
    temp_file_path = file_path + '.tmp'

    with open(file_path, 'r', newline='', encoding='utf-8') as infile, \
         open(temp_file_path, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        header = next(reader, None)
        if header:
            writer.writerow(header)

        for row in reader:
            if any("250106-" in cell for cell in row):
                writer.writerow(row)

    os.replace(temp_file_path, file_path)
    print(f"Filtered file saved: {file_path}")

if __name__ == "__main__":
    process_csv_files("./csv_source/")
