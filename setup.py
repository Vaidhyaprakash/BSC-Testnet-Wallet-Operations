#!/usr/bin/env python3
"""
Setup script for BSC Testnet Wallet
"""

from setuptools import setup, find_packages

# Read the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="bsc-testnet-wallet",
    version="1.0.0",
    author="BSC Wallet Developer",
    author_email="developer@example.com",
    description="A comprehensive Python application for BSC Testnet wallet operations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/bsc-testnet-wallet",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Office/Business :: Financial",
        "Topic :: Security :: Cryptography",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "isort>=5.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "bsc-wallet=cli:cli",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="bsc, binance, smart, chain, testnet, wallet, crypto, blockchain, web3, ethereum",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/bsc-testnet-wallet/issues",
        "Source": "https://github.com/yourusername/bsc-testnet-wallet",
        "Documentation": "https://github.com/yourusername/bsc-testnet-wallet#readme",
    },
) 