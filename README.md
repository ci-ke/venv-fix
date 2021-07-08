# venv-relocate

**Only for Windows and virtual environments created by "python -m venv"**

## Usage: 

python venvrelocate.py <VENV_PATH> (modified_python_name)

## Example:

After you move or rename virtual environment D:\venvs\venv1 to D:\venvs\venv2, the activate scripts and executable files in venv2\scripts should not work.

Then you can execute "python venvrelocate.py D:\venvs\venv2".

And then venv2 will work properly, you can activate it and use pip as usual.

## Notice:

If there is a modified python name in the venv\scripts such as "python3.exe" or "python36.exe"... , you should also send this name to arguments. (e.g. python venvrelocate.py venv1 python36.exe).