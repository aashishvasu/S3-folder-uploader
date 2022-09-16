import os
from time import sleep, strftime
from unittest import result
import boto3
import datetime
import json
import src.settings as settings
from src.file_progress import ProgressPercentage

# MT
from concurrent.futures import ThreadPoolExecutor
import threading
MAXTHREADS:int = 8
threads:dict = {}

# Vars
_localdirpath:str=''
_serverdirpath:str=''
_filepaths:list = []
_filescomplete:int = 0
_jsonfile = {}
_filesize:int = 0
_currentfilesize:int = 0

# Create boto3 client
session = boto3.session.Session()
client:boto3.Session

def init_session():
	# Empty the list of files for a new job
	_filepaths.clear()
	global _filescomplete
	_filescomplete = 0

	global client
	client = session.client('s3', region_name=settings.bucket_region, endpoint_url=settings.endpoint, aws_access_key_id=settings.api_key, aws_secret_access_key=settings.api_secret)

def file_test(localDirPath:str, serverDirPath:str):
	# Initialize boto session
	init_session()

	# Add all files in path to a list which will then be updated
	for root, dirs, files in os.walk(localDirPath):
		for file in files:
			_filepaths.append(os.path.join(root, file))

	global _localdirpath, _serverdirpath
	_localdirpath = localDirPath
	_serverdirpath = serverDirPath

def upload_files(filecallback, totalcallback):
	global threads
	if len(threads) == 0 and len(_filepaths) != 0:
		for x in range(MAXTHREADS):
			# This second check is if there are less filepaths than MAXTHREADS
			if len(_filepaths) != 0:
				filepath = _filepaths.pop()
				t = threading.Thread(target=thread_upload, args=(filepath, _localdirpath, _serverdirpath, filecallback, totalcallback))
				threads[filepath] = t
				t.start()
		
	elif len(_filepaths) == 0 and len(threads) == 0:
		# Dump generated output to json if there are no more threads to process and all files have been processed
		json_dump()

def thread_upload(filepath:str, localpath:str, serverpath:str, filecallback,  totalcallback):
	internal_filepath = filepath
	server_key = filepath.replace(localpath, serverpath).replace("\\", "/")

	global _filesize, _currentfilesize
	_filesize = os.stat(internal_filepath).st_size			
	_currentfilesize = 0
	# Upload the file
	with open(filepath, "rb") as file:
		client.upload_fileobj(file, settings.bucket_name, server_key, Callback=ProgressPercentage(internal_filepath, filecallback))

	# Add progress to json file
	global _jsonfile
	_jsonfile[server_key] = { 'upload-time': str(datetime.datetime.now()), 'local-path': internal_filepath }

	single_upload_complete(filepath, totalcallback)

	# Check if more files need to be processed
	upload_files(filecallback, totalcallback)

def file_progress_update(size):
	global _currentfilesize, _filesize, _FileProgressFunc
	if _filesize == 0:
		return
	_currentfilesize += size
	_FileProgressFunc(_currentfilesize, _filesize)

	print("{} %".format(int(_currentfilesize / _filesize * 100)))

def single_upload_complete(filepath:str, callback):	
	global _filescomplete
	_filescomplete += 1

	t = threads.pop(filepath)

	# Callback with progress
	callback(_filescomplete)

def json_dump():
	filename = datetime.datetime.now().strftime("%Y-%m-%d_%H.%M.%S") +".json"
	
	global _jsonfile
	# Save json file
	with open(filename, 'w') as f:
		json.dump(_jsonfile, f, indent=4)

	print('JSON saved as {}'.format(filename))
