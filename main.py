from fastapi import FastAPI

app = FastAPI()

@app.get("/enter_coordinates/")
def get_coordinates(x_axis: int, y_axis: int):
    if not (-10 <= x_axis <= 10) or not (-10 <= y_axis <= 10):
        raise HTTPException(status_code=400, detail="Coordinates must be between -10 and 10")
    # This is a change
    return {"x_axis": x_axis, "y_axis": y_axis}
