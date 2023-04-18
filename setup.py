import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="thonny-flake",
    version="1.0.3",
    author="Bigjango13",
    description="A plugin that adds flake8 warnings to the Thonny Python IDE.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bigjango13/thonny-flake",
    packages=["thonnycontrib.thonny-flake8"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Environment :: Plugins",
        "Intended Audience :: Education",
        "Operating System :: OS Independent",
    ],
    install_requires=["thonny >= 3.0.0", "Flake8"],
    python_requires=">=3.7",
)
