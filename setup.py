from setuptools import setup, find_packages

setup(
    name="your_project_name",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "pocketsphinx",
        "SpeechRecognition",  # The correct package name for speech_recogniser
        "openai",
    ],
)

