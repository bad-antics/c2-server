from setuptools import setup, find_packages

setup(
    name="c2-server",
    version="2.0.0",
    author="bad-antics",
    description="Command & Control server framework for red team operations",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=["requests", "colorama", "pyyaml", "rich"],
)
