import numpy as np

# Load data
lon_omega = np.load("lon_freq", allow_pickle=True) * 2 * np.pi
lon_amp = np.load("lon_amp", allow_pickle=True)
lon_phases = np.load("lon_phases", allow_pickle=True)

lat_omega = np.load("lat_freq", allow_pickle=True) * 2 * np.pi
lat_amp = np.load("lat_amp", allow_pickle=True)
lat_phases = np.load("lat_phases", allow_pickle=True)

dis_omega = np.load("dis_freq", allow_pickle=True) * 2 * np.pi
dis_amp = np.load("dis_amp", allow_pickle=True)
dis_phases = np.load("dis_phases", allow_pickle=True)


def moon_gse(t: float) -> tuple:
    """
    Returns the moon latitude(°), longitude(°) and radial distance(km) in Geocentric Solar Ecliptic (GSE) coordinates
    :param t: Time in Excel format. Days (24h) since 31/12/1899 00:00:00
    :return: (latitude, longitude, distance)
    """
    lon = lon_amp.dot(np.sin(t * lon_omega + lon_phases)) + 360 / 29.530589 * t - 262827.5235067
    lat = lat_amp.dot(np.sin(t * lat_omega + lat_phases))
    dis = dis_amp.dot(np.sin(t * dis_omega + dis_phases)) + 385000.4411
    return lat, lon, dis

def sun_distance(t: float) -> float:
    """
    Returns the sun's radial distance(km)
    :param t: Time in Excel format. Days (24h) since 31/12/1899 00:00:00
    :return: distance
    """
    dis = 149618828.7 + 2499293.007*np.sin(0.017201970017786433*t-1.62743406471495)
    return dis

def obliquity(t: float) -> float:
    """
    Returns the obliquity of the ecliptic in degrees
    :param t: Time in Excel format. Days (24h) since 31/12/1899 00:00:00
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

def mean_anomaly(t):
    # Earth-Moon barycenter perihelion
    t0 = 36528.9967245370
    ma = 2*np.pi/365.24218*(t-t0)
    return ma

def true_anomaly(t):
    ma = mean_anomaly(t)
    ec = 0.01671022
    # Equation of center
    ta = ma + (2*ec-1/4*ec**3 + 5/96*ec**5)*np.sin(ma) + (5/4*ec**2-11/24*ec**4)*np.sin(2*ma) + 13/12*ec**3*np.sin(3*ma)
    return ta

def observer_position(t,lat,lon):
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

    pos = orbit_rotation @ equinox_rotation @ day_rotation @ pos0
    return pos*earth_radius

def sun_position(t):
    pos = np.array([sun_distance(t),0,0])
    return pos

def moon_position(t):
    lat, lon, dis = moon_gse(t)
    lat, lon = np.deg2rad(lat), np.deg2rad(lon)

    dcos_lat = dis*np.cos(lat)
    x = dcos_lat*np.cos(lon)
    y = dcos_lat*np.sin(lon)
    z = dis*np.sin(lat)

    return np.array([x,y,z])

def alt(body,obs):
    body = body - obs
    angle = np.pi/2 - anglew(body,obs)
    return np.rad2deg(angle)

def separation(obs,body1,body2):
    obs_body1 = body1-obs
    obs_body2 = body2-obs
    return anglew(obs_body1,obs_body2)

def angular_radius(obs,body,radius):
    distance = norm(body-obs)
    angle = np.rad2deg(radius/distance)
    return angle

def overlap(obs,body1,body2,body1_radius,body2_radius):
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