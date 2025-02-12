import time
import schedule
from db import init_db

def main():
    init_db()
    
    # placeholder schedule
    schedule.every().day.do(print, "warehouse on hold")
    
    while True:
        schedule.run_pending()
        time.sleep(1)  # Sleep to prevent CPU overuse

main()