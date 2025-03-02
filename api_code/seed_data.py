import psycopg2
import random
import time

from common.utils import db_config


def wait_for_db() -> None:
    """A function that ensure connectivity to the DB

        Args:
            None
        
        Returns:
            None

    """
    retries = 3

    for i in range(retries):
        try:
            conn = psycopg2.connect(**db_config)
            conn.close()
            print("Database is ready!")
            return

        except psycopg2.OperationalError:
            print(f"Database not ready, retrying ({i+1}/{retries})...")
            time.sleep(5)

    raise Exception(f"Database connection failed after {retries} retries.")


def seed_data() -> None:
    """The function that generates random seed data and inserts it into the DB
    
        Args:
            None

        Returns:
            None

    """
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS fill_stations (
        id SERIAL PRIMARY KEY,
        x_axis INTEGER NOT NULL,
        y_axis INTEGER NOT NULL,
        med_a NUMERIC(6,2) NOT NULL,
        med_b NUMERIC(6,2) NOT NULL,
        med_c NUMERIC(6,2) NOT NULL
    );
    """
    )

    num_records = random.randint(6, 15)
    seed_records = gen_seeds(num_records)

    cursor.executemany(
        """
    INSERT INTO fill_stations (x_axis, y_axis, med_a, med_b, med_c)
    VALUES (%s, %s, %s, %s, %s);
    """,
        seed_records,
    )

    conn.commit()
    cursor.close()
    conn.close()
    print(f"Seeded {num_records} records into fill_stations.")

def gen_seeds(num_records: int) -> list[tuple[int | float]]:
    """A function to create a list of tuples with seed values

        Args:
            num_records (int): Random int controlling how many seeds to create

        Returns:
            list: List of tuples with x, y, and Med A/B/C seed values    
    
    """
    generated_coords = set()
    seed_records = []

    while len(seed_records) < num_records:
        x = random.randint(-10, 10)
        y = random.randint(-10, 10)

        if (x, y) not in generated_coords:
            generated_coords.add((x, y))
            seed_records.append(
                (
                    x,
                    y,
                    round(random.uniform(1.00, 100.00), 2),
                    round(random.uniform(1.00, 100.00), 2),
                    round(random.uniform(1.00, 100.00), 2),
                )
            )

    return seed_records

if __name__ == "__main__":
    wait_for_db()
    seed_data()
