# venv-relocate

**Only for Windows and virtual environments created by standard library venv (python -m venv)**

## Usage: 

```python venvfix.py <new_venv_python_path>```

## Example:

After you move or rename virtual environment "D:\oldpath\venv1" to "D:\newpath\venv2", the activate scripts and executable files in venv2\scripts (or venv2\bin) could not work.

Then you can execute "```python venvfix.py D:\newpath\venv2\scripts\python.exe```".

And then venv2 will work properly, you can activate it, use pip.exe and other executable files as usual.

## Notice:

The <new_venv_python_path> can be absolute or relative path of the python interpreter.

You can put this script in a place of sys.path (such as create a pth file) and use it anywhere like "```python -m venvfix .\venv2\scripts\python.exe```"
