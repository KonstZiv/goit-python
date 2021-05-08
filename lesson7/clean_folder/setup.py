from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="clean_folder",
    version="1.0.0",
    author="Konstyantin Zivenko",
    author_email="kos.zivenko@gmail.com",
    description="school: GoIT, group: Python On2, homework 7",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/KonstZiv/goit-python/tree/main/lesson7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU License",
        "Operating System :: OS Independent",
    ],
    #package_dir={"": "clean_folder"},
    packages=find_packages(),
    python_requires=">=3.6",
    entry_points={'console_scripts': ['clean_folder=clean_folder.clean:main']}
)
