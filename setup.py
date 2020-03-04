from setuptools import setup, find_packages

__version__ = "1.0.0"

setup(
    name="itembox",
    version=__version__,
    packages=find_packages(exclude=["tests*"]),
    include_package_data=True,
    install_requires=[
        "connexion",
        "connexion[swagger-ui]",
        "flask",
        "flask-cors",
        "flask-sqlalchemy",
        "flask-migrate",
        "flask-marshmallow",
        "marshmallow-sqlalchemy",
        "python-dotenv",
    ],
    entry_points={
        "console_scripts": [
            "itembox = itembox.manage:cli"
        ]
    },
)