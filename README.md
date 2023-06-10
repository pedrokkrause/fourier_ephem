# Fourier Ephemeris
A not so accurate ephemeris for the Sun and the Moon using a sum of sines approximation.
-
This is a recreative project to develop a simple ephemeris. This was done by performing a fourier transform on the Geocentric Solar Ecliptic (GSE) coordinates of the Moon and then perfoming a least squares fit, using data from NASA's [SSC Locator Form](https://sscweb.gsfc.nasa.gov/cgi-bin/Locator.cgi) from 1959 to 2040. 

There are 20, 8 and 9 terms for the longitude, latitude and distance of the Moon, respectively. For the Sun, the distance is only given by one sine wave, and its latitude and logitude is assumed to be 0. 

Regarding the precision, the root-mean-square deviation of the Moon's latitude, longitude and distance in the fitted period are 40", 51" and 165 km. While this is extremely high for today's standards, this is sufficiently accurate to predict eclipses. Below is the total solar eclipse of August 2, 2027. Note, that it can also predict eclipses from the year 3000, so it may be considered sufficiently accurate for many centuries.

![anigif](https://github.com/PedroKKr/fourierEphem/assets/52111108/2182c447-dc76-451c-a769-c4d6ca8b9768)

The main usage of this ephemeris is to calculate the position of the Sun and the Moon for a given latitude and longitude. As of now, it can only calculate the altitude, not the azimuth, which will be futurely added.
