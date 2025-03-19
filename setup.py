from setuptools import setup, find_packages

setup(
    name="rf_gds",
    version="0.1.0",
    description="A library for converting YAML descriptions of RF components to GDS files",
    author="RF GDS Team",
    packages=find_packages(),
    install_requires=[
        "gdsfactory>=7.0.0",
        "pyyaml>=6.0",
        "numpy>=1.20.0",
        "matplotlib>=3.5.0",
        "pydantic>=2.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=23.0.0",
            "isort>=5.10.0",
            "mypy>=1.0.0",
            "sphinx>=5.0.0",
        ]
    },
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "rf-gds=rf_gds.cli:main",
        ],
    },
)
