from setuptools import setup, find_packages

setup(
    name="webber",
    version="1.0.0",
    description="Async Flask + HTTPX + BeautifulSoup wrapper",
    packages=find_packages(),
    install_requires=[
        "flask",
        "httpx",
        "beautifulsoup4"
    ],
)
