import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lazysql",
    version="0.0.1",
    author="silvercondor",
    author_email="silvercondor@protonmail.com",
    description="SQL connector for lazy people",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/silvercondor/lazy-sql",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
