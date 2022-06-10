# venv-fix

**Only for Windows and virtual environments created by standard library venv (python -m venv)**

After you move or rename a virtual environment (v-env) leading to its path be changed, the activate scripts and executable files in v-env\scripts (or v-env\bin) could no longer work. Howerver, *venvfix* can fix the "path crash" and let v-env return to normal without reinstalling.

## Installation

```pip install venvfix```

## Usage

```venvfix VENV_PYTHON_PATH [-n OLD_VENV_NAME]```

## Example

After you move and rename a v-env from "D:\oldpath\venv1" to "E:\newpath\venv2", you can execute "```venvfix E:\newpath\venv2\scripts\python.exe```", and then venv2 will act normally again, you can activate it, use pip.exe and other executable files as usual.

## Notice

VENV_PYTHON_PATH can be absolute or relative path of the python interpreter executable in v-env.

OLD_VENV_NAME is not required because venvfix can dectect it automatically, but you can specify it if auto detection could not work properly.
