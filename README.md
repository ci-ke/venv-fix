# venv-relocate

**Only for Windows and virtual environments created by standard library venv (python -m venv)**

## Usage: 

```python venvrelocate.py <new_venv_python_path>```

## Example:

After you move or rename virtual environment "D:\venvs\venv1" to "D:\venvs\venv2", the activate scripts and executable files in venv2\scripts (or venv2\bin) could not work.

Then you can execute "```python venvrelocate.py D:\venvs\venv2\scripts\python.exe```".

And then venv2 will work properly, you can activate it, use pip.exe and other executable files as usual.

## Notice:

The <new_venv_python_path> can be absolute or relative path of the python interpreter.

You can put this script in a place of sys.path (such as create a pth file) and use it anywhere like "```python -m venvrelocate .\venv2\scripts\python.exe```"