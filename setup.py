import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fourier_ephem",
    version="1.0.0",
    author="Pedro Kleinschmitt Krause",
    description="An not-so-accurate ephemeris for the Sun and the Moon using a sum of sines approximation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    py_modules=["fourier_ephem"],
    package_dir={'':'src/fourier_ephem'},
    install_requires=["numpy","datetime"]
)
