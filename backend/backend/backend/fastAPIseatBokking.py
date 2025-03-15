from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import pymysql

app = FastAPI()

# Database Connection
def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="yourpassword",
        database="smart_bus_db",
        cursorclass=pymysql.cursors.DictCursor
    )

# Model for Seat Booking
class SeatBooking(BaseModel):
    bus_id: int
    seat_number: str
    passenger_id: int

# Fetch available seats for a bus
@app.get("/available-seats/{bus_id}")
def get_available_seats(bus_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT seat_number FROM bus_seats WHERE bus_id = %s AND status = 'available'", (bus_id,))
    seats = cursor.fetchall()
    cursor.close()
    conn.close()
    
    if not seats:
        raise HTTPException(status_code=404, detail="No available seats")
    return {"available_seats": [seat["seat_number"] for seat in seats]}

# Book a seat
@app.post("/book-seat/")
def book_seat(booking: SeatBooking):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if the seat is available
    cursor.execute("SELECT status FROM bus_seats WHERE bus_id = %s AND seat_number = %s", 
                   (booking.bus_id, booking.seat_number))
    seat = cursor.fetchone()

    if not seat or seat["status"] == "booked":
        raise HTTPException(status_code=400, detail="Seat is already booked")
# Book the seat
    cursor.execute(
        "UPDATE bus_seats SET status = 'booked', passenger_id = %s WHERE bus_id = %s AND seat_number = %s",
        (booking.passenger_id, booking.bus_id, booking.seat_number)
    )
    conn.commit()
    cursor.close()
    conn.close()

    return {"message": f"Seat {booking.seat_number} booked successfully"}