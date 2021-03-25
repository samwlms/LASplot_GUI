setup(
    name="LASplot",
    version="1.0.0",
    description="Fast Python LiDAR Visualisation",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/samwlms/LASplot_GUI",
    author="Sam Williams",
    author_email="swilliams@uon.edu.au",
    license="none",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    packages=["python"],
    include_package_data=True,
    install_requires=[
        "appdirs==1.4.4",
        "autopep8==1.5.5",
        "black==20.8b1",
        "click==7.1.2",
        "colorama==0.4.4",
        "cycler==0.10.0",
        "kiwisolver==1.3.1",
        "laspy==1.7.0",
        "matplotlib==3.3.3",
        "mypy-extensions==0.4.3",
        "numpy==1.19.3",
        "pathlib==1.0.1",
        "pathspec==0.8.1",
        "Pillow==8.1.2",
        "pycodestyle==2.6.0",
        "pyparsing==2.4.7",
        "python-dateutil==2.8.1",
        "regex==2020.11.13",
        "scipy==1.6.1",
        "six==1.15.0",
        "toml==0.10.2",
        "typed-ast==1.4.2",
        "typing-extensions==3.7.4.3",
    ],
    entry_points={"console_scripts": ["LASplot=python.LASplot:main"]},
)
