import os
import sys


def is_python_exe(python_path: str) -> bool:
    with open(python_path, 'rb') as exe_file:
        raw_content = exe_file.read()
        offset_python = raw_content.find(b'.exe\x0a\x0d\x0aPK\x03\x04\x14\x00\x00\x00\x00\x00')
    if offset_python == -1:
        return True
    else:
        return False


def parse_path(python_path: str) -> tuple:
    if os.path.isfile(python_path) and is_python_exe(python_path):
        full_python_path = os.path.abspath(python_path)
        path_split = full_python_path.split('\\')

        venv_path = '\\'.join(path_split[:-2])
        python_folder_path = '\\'.join(path_split[:-1])
        venv_name = path_split[-3]
        python_name = path_split[-1]

        files_in_venv = os.listdir(venv_path)
        files_in_venv = [s.lower() for s in files_in_venv]
        if 'lib' in files_in_venv and 'pyvenv.cfg' in files_in_venv:
            return venv_path, python_folder_path, python_name, venv_name
        else:
            print('This path is not in a venv.')
            exit()
    else:
        print('This is not a python interpreter name.')
        exit()


def fix_activate(venv_path, python_folder_path, python_name, venv_name) -> None:
    activate_path = python_folder_path+'\\activate'
    modified_activate_path = python_folder_path+'\\activate.tmp'
    if not os.path.exists(activate_path):
        return
    activate_file = open(activate_path, 'r')
    modified_activate_file = open(modified_activate_path, 'w')

    for line in activate_file:
        if 'VIRTUAL_ENV=\"' in line:  # old file
            line = 'VIRTUAL_ENV=\"'+venv_path+'\"\n'
        if 'VIRTUAL_ENV=$(cygpath' in line:  # new file
            line = 'VIRTUAL_ENV=$(cygpath \"'+venv_path+'\")\n'
        if ') \" != x ] ; then' in line:  # old file
            line = '    if [ \"x('+venv_name+') \" != x ] ; then\n'
        if ') ${PS1:-}\"' in line:  # old and new file
            line = '    PS1=\"('+venv_name+') ${PS1:-}\"\n'
        modified_activate_file.write(line)

    activate_file.close()
    modified_activate_file.close()
    os.remove(activate_path)
    os.rename(modified_activate_path, activate_path)
    print(activate_path+' fixed')


def fix_activate_bat(venv_path, python_folder_path, python_name, venv_name) -> None:
    activate_path = python_folder_path+'\\activate.bat'
    modified_activate_path = python_folder_path+'\\activate.bat.tmp'
    if not os.path.exists(activate_path):
        return
    activate_file = open(activate_path, 'r')
    modified_activate_file = open(modified_activate_path, 'w')

    for line in activate_file:
        if 'set VIRTUAL_ENV=' in line:
            line = 'set VIRTUAL_ENV='+venv_path+'\n'
        if 'set PROMPT=(' in line:
            line = 'set PROMPT=('+venv_name+') %PROMPT%\n'
        modified_activate_file.write(line)

    activate_file.close()
    modified_activate_file.close()
    os.remove(activate_path)
    os.rename(modified_activate_path, activate_path)
    print(activate_path+' fixed')


def fix_activate_ps1(venv_path, python_folder_path, python_name, venv_name) -> None:
    activate_path = python_folder_path+'\\activate.ps1'
    modified_activate_path = python_folder_path+'\\activate.ps1.tmp'
    if not os.path.exists(activate_path):
        return
    activate_file = open(activate_path, 'r')
    modified_activate_file = open(modified_activate_path, 'w')

    for line in activate_file:
        if '$env:VIRTUAL_ENV=\"' in line:  # old file
            line = '$env:VIRTUAL_ENV=\"'+venv_path+'\"\n'
        if 'Write-Host -NoNewline -ForegroundColor Green \'(' in line:  # old file
            line = 'Write-Host -NoNewline -ForegroundColor Green \'('+venv_name+') \'\n'
        modified_activate_file.write(line)

    activate_file.close()
    modified_activate_file.close()
    os.remove(activate_path)
    os.rename(modified_activate_path, activate_path)
    print(activate_path+' fixed')


def fix_exe_interpreter(venv_path, python_folder_path, python_name, venv_name) -> None:
    file_names = os.listdir(python_folder_path)
    for file_name in file_names:
        if file_name.split('.')[-1] == 'exe':
            file_path = python_folder_path+'\\'+file_name
            exe_file = open(file_path, 'rb')

            raw_content = exe_file.read()
            offset_python = raw_content.find(b'.exe\x0a\x0d\x0aPK\x03\x04\x14\x00\x00\x00\x00\x00')
            if offset_python == -1:
                continue
            start_offset = offset_python
            while raw_content[start_offset:start_offset+2] != b'#!':
                start_offset -= 1
            end_offset = offset_python+4

            replace_python_path = ('#!'+python_folder_path+'\\'+python_name).encode('ascii')
            new_content = raw_content[:start_offset]+replace_python_path+raw_content[end_offset:]

            exe_file.close()
            modified_exe_file = open(file_path+'.tmp', 'wb')
            modified_exe_file.write(new_content)
            modified_exe_file.close()
            os.remove(file_path)
            os.rename(file_path+'.tmp', file_path)
            print(file_path+' fixed')


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Usage: python '+sys.argv[0]+' <new_venv_python_path>')
        exit()
    python_path = sys.argv[1]
    ret = parse_path(python_path)
    fix_activate(*ret)
    fix_activate_bat(*ret)
    fix_activate_ps1(*ret)
    fix_exe_interpreter(*ret)
