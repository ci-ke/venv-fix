from setuptools import setup

setup(
    name="venvfix",
    version="0.3.0",
    keywords=["venv", "fix"],
    description="A python script to fix venv environments",
    long_description="A python script to fix the python virtual environments (standard library venv) after moved or renamed without reinstalling through pip",
    license="MIT Licence",
    url="https://github.com/ci-ke/venv-fix",
    author="cike",
    python_requires='>=3.3',
    py_modules=['venvfix'],
    entry_points={'console_scripts': ['venvfix = venvfix:main']},
)
