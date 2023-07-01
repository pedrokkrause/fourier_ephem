import numpy as np
from datetime import datetime

# Load data
lon_omega = np.load("data/lon_freq", allow_pickle=True) * 2 * np.pi
lon_amp = np.load("data/lon_amp", allow_pickle=True)
lon_phases = np.load("data/lon_phases", allow_pickle=True)

lat_omega = np.load("data/lat_freq", allow_pickle=True) * 2 * np.pi
lat_amp = np.load("data/lat_amp", allow_pickle=True)
lat_phases = np.load("data/lat_phases", allow_pickle=True)

dis_omega = np.load("data/dis_freq", allow_pickle=True) * 2 * np.pi
dis_amp = np.load("data/dis_amp", allow_pickle=True)
dis_phases = np.load("data/dis_phases", allow_pickle=True)


def get_date(year,month,day,hour=0,minute=0,second=0) -> float:
    """
    Calculates the given date in the format used by the program

    :return: Date in Excel format. Days (24h) since 30/12/1899 00:00:00 UTC
    """
    date = datetime(year,month,day,hour,minute,second) - datetime(1899,12,30)
    return date.total_seconds()/86400

def moon_gse(t: float) -> tuple:
    """
    Calculates the moon latitude(°), longitude(°) and radial distance(km) in Geocentric Solar Ecliptic (GSE) coordinates

    :param t: Time in Excel format. Days (24h) since 30/12/1899 00:00:00 UTC
    :return: A tuple containing the moon's latitude, longitude, and radial distance
             in GSE coordinates in the format (latitude, longitude, distance).
    """
    lon = lon_amp.dot(np.sin(t * lon_omega + lon_phases)) + 360 / 29.530589 * t - 262827.5235067
    lat = lat_amp.dot(np.sin(t * lat_omega + lat_phases))
    dis = dis_amp.dot(np.sin(t * dis_omega + dis_phases)) + 385000.4411
    return lat, lon, dis

def sun_distance(t: float) -> float:
    """
    Calculates the sun's radial distance(km) from Earth

    :param t: Time in Excel format. Days (24h) since 30/12/1899 00:00:00 UTC
    :return: Distance (km) of the Sun from the Earth's center
    """
    dis = 149618828.7 + 2499293.007*np.sin(0.017201970017786433*t-1.62743406471495)
    return dis

def obliquity(t: float) -> float:
    """
    Calculates the obliquity of the ecliptic in degrees

    :param t: Time in Excel format. Days (24h) since 30/12/1899 00:00:00 UTC
    :return: Obliquity of the ecliptic (°)
    """
    obl = 23.45229001425579 - 0.000000356200235759373*t
    return obl

earth_radius = 6371
sun_radius = 696342
moon_radius = 1737.4

norm = lambda x: np.sqrt(x.dot(x))
norm2 = lambda x: x.dot(x)
anglew = lambda u, v: np.arccos(u.dot(v)/np.sqrt(norm2(u)*norm2(v)))

def mean_anomaly(t: float) -> float:
    """
    Calculates the mean anomaly of the Earth's orbit

    :param t: Time in Excel format. Days (24h) since 30/12/1899 00:00:00 UTC
    :return: Mean anomaly (rad) of Earth's orbit
    """
    # Earth-Moon barycenter perihelion
    t0 = 36528.9967245370
    ma = 2*np.pi/365.24218*(t-t0)
    return ma

def true_anomaly(t: float) -> float:
    """
    Calculates the true anomaly of the Earth's orbit using the equation of the center

    :param t: Time in Excel format. Days (24h) since 30/12/1899 00:00:00 UTC
    :return: True anomaly (rad) of Earth's orbit
    """
    ma = mean_anomaly(t)
    ec = 0.01671022
    ta = ma + (2*ec-1/4*ec**3 + 5/96*ec**5)*np.sin(ma) + (5/4*ec**2-11/24*ec**4)*np.sin(2*ma) + 13/12*ec**3*np.sin(3*ma)
    return ta

