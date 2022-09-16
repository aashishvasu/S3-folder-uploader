# S3-folder-uploader (S3FU)
A simple and sweet folder uploader for S3-compliant object storage made in python. Has multithreaded uploading. Made using [PySimpleGUI](https://www.pysimplegui.org).


## Getting Started
S3FU is built using python and a few libraries to be a multithreaded option to upload entire folders to S3-compliant storage.

### Usage
- Get the [latest release](/releases/latest) or clone the repo
- Install the [prerequisites](#Prerequisites) (see below)
- Fill out the `settings.ini` file based on your S3 settings
- Run using
	```sh
	py main.py
	```

and you're good to go!

### Prerequisites
- Python 3.7+
- [PySimpleGui](https://www.pysimplegui.org)
- [boto3](https://pypi.org/project/boto3/)

### Installing
Install the prerequisites manually, or using the included `requirements.txt`.

**NOTE: I would recommend [using a virtual environment](https://docs.python.org/3/library/venv.html), but that's obviously optional.**
#### Virtual Environment (optional)
```sh
# Create virtual environment
py -m venv venv 
```

#### Using `requirements.txt` 
```sh
pip install -r requirements.txt
```

#### Manually
```sh
# boto
pip install boto3

# PySimpleGui
pip install pysimplegui
```

### Development
- All of the UI code except the error window is in `main.py`
- [`uploader.py`](src/uploader.py) handles uploading the files in separate threads (the multithreading logic is very sus, sorry)
- [`settings.py`](src/settings.py) handles saving and loading the `settings.ini` file
- [`errorWindow.py`](src/errorWindow.py) handles creating an external error window.
- [`file_progress.py`](src/errorWindow.py) reports the progress of the currently uploading file to the ui via callback

## Built With
- Python
- PySimpleGUI
- boto3
- [Love](https://www.merriam-webster.com/dictionary/love)

## Versioning
This tool uses [Semantic Versioning](http://semver.org/) for versioning. For the versions
available, see the [tags on this repository](https://github.com/aashishvasu/S3-folder-uploader/tags).

## Contributors
  - [**Aashish Vasudevan**](https://github.com/aashishvasu) - *Repo owner*

## License

This project is licensed under the [LGPL-2.1](LICENSE.md) license - see the [LICENSE.md](LICENSE.md) file for details.
