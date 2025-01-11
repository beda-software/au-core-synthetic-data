.PHONY: synthea mapping_script clean-previous-runs

validate-results:
	java -jar validator_cli.jar results/ -ig hl7.fhir.au.core#1.0.0-preview -tx https://tx.dev.hl7.org.au/fhir -hintAboutNonMustSupport

clean-previous-runs:
	rm -rf results/csv/*
	rn -rf results/json/*
	rm -rf au-fhir-test-data/testdata-csv/*
	rm -rf au-fhir-test-data/generated/*
	make -C mapping_script cleanup-source
	make -C mapping_script cleanup-results
	make -C synthea cleanup

generate-basic-synthea-data:
	make -C synthea build
	make -C synthea up

copy-synthea-generated-data-to-mapping-script-folder:
	cp -rf synthea/output/csv/* mapping_script/csv_source/

run-mapping-scripts:
	make -C mapping_script clean-csv
	make -C mapping_script run

run-csv-2-fhir-script:
	cp -rf ./mapping_script/mapping_results/*.csv ./au-fhir-test-data/testdata-csv/
	cp -rf ./mapping_script/mapping_results/*.csv ./results/csv
	cp ./Csv2FhirMapping-linux-x64-binaries/Csv2Fhir ./au-fhir-test-data/Sparked.Csv2FhirMapping/
	- ./mapping-script.sh; 	false
	cp au-fhir-test-data/generated/* ./results/json

create-archive:
	tar -czvf results.tar.gz results/

download-csv2fhir:
    wget https://github.com/hl7au/au-fhir-test-data-utils/releases/latest/download/Csv2FhirMapping-linux-x64.zip
	unzip Csv2FhirMapping-linux-x64.zip
	chmod +x Csv2FhirMapping-linux-x64-binaries/Csv2Fhir

create-mapping-source-folder:
	mkdir mapping_script/csv_source/

pipeline-local: clean-previous-runs generate-basic-synthea-data copy-synthea-generated-data-to-mapping-script-folder run-mapping-scripts run-csv-2-fhir-script validate-results create-archive

pipeline-ci: download-csv2fhir create-mapping-source-folder generate-basic-synthea-data copy-synthea-generated-data-to-mapping-script-folder run-mapping-scripts run-csv-2-fhir-script validate-results create-archive
