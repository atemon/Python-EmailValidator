"""Setup.py file for atemon.EmailValidator package."""
from distutils.core import setup

setup(
    name='Atemon-EmailValidator',
    version='0.1.2.0',
    packages=['atemon', 'atemon.EmailValidator'],
    long_description="Check if the given email address is valid or not using nslookup",
    author="Varghese Chacko",
    author_email="varghese@atemon.com",
    url="https://github.com/atemon/Python-EmailValidator",
    provides=["EmailValidator"],
    license="MIT License",
)
