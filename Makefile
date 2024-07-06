install:
	pip -r requirments.txt

run:
	python main.py

compile:
	cd binder_r
	maturin build --release
	pip install ./target/wheel/*
	cd ..