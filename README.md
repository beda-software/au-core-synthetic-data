
# AU Core Synthetic Data

Data generated by Synthea then mapped to be valid according to AU Core IG

## Pipeline

1. **Generate Data**: Use dockerized Synthea and a custom module to generate data in CSV format.
2. **Map/Post-Process CSV Files**:
    * Map target patients to the generated patients (because it is not possible to assign specific patient IDs in Synthea data).
    * Rename column names in the generated CSV files according to the mapping configuration.
    * Rename the resulting CSV files based on the mapping configuration.
    * Delete unused CSV files.
    * Add additional columns to the generated CSV files to maintain a structure for the Csv2Fhir.
    * Perform post-processing using the configuration to enrich the data, as Synthea has a limited number of fields.
3. **Generate FHIR Resources**: Use the Csv2Fhir application to convert CSV data into FHIR resources in JSON format.
4. **Validate Results**: Validate the generated FHIR resources using the official FHIR Validator CLI.
5. **Create an Archive**: Bundle the generated FHIR resources in both JSON and CSV formats into an archive.

## Run

```bash
./download-mapper.sh
```

``` bash
make pipeline
```

