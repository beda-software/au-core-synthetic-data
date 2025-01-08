#!/bin/bash

cd au-fhir-test-data/Sparked.Csv2FhirMapping/ || exit

declare -a resources=(
    "Patient"
    "HealthcareService"
    "Organization"
    "Location"
    "Practitioner"
    "PractitionerRole"
    "RelatedPerson"
    "Encounter"
    "AllergyIntolerance"
    "Condition"
    "Immunization"
    "Observation"
    "Procedure"
    "Medication"
    "MedicationRequest"
)

for resource in "${resources[@]}"; do
    echo "Processing resource: $resource"
    ./Csv2Fhir "$resource" "../testdata-csv/AU Core Sample Data - ${resource}.csv" ../generated/
done

