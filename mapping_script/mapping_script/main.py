import os
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

    return dataframes, mapping_fields

def read_yaml_config(path_to_config):
    with open(path_to_config, 'r') as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config

def main(path_to_original, path_to_config, path_to_result):
    try:
        data = read_csv_files(path_to_original)

        config = read_yaml_config(path_to_config)

        target_patient_ids = config.get('target_patient_ids', [])
        if not target_patient_ids:
            print("No target_patient_ids found in the YAML configuration.")

        mapped_patient_ids = dict(zip(target_patient_ids, list(data['patients']['Id'])))

        full_path_to_result = "{}/{}".format(path_to_result, "mapped_patients_info.yaml")
        with open(full_path_to_result, 'w') as file:
            yaml.dump({"patients": mapped_patient_ids}, file, default_flow_style=False, sort_keys=False)

        for resource_type in data.keys():
            modified_df = data[resource_type]
            for target_patient_id in mapped_patient_ids.keys():
                modified_df = modified_df.replace(mapped_patient_ids[target_patient_id], target_patient_id)
            result_filename = "{}.csv".format(resource_type)
            modified_df.to_csv("{}/{}".format(path_to_result, result_filename), index=False)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process CSV files and YAML configuration.")
    parser.add_argument("path_to_original", type=str, help="Path to the directory containing original CSV files.")
    parser.add_argument("path_to_config", type=str, help="Path to the YAML configuration file.")
    parser.add_argument("path_to_result", type=str, help="Path to save the result output.")

    args = parser.parse_args()

    main(args.path_to_original, args.path_to_config, args.path_to_result)

