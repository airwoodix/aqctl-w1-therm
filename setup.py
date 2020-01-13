from setuptools import setup, find_packages

setup(
    name="aqctl-w1-therm",
    author="Etienne Wodey",
    author_email="wodey@iqo.uni-hannover.de",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    install_requires=["sipyco", "aiofiles>=0.4.0"],
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "aqctl_w1_therm = aqctl_w1_therm.aqctl_w1_therm:main",
        ],
    },
)
