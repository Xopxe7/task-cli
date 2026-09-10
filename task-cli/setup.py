from setuptools import setup, find_packages

setup(
    name="task-cli",
    version="0.1.0",
    description="A simple, no-nonsense command-line task manager",
    packages=find_packages(exclude=["tests"]),
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "task-cli=taskcli.cli:main",
        ],
    },
)
