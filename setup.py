from setuptools import setup, find_packages

setup(
    name="logmagix",                   
    version="2.0.5",                           
    packages=find_packages(),               
    install_requires=["colorama"],           
    author="Sexfrance",                     
    author_email="bwuuuuu@gmail.com",   
    description="A custom logger package",   
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/sexfrance/LogMagix",  
    classifiers=[                          
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
