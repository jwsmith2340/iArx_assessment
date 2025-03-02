import psycopg2
from fastapi import FastAPI, HTTPException

from common.utils import db_config

app = FastAPI()


@app.get("/enter_coordinates/")
def get_coordinates(x_axis: int, y_axis: int):
    if not (-10 <= x_axis <= 10) or not (-10 <= y_axis <= 10):
        raise HTTPException(
            status_code=400, detail="Coordinates must be between -10 and 10"
        )

    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        # SQL query to calculate Manhattan distance and get 3 closest stations
        cursor.execute(
            """
            SELECT id, med_a, med_b, med_c,
                   ABS(x_axis - %s) + ABS(y_axis - %s) AS manhattan_distance
            FROM fill_stations
            ORDER BY manhattan_distance
            LIMIT 3;
            """,
            (x_axis, y_axis),
        )

        result = cursor.fetchall()
        cursor.close()
        conn.close()

        if result:
            # Prepare the response with only facility IDs, cheapest medication, and its name
            return [
                {
                    "central_fill": row[0],
                    "cheapest_medication": {
                        "med_name": "Medication A"
                        if row[1] == min(row[1], row[2], row[3])
                        else "Medication B"
                        if row[2] == min(row[1], row[2], row[3])
                        else "Medication C",
                        "med_price": min(row[1], row[2], row[3]),
                    },
                    "manhattan_distance": row[4],
                }
                for row in result
            ]
        else:
            raise HTTPException(status_code=404, detail="No fill stations found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
