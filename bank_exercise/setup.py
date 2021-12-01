import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="accounts-LEONARDBISE",
    version="0.0.2",
    author="Léonard Bise",
    author_email="author@example.com",
    description="This is a package used for a tutorial",
    long_description=long_description,
    long_description_content_type="text/markdown",
#    url="https://github.com/pypa/sampleproject",
#    project_urls={
#        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
#    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "."},
    packages=setuptools.find_packages(where="."),
    python_requires=">=3.7",
    install_requires=[
            'numpy'
        ]
)