def observer_position(t: float,lat: float,lon: float,return_rotation=False):
    """
    Calculates the cartesian coordinates of an observer at a given latitude and longitude in the GSE coordinate system

    :param t: Time in Excel format. Days (24h) since 30/12/1899 00:00:00 UTC
    :param lat: Geographic latitude in decimal degrees, ranging from -90 (South Pole) to +90 (North Pole)
    :param lon: Geographic longitude in decimal degrees, ranging from -180 (West) to +180 (East)
    :return: If return_rotation is false, a 1-D numpy array containing the 3D coordinates (X, Y, and Z) of the observer
             in the GSE coordinate system.
             If return_rotation is true, it also returns a rotation matrix needed for certain calculations,
             such as the azimuth.
    """
    lat, lon = np.deg2rad(lat), np.deg2rad(lon)
    # March equinox
    t0 = 36605.3161689815
    lon0 = np.deg2rad(68.05)

    pos0 = np.array([np.cos(lat)*np.cos(lon-lon0),
                     np.cos(lat)*np.sin(lon-lon0),
                     np.sin(lat)])
    day_angle = 2*np.pi/0.9972695662744252*(t-t0)
    day_rotation = np.array([[np.cos(day_angle), -np.sin(day_angle),0],
                             [np.sin(day_angle), np.cos(day_angle), 0],
                             [0, 0, 1]])
    obl = np.deg2rad(obliquity(t))
    equinox_rotation = np.array([[1, 0, 0],
                                 [0, np.cos(obl), np.sin(obl)],
                                 [0, -np.sin(obl), np.cos(obl)]])
    ta = true_anomaly(t) - true_anomaly(t0)

    orbit_rotation = np.array([[np.cos(ta), np.sin(ta),0],
                             [-np.sin(ta), np.cos(ta), 0],
                             [0, 0, 1]])

    if return_rotation:
        rotation = orbit_rotation @ equinox_rotation @ day_rotation
        pos = rotation @ pos0
        return pos*earth_radius, rotation
    else:
        pos = orbit_rotation @ equinox_rotation @ day_rotation @ pos0
        return pos*earth_radius

def sun_position(t: float):
    """
    Calculates the cartesian coordinates of the Sun in the GSE coordinate system

    :param t: Time in Excel format. Days (24h) since 30/12/1899 00:00:00 UTC
    :return: A 1-D numpy array containing the 3D coordinates (X, Y, and Z) of the Sun in the GSE coordinate system.
    """
    return np.array([sun_distance(t),0,0])

def moon_position(t: float):
    """
    Calculates the cartesian coordinates of the Moon in the GSE coordinate system

    :param t: Time in Excel format. Days (24h) since 30/12/1899 00:00:00 UTC
    :return: A 1-D numpy array containing the 3D coordinates (X, Y, and Z) of the Moon in the GSE coordinate system.
    """
    lat, lon, dis = moon_gse(t)
    lat, lon = np.deg2rad(lat), np.deg2rad(lon)

    dcos_lat = dis*np.cos(lat)
    x = dcos_lat*np.cos(lon)
    y = dcos_lat*np.sin(lon)
    z = dis*np.sin(lat)

    return np.array([x,y,z])

def alt(obs,body) -> float:
    """
    Calculates the altitude of an object for a given observer in the alt/az or horizontal coordinate system

    :param obs: A 1-D Numpy array containing the GSE coordinates of the observer
    :param body: A 1-D Numpy array containing the GSE coordinates of the celestial body required altitude
    :return: The altitude angle of the body with respect to the observer in degrees.
    """
    body = body - obs
    angle = np.pi/2 - anglew(body,obs)
    return np.rad2deg(angle)

def az(obs,rotation,body) -> float:
    """
    Calculates the azimuth of an object for a given observer in the alt/az or horizontal coordinate system

    :param obs: A 1-D Numpy array containing the GSE coordinates of the observer
    :param rotation: The rotation matrix associated with the observer. Given by the observer_position function
    :param body: A 1-D Numpy array containing the GSE coordinates of the celestial body required azimuth
    :return: The azimuth angle of the body with respect to the observer in degrees.
    """
    az_vec = body - obs*(obs.dot(body)/obs.dot(obs))
    north_vec = rotation @ np.array([0,0,1])
    north_vec = north_vec*(obs.dot(obs)/north_vec.dot(obs)) - obs
    azimuth = np.rad2deg(anglew(az_vec,north_vec))
    if np.cross(north_vec,az_vec).dot(obs) < 0:
        azimuth += 180
    else:
        azimuth = 180 - azimuth
    return azimuth

