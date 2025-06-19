from flask import Flask, render_template, request, redirect, url_for
import json, os

app = Flask(__name__)
DATA_FILE = "data/locations.json"
PASSWORDS = {"Ben": "Tottenham1", "John": "Fortunte2", "Jude": "Ray3", "Laoch": "Kennedy4", "Peter": "Richardson5"}

def load_locations():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as f:
            json.dump({}, f)
    with open(DATA_FILE) as f:
        return json.load(f)

def save_locations(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

@app.route("/")
def index():
    people = [
        {"id": "Ben", "image": "Ben.png"},
        {"id": "John", "image": "John.png"},
        {"id": "Jude", "image": "Jude.png"},
        {"id": "Laoch", "image": "Laoch.png"},
        {"id": "Peter", "image": "Peter.png"},
        {"id": "All", "image": "all.png"},
    ]
    return render_template("index.html", people=people)

# @app.route("/<person>")
# def person_page(person):
#     locations = load_locations()
#     loc = locations.get(person, {"lat": 0, "lng": 0})
#     return render_template("person.html", person=person, lat=loc["lat"], lng=loc["lng"])

@app.route("/<person>")
def person_page(person):
    locations = load_locations()

    if person == "All":
        people = [
            {"id": "Ben", "image": "Ben.png"},
            {"id": "John", "image": "John.png"},
            {"id": "Jude", "image": "Jude.png"},
            {"id": "Laoch", "image": "Laoch.png"},
            {"id": "Peter", "image": "Peter.png"},
        ]
        # Only include people with known locations
        locs = []
        for p in people:
            loc = locations.get(p["id"])
            if loc:
                locs.append({
                    "id": p["id"],
                    "image": p["image"],
                    "lat": loc["lat"],
                    "lng": loc["lng"]
                })
        return render_template("all.html", people=locs)
    else:
        loc = locations.get(person, {"lat": 0, "lng": 0})
        return render_template("person.html", person=person, lat=loc["lat"], lng=loc["lng"])



@app.route("/update/<person>", methods=["POST"])
def update_location(person):
    password = request.form["password"]
    if password != PASSWORDS.get(person):
        return "Incorrect password", 403

    lat = request.form["lat"]
    lng = request.form["lng"]

    locations = load_locations()
    locations[person] = {"lat": float(lat), "lng": float(lng)}
    save_locations(locations)

    return redirect(url_for('person_page', person=person))

if __name__ == "__main__":
    app.run(debug=True)
