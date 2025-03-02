import psycopg2
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

from common.utils import db_config

app = FastAPI()

class CheapestMedication(BaseModel):
    med_name: str
    med_price: float

class FillStationResponse(BaseModel):
    central_fill: int
    cheapest_medication: CheapestMedication
    manhattan_distance: int

@app.get("/health")
def health_check():
    """Compose health check route"""
    return {"status": "healthy"}

@app.get("/enter_coordinates/", response_model=List[FillStationResponse])
def get_coordinates(x_axis: int, y_axis: int) -> List[FillStationResponse]:
    """GET Route to return information about the three nearest fill stations.

    Args:
        x_axis (int): x axis coordinate within [-10, 10]
        y_axis (int): y axis coordinate within [-10, 10]

    Returns:
        List[FillStationResponse]: List of details for the three nearest fill stations.
    """
    if not (-10 <= x_axis <= 10) or not (-10 <= y_axis <= 10):
        raise HTTPException(
            status_code=400, detail="Coordinates must be between -10 and 10"
        )

    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

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
            return [
                FillStationResponse(
                    central_fill=row[0],
                    cheapest_medication=CheapestMedication(
                        med_name=(
                            "Medication A"
                            if row[1] == min(row[1], row[2], row[3])
                            else "Medication B"
                            if row[2] == min(row[1], row[2], row[3])
                            else "Medication C"
                        ),
                        med_price=min(row[1], row[2], row[3]),
                    ),
                    manhattan_distance=row[4],
                )
                for row in result
            ]
        else:
            raise HTTPException(status_code=404, detail="No fill stations found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
