import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cache-by-key",
    version="0.0.2",
    author="Rashikraj Shrestha",
    author_email="rashik123.rs@gmail.com",
    description="cache-by-key is a lru based cache that allows you to cache by specific keyword argument from a decorated function.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Rashik-raj/cache-by-key",
    project_urls={
        "Bug Tracker": "https://github.com/Rashik-raj/cache-by-key/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
)
