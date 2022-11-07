.phony:

env:
	export $(cat .env | grep -v ^# )

pdf:
	python3 main.py

csv:
	python3 pdf2doc.py