from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()

requirements = [ p.strip() for p in requirements.strip().splitlines() ]

setup(
    name="quotesfinder",
    version="0.0.3",
    author="Junho Oh",
    author_email="pinedance@gmail.com",
    description="finding quotes between two texts written in old Chinese",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pinedance/python-quotesfinder",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=requirements,
    entry_points={"console_scripts": ["quotesfinder=quotesfinder.__main__:main"]},
)
