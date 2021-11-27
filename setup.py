import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pycoli-yths",
    version="0.0.1",
    author="Yannik Schelske",
    author_email="pycoli@yths.de",
    description="A Python Color Library.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yths/yths.color",
    project_urls={
        "Bug Tracker": "https://github.com/yths/yths.color/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.9",
)