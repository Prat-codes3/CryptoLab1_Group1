from datetime import datetime

LOG_FILE = "logs/execution.log"

def log_action(action):
    with open(LOG_FILE, "a") as file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"{timestamp} - {action}\n")