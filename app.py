
from flask import Flask, request, redirect, url_for

app = Flask(__name__)
appointments = []
next_id = 1


@app.route("/")
def home():
    rows = ""
    for a in appointments:
        rows += f"""
        <tr>
          <td>{a['id']}</td>
          <td>{a['name']}</td>
          <td>{a['date']}</td>
          <td>{a['time']}</td>
          <td><a href="/cancel/{a['id']}">Cancel</a></td>
        </tr>
        """

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
      <title>Appointment Booking System</title>
      <style>
        body {{ font-family: Arial; max-width: 800px;
                margin: 40px auto; background: #f4f7fb; }}
        h1 {{ color: #174ea6; }}
        form, table {{ background: white; padding: 20px;
                       border-radius: 8px; width: 100%; }}
        input, button {{ padding: 10px; margin: 6px 0; }}
        table {{ border-collapse: collapse; }}
        td, th {{ padding: 10px; border-bottom: 1px solid #ddd; }}
      </style>
    </head>
    <body>
      <h1>Appointment Booking System</h1>
      <form action="/book" method="post">
        <input name="name" placeholder="Your name" required>
        <input name="date" type="date" required>
        <input name="time" type="time" required>
        <button type="submit">Book Appointment</button>
      </form>
      <h2>Booked Appointments</h2>
      <table>
        <tr><th>ID</th><th>Name</th><th>Date</th>
            <th>Time</th><th>Action</th></tr>
        {rows}
      </table>
    </body>
    </html>
    """


@app.route("/book", methods=["POST"])
def book():
    global next_id

    appointments.append({
        "id": next_id,
        "name": request.form["name"],
        "date": request.form["date"],
        "time": request.form["time"]
    })
    next_id += 1

    return redirect(url_for("home"))


@app.route("/cancel/<int:appointment_id>")
def cancel(appointment_id):
    appointments[:] = [
        a for a in appointments if a["id"] != appointment_id
    ]
    return redirect(url_for("home"))


@app.route("/health")
def health():
    return {"status": "healthy"}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
