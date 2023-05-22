import redis
from flask import Flask, render_template, request, redirect, json

app = Flask(__name__)
r = redis.Redis()


@app.route('/')
def home():
    return render_template("map.html")


@app.route('/add-marker', methods=['POST'])
def add_marker():
    req = request.form
    location = req['lname']
    latitude = req['latitude']
    longitude = req['longitude']

    print(location, latitude, longitude)

    r.geoadd("points", [longitude, latitude, location])
    r.set("last_loc_name", location)
    return redirect('/')


@app.route('/data')
def data():
    loc_name = r.get('last_loc_name')

    if loc_name is None:
        r.geoadd('points', ['-104.985784', '39.728206', 'parking'])
        loc_name = 'parking'

    all_location = r.georadiusbymember(name='points', member=loc_name, radius=4000, withcoord=True)

    coord = dict()

    for loc in all_location:
        name = loc[0].decode("utf-8")
        longitude = loc[1][0]
        latitude = loc[1][1]

        coord[name] = {'lat': latitude, 'lng': longitude}

    return json.dumps(coord)


@app.route("/last")
def last_loc():
    return r.get('las_loc_name').decode('utf-8')


if __name__ == '__main__':
    app.run()
