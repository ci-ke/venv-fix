# virtualenv-relocate
A python script to fix the python virtual environment after moved or renamed.

**Only for Windows**

## Usage: 

python venvrelocate.py <VENV_ABSOLUTE_PATH>

## Example:

After you move or rename D:\venvs\venv1 to D:\venvs\venv2, the activate.bat and executable files in venv2\scripts should not work.

Then you can execute "python venvrelocate.py D:\venvs\venv2".

And then venv2 will work properly, you can activate it and use pip as usual.
