from distutils.core import setup

setup(
  name = 'fourier_ephem',
  packages = ['fourier_ephem'],
  version = '1.0.1',
  license='MIT',
  description = 'An not-so-accurate ephemeris for the Sun and the Moon using a sum of sines approximation',
  long_description=open("README.md", 'r').read(),
  long_description_content_type='text/markdown',
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
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
  ],
)
