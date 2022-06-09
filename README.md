# venv-fix

**Only for Windows and virtual environments created by standard library venv (python -m venv)**

## Installation:

```pip install venvfix```

## Usage: 

```venvfix [-h] -p VENV_PYTHON_PATH [-n OLD_VENV_NAME]```

## Example:

After you move or rename virtual environment "D:\oldpath\venv1" to "D:\newpath\venv2", the activate scripts and executable files in venv2\scripts (or venv2\bin) could not work.

Then you can execute "```venvfix -p D:\newpath\venv2\scripts\python.exe -n venv1```".

And then venv2 will work properly, you can activate it, use pip.exe and other executable files as usual.

## Notice:

VENV_PYTHON_PATH can be absolute or relative path of the python interpreter executable.

OLD_VENV_NAME is not required if the virtual environment name has no change, you can check the old name from activate scripts.
