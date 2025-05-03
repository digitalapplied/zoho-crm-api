import datetime

def log_action(message):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open('process_log.txt', 'a') as log_file:
        log_file.write(f"[{timestamp}] {message}\n") 