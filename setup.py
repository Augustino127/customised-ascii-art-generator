"""
Setup script pour le générateur ASCII art.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Lecture du README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8") if (this_directory / "README.md").exists() else ""

setup(
    name="ascii-art-generator",
    version="1.0.0",
    author="ASCII Art Generator Team",
    description="Générateur ASCII art personnalisé avec fonctionnalités avancées",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ascii-art-generator",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Artistic Software",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "Pillow>=10.0.0",
        "numpy>=1.24.0",
        "opencv-python>=4.8.0",
        "rich>=13.0.0",
        "click>=8.1.0",
        "prompt-toolkit>=3.0.0",
        "pyfiglet>=0.8.0",
        "art>=6.0",
        "imageio>=2.31.0",
        "imageio-ffmpeg>=0.4.9",
        "scipy>=1.11.0",
        "scikit-image>=0.21.0",
        "svgwrite>=1.4.3",
        "colorama>=0.4.6",
        "termcolor>=2.3.0",
    ],
    entry_points={
        "console_scripts": [
            "ascii-gen=ascii_generator.cli.main:cli",
        ],
    },
    include_package_data=True,
    keywords=[
        "ascii",
        "art",
        "generator",
        "image",
        "text",
        "animation",
        "converter",
        "cli",
    ],
)
