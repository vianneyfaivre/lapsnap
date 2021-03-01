# lapsnap

This script takes pictures every X seconds by using your laptop camera. 

A folder will be created with today's date, pictures will be put in that folder.

## Requirements

- Python 3
- Open-CV https://docs.opencv.org/4.2.0/d6/d00/tutorial_py_root.html

## Run (linux)

Install the dependencies

```
pip3 install -r requirements.txt
```

Run! (will snap every 5 seconds)

```
python3 lapsnap.py --lap=5
```