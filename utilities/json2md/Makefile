install:
	python3 -m venv "json2md_venv"
	. json2md_venv/bin/activate && pip3 install --upgrade pip && pip3 install -r requirements.txt
	chmod +x json2md.py
zip:
	mkdir -p dist/json2md
	zip -r dist/json2md.zip dist/json2md && zip -g -r dist/json2md.zip requirements.txt json2md.py template.md Makefile README.md
clean_env:
	rm -rf "json2md_venv"
