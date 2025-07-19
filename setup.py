from setuptools import setup, find_packages

setup(
    name="coin_counter",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.20.0",
        "scipy>=1.7.0",
        "Pillow>=9.0.0",
        "matplotlib>=3.5.0",
        "pandas>=1.3.0",
        "kagglehub>=0.3.5",
    ],
    entry_points={
        "console_scripts": [
            "coin-counter=coin_counter.main:main",
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A Python application for detecting and counting coins in images",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/coin-counter",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)