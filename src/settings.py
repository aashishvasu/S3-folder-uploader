from os.path import exists
import configparser

# Vars
api_key:str			= ''
api_secret:str		= ''
bucket_name:str		= ''
bucket_region:str	= ''
bucket_url:str		= ''
endpoint:str		= ''

# Initialize config
config = configparser.ConfigParser()
config['SETTINGS'] = {}

def write_config():
	section = config['SETTINGS']

	global api_key, api_secret, bucket_name, bucket_region, bucket_url, endpoint

	section['API Key']			= api_key
	section['API Secret']		= api_secret
	section['Bucket Name']		= bucket_name
	section['Bucket Region']	= bucket_region
	section['Bucket URL']		= bucket_url
	section['Endpoint']			= endpoint

	with open('settings.ini', 'w') as configfile:
		config.write(configfile)

def read_config():
	config.read('settings.ini')

	section = config['SETTINGS']

	global api_key, api_secret, bucket_name, bucket_region, bucket_url, endpoint
	
	api_key			= section['API Key']
	api_secret		= section['API Secret']
	bucket_name		= section['Bucket Name']
	bucket_region	= section['Bucket Region']
	bucket_url		= section['Bucket URL']
	endpoint		= section['Endpoint']

# Check if settings file exists. If not, create it
if not exists('settings.ini'):
	write_config()
else:
	read_config()
	