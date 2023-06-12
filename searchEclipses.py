from main import *

# Get all eclipses from "time" to "end"
time = get_date(2001,1,1)
end = get_date(2100,12,31)
ref = datetime(1899,12,30)

# Eclipse candidates
candidates = []

# A specific time is an eclipse candidate if the angular distance of the Moon and the Sun is less than 1.8° in GSE coordinates
# This is a sufficiently high bound to never miss an eclipse, but can give false-positives
first = True
while time < end:
    if not first:
        previouslat, previouslon = lat, lon
        first = False
    lat, lon, dis = moon_gse(time)
    lon = lon - 360 * round(lon / 360)
    distance = np.sqrt(lat*lat + lon*lon)
    # If the distance is only increasing, can skip to the next month
    if not first and distance > np.sqrt(previouslat*previouslat + previouslon*previouslon):
        time += 29
    if distance < 1.8:
        candidates.append(time)
        # If candidate found, can skip to the next month
        time += 29
        continue
    # Search 1 hour at a time
    time += 1/24

obs_memo = {}
t0 = 36605.3161689815
lon0 = np.deg2rad(68.05)

# Pre-calculate the position of 100 observers world-wide
for lon in range(-180,180,10):
    lon = np.deg2rad(lon)
    for lat in range(-90,90,10):
        lat = np.deg2rad(lat)
        pos0 = np.array([np.cos(lat) * np.cos(lon - lon0),
                         np.cos(lat) * np.sin(lon - lon0),
                         np.sin(lat)]) * earth_radius
        obs_memo[(lat,lon)] = pos0

# Loops through each eclipse candidate to see if any observer sees an eclipse in a span of +- 1 day from the candidate time
# if so, it will print the time. Note the eclipse actual start time will be within 1 hour before the time print.
counter = 0
for time in candidates:
    time -= 1
    for i in range(48):
        day_angle = 2 * np.pi / 0.9972695662744252 * (time - t0)
        day_rotation = np.array([[np.cos(day_angle), -np.sin(day_angle), 0],
                                 [np.sin(day_angle), np.cos(day_angle), 0],
                                 [0, 0, 1]])
        obl = np.deg2rad(obliquity(time))
        equinox_rotation = np.array([[1, 0, 0],
                                     [0, np.cos(obl), np.sin(obl)],
                                     [0, -np.sin(obl), np.cos(obl)]])
        ta = true_anomaly(time) - true_anomaly(t0)

        orbit_rotation = np.array([[np.cos(ta), np.sin(ta), 0],
                                   [-np.sin(ta), np.cos(ta), 0],
                                   [0, 0, 1]])

        rot_matrix = orbit_rotation @ equinox_rotation @ day_rotation
        sun = sun_position(time)
        moon = moon_position(time)

        # Loop through each observer
        for pos0 in obs_memo.values():
            observer = rot_matrix @ pos0
            if observer.dot(sun) >= 0 and overlap(observer,sun,moon,sun_radius,moon_radius) > 0:
                counter += 1
                print(counter,ref+timedelta(days=time))
                break
        else:
            time += 1 / 24
            continue
        break


