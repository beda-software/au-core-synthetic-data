import os
import uuid
import pandas as pd
import yaml
import argparse

def read_csv_files(path_to_original):
    csv_files = [
        os.path.join(path_to_original, file)
        for file in os.listdir(path_to_original)
        if file.endswith('.csv')
    ]

    if not csv_files:
        raise ValueError(f"No CSV files found in the directory: {path_to_original}")

    dataframes = {}
    for csv_file in csv_files:
        resource_type = csv_file.split('/')[-1].split('.csv')[0]
        df = pd.read_csv(csv_file)
        dataframes[resource_type] = df

    return dataframes

def read_yaml_config(path_to_config):
    with open(path_to_config, 'r') as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config

def save_patients_mapping_file(path_to_result, mapped_patient_ids):
    full_path_to_result = "{}/{}".format(path_to_result, "mapped_patients_info.yaml")
    with open(full_path_to_result, 'w') as file:
        yaml.dump({"patients": mapped_patient_ids}, file, default_flow_style=False, sort_keys=False)

def replace_data(generated_data, mapped_patient_ids, mapping_config, add_id_column, rename_files, delete_files, path_to_result):
    for resource_type in generated_data.keys():
        if resource_type in delete_files:
            print(f"Skip processing of the {resource_type}")
            continue

        modified_df = generated_data[resource_type]

        if resource_type in add_id_column:
            print(f"Add id column for {resource_type}")
            modified_df['id'] = [uuid.uuid4() for _ in range(len(modified_df))]

        print("Replace patient ids if needed...")
        modified_df.replace(mapped_patient_ids, inplace=True)

        if resource_type in mapping_config:
            for mapping_config_item in mapping_config[resource_type]:
                print(f"Rename column from {mapping_config_item['from']} to {mapping_config_item['to']} for {resource_type}")
                modified_df.rename(columns={mapping_config_item['from']: mapping_config_item['to']}, inplace=True)

        result_filename = f"{rename_files.get(resource_type, resource_type)}.csv"
        print(f"Save file with name {result_filename}")

        output_path = os.path.join(path_to_result, result_filename)
        modified_df.to_csv(output_path, index=False)

def check_config(config_data):
    problems = []

    mapping_config = config_data.get('mapping', {})
    mapping_config_keys = mapping_config.keys()

    if len(mapping_config_keys) != len(list(set(mapping_config_keys))):
        problems.append("Duplicate keys in mapping variable")

    return problems

def main(path_to_original, path_to_config, path_to_result):
    try:
        data = read_csv_files(path_to_original)
        config = read_yaml_config(path_to_config)
        target_patient_ids = config.get('target_patient_ids', [])
        mapping_config = config.get('mapping', {})
        rename_files = config.get('rename_files', {})
        delete_files = config.get('delete_files', [])
        add_id_column = config.get('add_ids_column', [])

        if not target_patient_ids:
            print("No target_patient_ids found in the YAML configuration.")

        mapped_patient_ids = dict(zip(target_patient_ids, list(data['patients']['Id'])))

        save_patients_mapping_file(path_to_result, mapped_patient_ids)
        replace_data(data, mapped_patient_ids, mapping_config, add_id_column, rename_files, delete_files, path_to_result)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process CSV files and YAML configuration.")
    parser.add_argument("path_to_original", type=str, help="Path to the directory containing original CSV files.")
    parser.add_argument("path_to_config", type=str, help="Path to the YAML configuration file.")
    parser.add_argument("path_to_result", type=str, help="Path to save the result output.")

    args = parser.parse_args()

    main(args.path_to_original, args.path_to_config, args.path_to_result)

