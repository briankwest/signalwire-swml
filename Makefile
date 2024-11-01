build:
	python3 -m venv "./venv"
	./venv/bin/pip install twine build
	./venv/bin/ython3 -m build

upload:
	./venv/bin/twine upload dist/*

clean:
	git clean -fdx