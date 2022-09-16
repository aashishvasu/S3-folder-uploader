import PySimpleGUI as sg

def open_error_window(text:str):
	layout = [	[sg.Text(text, text_color='red')],
				[sg.Button('Ok')]	]
	window = sg.Window("ERROR", layout, modal=True, element_justification='c')
	while True:
		event, values = window.read()
		if event == sg.WIN_CLOSED or event == 'Ok': # if user closes window or clicks cancel
			break

	window.close()