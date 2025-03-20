from flask import Flask, Response, render_template
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def generate_output():
    """Runs main.py and streams all output (including from imported scripts) to frontend."""
    process = subprocess.Popen(
        ['python','-u','main.py'], 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE, 
        text=True,
        bufsize=1
    )

    # Read and stream stdout and stderr
    for line in iter(process.stdout.readline, ''):
        yield f"data: {line.strip()}\n\n"

    for line in iter(process.stderr.readline, ''):
        yield f"data: {line.strip()}\n\n"

@app.route('/output')
def stream_output():
    return Response(generate_output(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
