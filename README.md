# venv-fix

**Only for Windows and virtual environments created by standard library venv (python -m venv)**

## Installation:

```pip install venvfix```

## Usage: 

```venvfix <venv_python_path>```

## Example:

After you move or rename virtual environment "D:\oldpath\venv1" to "D:\newpath\venv2", the activate scripts and executable files in venv2\scripts (or venv2\bin) could not work.

Then you can execute "```venvfix D:\newpath\venv2\scripts\python.exe```".

And then venv2 will work properly, you can activate it, use pip.exe and other executable files as usual.

## Notice:

The <venv_python_path> can be absolute or relative path of the python interpreter.
