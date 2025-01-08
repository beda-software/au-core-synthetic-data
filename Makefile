.PHONY: synthea mapping_script

validate-result:
	# java -jar validator_cli.jar results/ -ig hl7.fhir.au.core#1.0.0-preview -tx https://tx.dev.hl7.org.au/fhir
	java -jar validator_cli.jar results/ -ig hl7.fhir.au.core#1.0.0-preview -hintAboutNonMustSupport

pipeline:
	rm -rf results/*
	rm -rf au-fhir-test-data/testdata-csv/*
	rm -rf au-fhir-test-data/generated/*
	make -C mapping_script cleanup-source
	make -C mapping_script cleanup-results
	make -C synthea cleanup
	make -C synthea build
	make -C synthea up
	cp -rf synthea/output/csv/* mapping_script/csv_source/
	make -C mapping_script clean-csv
	make -C mapping_script run
	cp -rf ./mapping_script/mapping_results/*.csv ./au-fhir-test-data/testdata-csv/
	cp ./Csv2FhirMapping-linux-x64-binaries/Csv2Fhir ./au-fhir-test-data/Sparked.Csv2FhirMapping/
	- ./mapping-script.sh; 	false
	cp au-fhir-test-data/generated/* ./results/
	validate-result
