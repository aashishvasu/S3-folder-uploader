import os
import PySimpleGUI as sg
import src.uploader as uploader
import src.errorWindow as error

# Vars
folder:str = ''
path:str = ''
totalfiles:int = 0
threads:dict = {}

# Theme
sg.theme('BrownBlue')

# Layouts
LocalPathError = [	[sg.Text(size=(10, 1)), sg.Text('Invalid Local Path', text_color='red')]	]

col1Layout =	[
					[sg.Text('Local Path', size=(10, 1)), sg.InputText(size=(30, 1), enable_events=True ,key='-LOCAL-'), sg.FolderBrowse()],
					[sg.Column(LocalPathError, key='-PATHERROR-', visible=False)],
					[sg.Text('Server Path', size=(10, 1)), sg.InputText(size=(30, 1), enable_events=True ,key='-SERVER-')],
					[sg.Button('Start'), sg.Button('S3 Settings'), sg.Push(), sg.Button('Quit')]
				]
col2Layout =	[
					[sg.ProgressBar(size=(30,10), max_value=1, orientation='h', key='-FILEPROGRESSBAR-')],
					[sg.ProgressBar(size=(30,10), max_value=1, orientation='h', key='-TOTALPROGRESSBAR-')],
					[sg.Text('Total Files: ', key='-TOTALFILES-'), sg.Push(), sg.Text('', key='-FILENAME-')],
					[sg.Button('Upload'), sg.Push(), sg.Text('Upload Done!', text_color='aquamarine2', key='-DONETEXT-', visible=False)]
				]
mainLayout =	[
					[sg.Column(col1Layout), sg.Column(col2Layout, key='-UPLOADPANEL-', visible=False)]
				]

# Create the Window
window = sg.Window('Object Storage Uploader', mainLayout)

def progress_update(number:int):
	window.write_event_value('progress-bar', number)
	window['-TOTALFILES-'].update(value='Files: {}'.format(totalfiles-number))

	if number == totalfiles:
		window['-DONETEXT-'].update(visible=True)
		window['-FILENAME-'].update(visible=False)
		window['-SERVER-'].update(disabled=False)
		window['-LOCAL-'].update(disabled=False)
		window['Start'].update(disabled=False)
		window['S3 Settings'].update(disabled=False)

def file_progress_update(current:int, filename:str):
	window['-FILENAME-'].update(value=filename, visible=True)
	window.write_event_value('file-progress-bar', current)

# Event Loop to process "events" and get the "values" of the inputs
while True:
	event, values = window.read()
	if event == sg.WIN_CLOSED or event == 'Quit': # if user closes window or clicks cancel
		break

	# Folder path updated
	if event == '-LOCAL-':
		folder = values['-LOCAL-']
		try:
			window['-SERVER-'].update(os.path.basename(folder))
			path=os.path.basename(folder)
		except:
			window['-SERVER-'].update('Path Invalid')

	# Server path updated
	if event == "-SERVER-":
		path = values["-SERVER-"]

	# Progress bar updated
	if event == "progress-bar":
		window['-TOTALPROGRESSBAR-'].update(values[event])
	
	# File progress bar updated
	if event == "file-progress-bar":
		window['-FILEPROGRESSBAR-'].update(values[event])

	# Open and initialize the upload panel
	if event == 'Start':
		if path == '':
			error.open_error_window('No server path specified.')
		if folder == '':
			error.open_error_window('No folder path specified.')
		else:
			uploader.file_test(folder, path)
			window['-UPLOADPANEL-'].update(visible=True)
			window['-DONETEXT-'].update(visible=False)
			window['-FILENAME-'].update(visible=False)
			window['Upload'].update(disabled=False)
			window['-SERVER-'].update(disabled=True)
			window['-LOCAL-'].update(disabled=True)
			input = window['-TOTALFILES-']
			input.update(value='Files: {}'.format(len(uploader._filepaths)))
			totalfiles = len(uploader._filepaths)
			input = window['-FILEPROGRESSBAR-']
			input.update(current_count=0, max=100)
			input = window['-TOTALPROGRESSBAR-']
			input.update(current_count=0, max=len(uploader._filepaths))

	# Open the settings file
	if event == 'Settings':
		os.startfile('settings.ini')

	if event == 'Upload':
		input = window['-TOTALPROGRESSBAR-']
		input.update(current_count=0, max=len(uploader._filepaths))
		uploader.upload_files(file_progress_update, progress_update)
		window['Upload'].update(disabled=True)
		window['Start'].update(disabled=True)
		window['S3 Settings'].update(disabled=True)

	if not os.path.exists(folder):
		window['-PATHERROR-'].update(visible=True)
	else:
		window['-PATHERROR-'].update(visible=False)

window.close()