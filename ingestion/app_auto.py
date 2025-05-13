import psycopg2   # pip install psycopg2
import csv
import os
from watchdog.observers import Observer  # pip install watchdog
from watchdog.events import FileSystemEventHandler

# Database connection parameters
DB_HOST = 'localhost'
DB_NAME = 'Db name'
DB_USER = 'postgres'
DB_PASSWORD = 'your password'
DB_PORT = '5432'
CSV_FILE_PATH = 'data.csv'

# Function to connect to PostgreSQL
def connect_to_db():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )

# Function to check if the row already exists
def is_row_exists(cur, row_id):
    cur.execute("SELECT 1 FROM staff WHERE id = %s", (row_id,))
    return cur.fetchone() is not None

# Main function to ingest data
def ingest_data():
    # Connect to PostgreSQL
    conn = connect_to_db()
    cur = conn.cursor()

    # Open the CSV file
    with open(CSV_FILE_PATH, 'r') as file:
        data_reader = csv.reader(file)
        next(data_reader)  # Skip the header row

        # Insert each row into the table, if it doesn't exist
        for row in data_reader:
            if not is_row_exists(cur, row[0]):  # Check if row already exists by id
                cur.execute("INSERT INTO staff (id, name, age) VALUES (%s, %s, %s)", row)
            else:
                print(f"Skipping duplicate row with id: {row[0]}")

    # Commit and close the connection
    conn.commit()
    cur.close()
    conn.close()
    print("Data ingestion complete")

# Watchdog event handler to monitor file changes
class CSVFileEventHandler(FileSystemEventHandler):
    def on_modified(self, event):                           #  on_created, on_deleted , on_moved
        if event.src_path.endswith(CSV_FILE_PATH):    # checks whether the modified file is the same as the file you are interested in (the CSV file).if there is other file which modfied shouldnt be cosnsidered
            print(f"{CSV_FILE_PATH} has been modified. Ingesting new data...")
            ingest_data()  # Trigger the data ingestion process when the file changes

# Set up the file observer
def watch_file():    #sets up the file monitoring system using the watchdog library
    event_handler = CSVFileEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(os.path.abspath(CSV_FILE_PATH)), recursive=False)
    observer.start()
    print(f"Monitoring {CSV_FILE_PATH} for changes...")
    try:
        while True:
            pass  # Keep the script running to monitor the file
    except KeyboardInterrupt:            
        observer.stop()
    observer.join()  # ensures that the observer keeps running

if __name__ == "__main__":
    watch_file() # To make sure watch_file monitoring will be run only when it is directly triggered 
