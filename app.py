import time
from flask import Flask, render_template, Response, request, jsonify
import subprocess
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import threading

app = Flask(__name__)

scheduler = BackgroundScheduler()
scheduler.start()

# Store the process reference
current_process = None
process_lock = threading.Lock()

def run_script():
    """Runs main.py once and stops."""
    global current_process
    with process_lock:
        if current_process and current_process.poll() is None:
            return  # Script is already running, do not start another

        current_process = subprocess.Popen(
            ['python', '-u', 'main.py'], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            text=True,
            bufsize=1
        )

@app.route('/')
def index():
    return render_template('index.html')

def generate_output():
    """Streams logs only when main.py is running."""
    global current_process
    with process_lock:
        if not current_process or current_process.poll() is not None:
            yield "data: No active script execution. Waiting for schedule...\n\n"
            time.sleep(60)
            return

    for line in iter(current_process.stdout.readline, ''):
        yield f"data: {line.strip()}\n\n"

@app.route('/output')
def stream_output():
    return Response(generate_output(), mimetype='text/event-stream')

@app.route('/schedule', methods=['POST'])
def schedule_script():
    """Handles scheduling based on user input."""
    schedule_type = request.json.get("type")
    schedule_time = request.json.get("time")
    interval = request.json.get("interval")

    if schedule_type == "run_now":
        run_script()
        return jsonify({"message": "Script started immediately."})

    elif schedule_type == "time":
        job_id = "scheduled_time"
        scheduler.remove_job(job_id) if scheduler.get_job(job_id) else None
        run_time = datetime.strptime(schedule_time, "%H:%M").time()
        scheduler.add_job(run_script, "cron", hour=run_time.hour, minute=run_time.minute, id=job_id)
        return jsonify({"message": f"Scheduled at {schedule_time}."})

    elif schedule_type == "interval":
        # Ensure the interval is at least 30 minutes
        if not interval or int(interval) < 30:
            return jsonify({"error": "Minimum interval must be 30 minutes."}), 400

        job_id = "scheduled_interval"
        scheduler.remove_job(job_id) if scheduler.get_job(job_id) else None
        scheduler.add_job(run_script, "interval", minutes=int(interval), id=job_id)
        return jsonify({"message": f"Running every {interval} minutes."})

    return jsonify({"message": "Invalid schedule type."})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
