from setuptools import find_packages, setup

setup(
    name="dryad",
    version="1.0.0",
    description="Description of your library",
    long_description="Long description of your library",
    author="zweix123",
    author_email="1979803044@qq.com",
    url="https://github.com/zweix123/dryad",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "dryad = dryad.execute:main",
        ],
    },
)
