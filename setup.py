from setuptools import setup, find_packages

setup(
    name="aiNoteMaker",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,  # Ensure data files are included
    package_data={"mypackage": ["data/*"]},  # Add data folder
    install_requires=[
        "openai==1.66.3",
        "yt-dlp==2025.2.19",
        "python-pptx==0.6.23",
        "python-dotenv==1.0.1",
        "textract==1.6.5"
    ],
)
