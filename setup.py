from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="loka-lang",
    version="0.1.0",
    author="LOKA Developer",
    author_email="loka.dev@example.com",
    description="Un langage de programmation moderne pour l'IA",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cedric202012/loka",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Compilers",
    ],
    python_requires=">=3.8",
    install_requires=[
        "llvmlite>=0.40.0",
        "numpy>=1.21.0",
        "scikit-learn>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "loka=loka.cli:main",
        ],
    },
)
