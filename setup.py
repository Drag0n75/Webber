from setuptools import setup, find_packages

setup(
    name="webber",
    version="1.0.0",
    description="Lightweight HTTP, scraping and Flask wrapper",
    author="Your Name",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "flask>=3.0.0",
        "httpx>=0.27.0",
        "beautifulsoup4>=4.12.0"
    ],
    python_requires=">=3.9",
)
