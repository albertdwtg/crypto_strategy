pre-commit:
	terraform -chdir=tf_files fmt
	black src/
	black tests/
	black main.py
	vulture src/conf.py --min-confidence 90