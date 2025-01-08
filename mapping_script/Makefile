run:
	poetry run python mapping_script/main.py ./csv_source/ ./config.yaml ./mapping_results

cleanup-source:
	rm -rf ./csv_source/*

cleanup-results:
	rm -rf ./mapping_results/*

clean-csv:
	sudo poetry run python mapping_script/csv_cleaner.py
