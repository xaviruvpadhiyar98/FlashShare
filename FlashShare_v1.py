from pyperclip import paste,copy
from flask import Flask, request, send_file 
from shutil import make_archive
from glob import glob
from os import system

from socket import socket, SOCK_DGRAM, AF_INET

s = socket(AF_INET, SOCK_DGRAM)
s.connect(('8.8.8.8', 1))
print(f"\nYour Server IP is   http://{s.getsockname()[0]}/\n")

app = Flask(__name__)

@app.route("/",methods=["GET"])
def CheckServer():
	return "True"

@app.route("/text",methods=["POST","GET"])
def CopyPaste():
	if request.method == 'POST':
		for x,y in request.form.items():
			print(y)
			clipboardText = copy(y)
			if "https://youtu" in y:
				system(f"cvlc {y} &")
			if "http" in y and "https://youtu" not in y:
				system(f"chromium-browser {y}")
		return "Done"
	if request.method == 'GET':
		clipboardText = paste()
		return clipboardText
		
		
@app.route("/file",methods=["POST","GET"])
def CopyPaste11():
	if request.method == 'POST':
		folder = "Complete/DownloadedFiles/"
		for x,y in request.files.items():
			y.save(folder + y.filename)
			system(f"xdg-open {folder + y.filename}")
		return "Received\n"
		
		
	if request.method == 'GET':
		folder = 'Complete/FilesTOUpload/'
		if len(glob(folder + '*')) == 0:
			print("EmptyFolder")
			return "No Files to share"
		else:
			make_archive("allFiles", 'zip', folder)
			return send_file("allFiles.zip", as_attachment=True)

			
		
		
		
if __name__ == "__main__":
	app.config['UPLOAD_FOLDER'] = 'Complete/DownloadedFiles/'
	app.run(host="0.0.0.0",debug=True,threaded=True)
