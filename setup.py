from setuptools import setup

def readme():
    with open("README.md", encoding="utf8") as f:
        return f.read()


setup(
    # This is the name of your project. The first time you publish this
    # package, this name will be registered for you. It will determine how
    # users can install this project, e.g.:
    #
    # $ pip install spongeWebPy
    #
    # And where it will live on PyPI: https://pypi.org/project/spongeWebPy/
    name='spongeWebPy',
    version="1.0.9",

    # This is a one-line description or tagline of what your project does. This
    # corresponds to the "Summary" metadata field:
    description="Provides user-friendly usage of the SPONGE API.",

    long_description=readme(),
    long_description_content_type="text/markdown",

    # This should be a valid link to your project's main homepage.
    url='https://github.com/biomedbigdata/spongeWebPy',  # Optional

    # This should be your name or the name of the organization which owns the
    # project.
    author='The List Lab - Big Data in BioMedicine',
    author_email='markus.list@wzw.tum.de',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
    ],

    # Keywords for your project which will appear on the
    # project page. What does your project relate to?
    keywords='SPONGE API ceRNAInteractions networkAnalysis',


    # You can just specify package directories manually here if your project is simple.
    packages=["spongeWebPy"],  # Required

    python_requires=">=3.5, <4",

    # This field lists other packages that your project depends on to run.
    # Any package you put here will be installed by pip when your project is
    # installed, so they must be valid existing projects.
    #
    # For an analysis of "install_requires" vs pip's requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[
        "certifi>=2019.11.28",
        "chardet>=3.0.4",
        "idna>=2.9",
        "numpy>=1.18.1",
        "pandas>=1.0.1",
        "python-dateutil>=2.8.1",
        "pytz>=2019.3",
        "requests>=2.23.0",
        "six>=1.14.0",
        "urllib3>=1.25.8"
    ],

    include_package_data=True,
    zip_safe=False)