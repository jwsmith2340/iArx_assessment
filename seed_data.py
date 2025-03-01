import psycopg2
import random
import time

DB_CONFIG = {
    "dbname": "data",
    "user": "admin",
    "password": "admin",
    "host": "postgres",
    "port": "5432",
}

# Retry logic to wait for PostgreSQL to be ready
def wait_for_db():
    retries = 3
    for i in range(retries):
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            conn.close()
            print("Database is ready!")
            return
        except psycopg2.OperationalError:
            print(f"Database not ready, retrying ({i+1}/{retries})...")
            time.sleep(5)
    raise Exception("Database connection failed after retries.")

# Seed data function
def seed_data():
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # Ensure table exists
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS fill_stations (
        id SERIAL PRIMARY KEY,
        x_axis INTEGER NOT NULL,
        y_axis INTEGER NOT NULL,
        med_a NUMERIC(6,2) NOT NULL,
        med_b NUMERIC(6,2) NOT NULL,
        med_c NUMERIC(6,2) NOT NULL
    );
    """)

    num_records = random.randint(6, 15)
    generated_coords = set()
    seed_records = []

    while len(seed_records) < num_records:
        x = random.randint(-10, 10)
        y = random.randint(-10, 10)

        if (x, y) not in generated_coords:
            generated_coords.add((x, y))
            seed_records.append((
                x, y,
                round(random.uniform(1.00, 100.00), 2),
                round(random.uniform(1.00, 100.00), 2),
                round(random.uniform(1.00, 100.00), 2)
            ))

    # Insert generated seed data
    cursor.executemany("""
    INSERT INTO fill_stations (x_axis, y_axis, med_a, med_b, med_c)
    VALUES (%s, %s, %s, %s, %s);
    """, seed_records)

    conn.commit()
    cursor.close()
    conn.close()
    print(f"Seeded {num_records} records into fill_stations.")

if __name__ == "__main__":
    wait_for_db()
    seed_data()
