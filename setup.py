from distutils.core import setup
setup(
  name = 'fourier_ephem',
  packages = ['fourier_ephem'],
  version = '0.1',
  license='MIT',
  description = 'An not-so-accurate ephemeris for the Sun and the Moon using a sum of sines approximation',
  author = 'Pedro Kleinschmitt Krause',
  url = 'https://github.com/PedroKKr/fourier_ephem',
  download_url = 'https://github.com/PedroKKr/fourier_ephem/archive/refs/tags/v1.0.0.tar.gz',
  keywords = ['fourier', 'ephemeris', 'astronomy'],
  install_requires=[
          'numpy',
          'datetime',
      ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.x',
  ],
)
