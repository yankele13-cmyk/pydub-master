# import warnings
# warnings.filterwarnings('ignore')

import os
import io
import time
import traceback
import sys
import TTS_chatterbox
import urllib
from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO
import socket as sct
import webview as pywebview
from tkinter import filedialog
import threading
import contextlib
import logging

def resource_path(relative_path): return os.path.join(os.path.abspath('.'), relative_path)

# Flask app setup
app = Flask(__name__, template_folder=resource_path('templates'), static_folder=resource_path('static'))
socketio = SocketIO(app, async_mode='threading')


class API:
    def choose_file(self, file_type): return filedialog.askopenfilename(filetypes=file_type)
    def choose_folder(self): return filedialog.askdirectory()
    def capture_print_output(func):
        def wrapper(*args, **kwargs):
            emit_stream = EmitStream(socketio, 'TTS_output')
            sys.stdout = emit_stream
            with contextlib.redirect_stdout(emit_stream), contextlib.redirect_stderr(emit_stream):
                result = func(*args, **kwargs)
            sys.stdout = sys.__stdout__
            return result
        return wrapper
    @capture_print_output
    def run_tts(self, paths):
        try:
            # Get the form data
            csv_path = paths['csvFile']
            audio_path = paths['audioFile']
            output_folder = paths['outputFolder']
            TTS_chatterbox.main(csv_path, audio_path, output_folder)
            return "Audio files generated successfully!"
        except Exception as e:
            return "An error occured when generating: " + str(e)


class EmitStream(io.StringIO):
    def __init__(self, socket, event):
        super().__init__()
        self.socket = socket
        self.event = event
    def write(self, message):
        if message.strip(): socketio.emit(self.event, {'output': message})


class SocketIOHandler(logging.Handler):
    def emit(self, record):
        socketio.emit('TTS_output', {'output': self.format(record)})


def progress_bar(block_num, block_size, total_size):
    if total_size > 0: socketio.emit('progress', {'downloaded': block_num * block_size * 100 / total_size, 'total': total_size})

@app.errorhandler(500)
def internal_error(e):
    print("----- Flask Internal Error -----")
    traceback.print_exc()
    print("-------------------------------")
    return f"<pre>{traceback.format_exc()}</pre>", 500

@app.route('/')
def index():
    print('rendering')
    return render_template('index.html')

# Function to check if the Dicta model exists
@app.route('/check_model')
def check_model():
    if os.path.exists(resource_path('dicta-1.0.onnx')):
        return jsonify({"modelExists": True})
    else:
        return jsonify({"modelExists": False})

# Function to install the model
@app.route('/install_model', methods=['POST'])
def install_model():
    url = "https://github.com/thewh1teagle/dicta-onnx/releases/download/model-files-v1.0/dicta-1.0.onnx"
    filename = "dicta-1.0.onnx"
    
    try:
        res = urllib.request.urlopen(url)
        total_size = int(res.getheader('Content-Length'))
        res.close()

        print(f"Downloading {filename}...")
        urllib.request.urlretrieve(url, resource_path(filename), reporthook=progress_bar)
        socketio.emit('progress', {'downloaded': 100, 'total': total_size}) # final update
        print("Download complete!")
        return jsonify(success=True)
    except Exception as e:
        socketio.emit('progress', {'downloaded': 0, 'total': 0})  # In case of failure
        return jsonify(success=False, error=str(e))

# Flask app routing
def run_flask_app():
    socketio.run(app=app, debug=True, port=5001, use_reloader=False)

def wait_for_port(port, host="127.0.0.1", timeout=30):
    start = time.time()
    while time.time() - start < timeout:
        try:
            with sct.create_connection((host, port), timeout=1):
                return True
        except OSError:
            time.sleep(0.2)
    return False


if __name__ == '__main__':
    # Run Flask app in a background thread, passing the event
    threading.Thread(target=run_flask_app, daemon=True).start()

    # Wait for Flask to be ready
    if not wait_for_port(5001):
        print("Flask startup timed out!")
        sys.exit(1)

    # Start PyWebView with the Flask app
    api = API()
    pywebview.create_window('Hebrew TTS Installer & Converter', 'http://127.0.0.1:5001', js_api=api)
    pywebview.start()
