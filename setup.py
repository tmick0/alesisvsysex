from setuptools import setup, find_packages

setup(
    name="alesisvsysex",
    version="0.0.1",
    install_requires=["pytest", "python-rtmidi", "mido", "vext.pyqt5"],
    packages=find_packages(),
    entry_points={
        'console_scripts': ['alesisvsysex=alesisvsysex.__main__:main'],
    }
)

