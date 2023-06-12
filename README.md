# Fourier Ephemeris

An not-so-accurate ephemeris for the Sun and the Moon using a sum of sines approximation.

## Introduction

This recreational project presents a simple ephemeris developed by performing a Fourier transform on the Geocentric Solar Ecliptic (GSE) coordinates of the Moon and applying a least squares fit. The data used for this project is sourced from NASA's [SSC Locator Form](https://sscweb.gsfc.nasa.gov/cgi-bin/Locator.cgi) and spans from 1959 to 2040.

The ephemeris contains 20, 8, and 9 terms for the longitude, latitude, and distance of the Moon, respectively. For the Sun, the distance is represented by a single sine wave, while its latitude and longitude are assumed to be 0.

## Precision

The root-mean-square deviation of the Moon's latitude, longitude, and distance in the fitted period is 40", 51", and 165 km, respectively. While this level of precision may be considered high by modern standards, it is sufficient for predicting eclipses, as demonstrated below with the total solar eclipse of August 2, 2027. Note that the ephemeris can predict eclipses even from the year 3000, rendering it accurate enough for many centuries.

![anigif](https://github.com/PedroKKr/fourierEphem/assets/52111108/2182c447-dc76-451c-a769-c4d6ca8b9768)

## Features

The ephemeris currently supports the following calculations:

- Position of the Sun and the Moon in the GSE system
- Altitude and azimuth of the Sun and the Moon for a given observer at specific latitude and longitude coordinates
- Angular distance and apparent intersection of the Sun and the Moon, particularly useful for eclipse calculations (Eclipse animations can be created using the `eclipseAnimation.py` file and eclipses within a time range can be found using the `searchEclipses.py` file)
- Obliquity of the ecliptic, mean and true anomaly of the Earth
