from main import *
from PIL import Image

worldmap = Image.open("Equirectangular_projection_SW.jpg")
width, height = worldmap.size

# Initial time
time = 402060.6250000000

for i in range(70):
    frame = worldmap.copy()
    pixels = frame.load()

    t0 = 36605.3161689815
    lon0 = np.deg2rad(68.05)

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
    memo = {}
    for x in range(width):
        for y in range(height):
            lon, lat = np.deg2rad(round(((x + 0.5) / width - 0.5) * 360)), np.deg2rad(round(-((y + 0.5) / height - 0.5) * 180))
            if (lat,lon) in memo:
                ocultation,visible = memo[(lat,lon)]
            else:
                pos0 = np.array([np.cos(lat) * np.cos(lon - lon0),
                                 np.cos(lat) * np.sin(lon - lon0),
                                 np.sin(lat)]) * earth_radius
                observer = rot_matrix @ pos0
                ocultation = 1-overlap(observer,sun,moon,sun_radius,moon_radius)
                memo[(lat,lon)] = (ocultation, alt(sun,observer) >= 0)
            if ocultation < 1 and visible:
                original = pixels[x,y]
                pixels[x,y] = (round(ocultation*original[0]),round(ocultation*original[1]),round(ocultation*original[2]))
    frame.save(f"eclipse/solar{i}.jpg")
    time += 5/1440
    print(i)

