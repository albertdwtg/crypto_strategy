pre-commit:
	terraform -chdir=tf_files fmt
	black src/
	vulture src/conf.py --min-confidence 90