def atmosphere_correction(altitude, temperature=15, pressure=1013):
    """
    The corrected altitude for an object due to the atmosphere for altitudes greater than 0.

    :param altitude: altitude of the observed body in degrees
    :param temperature: atmosphere temperature
    :param pressure: atmosphere pressure
    :return: the altitude of the body with atmospheric corrections in degrees
    """
    dT = temperature - 15
    dP = pressure - 1013

    c1 = 1.00001158 + dT*-0.0000000390 + dP*0.0000000122
    c2 = -0.01303911 + dT*0.0000436960 + dP*-0.0000129220
    c3 = 1.32591342 + dT*-0.0044503580 + dP*0.0013103002
    c4 = 2.65776455 + dT*-0.0000027020 + dP*0.0000033669

    new_altitude = c1*altitude+c2+c3/(altitude+c4)
    return new_altitude

def separation(obs,body1,body2) -> float:
    """
    The angular distance between two celestial bodies for a given observer

    :param obs: A 1-D Numpy array containing the coordinates of the observer
    :param body1: A 1-D Numpy array containing the coordinates of the first celestial body
    :param body2: A 1-D Numpy array containing the coordinates of the second celestial body
    :return: The angular distance between the two bodies in degrees
    """
    obs_body1 = body1-obs
    obs_body2 = body2-obs
    return anglew(obs_body1,obs_body2)

def angular_radius(obs,body,radius) -> float:
    """
    The angular radius or half the angular size of a celestial body for a given observer

    :param obs: A 1-D Numpy array containing the coordinates of the observer
    :param body: A 1-D Numpy array containing the coordinates of the celestial body
    :param radius: The true radius of the body
    :return: The angular radius of the given body in degrees
    """
    distance = norm(body-obs)
    angle = np.rad2deg(radius/distance)
    return angle

def overlap(obs,body1,body2,body1_radius,body2_radius) -> float:
    """
    Calculate the fraction of the first celestial body that is occulted by the second celestial body.

    :param obs: A 1-D Numpy array containing the coordinates of the observer (x, y, z)
    :param body1: A 1-D Numpy array containing the coordinates of the first celestial body (x, y, z)
    :param body2: A 1-D Numpy array containing the coordinates of the second celestial body (x, y, z)
    :param body1_radius: A float representing the radius of the first celestial body
    :param body2_radius: A float representing the radius of the second celestial body
    :return: A float representing the fraction of the first celestial body that is occulted by the second celestial body.
    """
    obs_body1 = body1 - obs
    obs_body2 = body2 - obs
    norm_b1 = norm(obs_body1)
    norm_b2 = norm(obs_body2)
    body1_size = body1_radius/norm_b1
    body2_size = body2_radius/norm_b2
    angle_separation = np.arccos(obs_body1.dot(obs_body2)/(norm_b1*norm_b2))
    if angle_separation >= body1_size+body2_size:
        return 0
    elif angle_separation <= body1_size-body2_size and body1_size > body2_size:
        intersection = np.pi * body2_size**2
    elif angle_separation <= body2_size-body1_size and body2_size > body1_size:
        intersection = np.pi * body1_size ** 2
    else:
        alpha = np.arccos(((body1_size * body1_size) + (angle_separation * angle_separation) - (body2_size * body2_size)) / (2 * body1_size * angle_separation)) * 2
        beta = np.arccos(((body2_size * body2_size) + (angle_separation * angle_separation) - (body1_size * body1_size)) / (2 * body2_size * angle_separation)) * 2

        a1 = (0.5 * beta * body2_size * body2_size) - (0.5 * body2_size * body2_size * np.sin(beta))
        a2 = (0.5 * alpha * body1_size * body1_size) - (0.5 * body1_size * body1_size * np.sin(alpha))

        intersection = a1+a2

    intersection /= np.pi*body1_size**2
    return intersection
