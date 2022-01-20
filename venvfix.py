import os
import sys
import argparse


def parse_args(args_list: list) -> str:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '<new_venv_python_path>',
        help='It can be absolute or relative path of the python interpreter in new venv folder.',
    )
    args_space = parser.parse_args(args_list)
    python_path = vars(args_space)['<new_venv_python_path>']
    return python_path


def is_python_exe(python_path: str) -> bool:
    with open(python_path, 'rb') as exe_file:
        raw_content = exe_file.read()
        offset_python = raw_content.find(
            b'.exe\x0a\x0d\x0aPK\x03\x04\x14\x00\x00\x00\x00\x00'
        )
    if offset_python == -1:
        return True
    else:
        return False


def parse_path(python_path: str) -> dict:
    if not (os.path.isfile(python_path) and is_python_exe(python_path)):
        print('This is not a python interpreter name.')
        exit()

    full_python_path = os.path.abspath(python_path)
    path_split = full_python_path.split('\\')
    venv_path = '\\'.join(path_split[:-2])
    python_folder_path = '\\'.join(path_split[:-1])
    venv_name = path_split[-3]
    python_name = path_split[-1]

    files_in_venv = os.listdir(venv_path)
    files_in_venv = [s.lower() for s in files_in_venv]
    if not 'pyvenv.cfg' in files_in_venv:
        print('This path is not in a venv.')
        exit()

    return {
        'venv_name': venv_name,
        'venv_path': venv_path,
        'python_name': python_name,
        'python_folder_path': python_folder_path,
    }


def match_line(search_lines: list, line: str) -> bool:
    for search in search_lines:
        if search not in line:
            return False
    return True


def fix_activate_script(paths: dict, script_name: str, replace_line: list) -> None:
    script_path = paths['python_folder_path'] + '\\' + script_name
    modified_script_path = paths['python_folder_path'] + '\\' + script_name + '.tmp'
    if not os.path.exists(script_path):
        return

    with open(script_path, 'r') as script_file, open(
        modified_script_path, 'w'
    ) as modified_script_file:
        for line in script_file:
            for search_lines, new_line in replace_line:
                if match_line(search_lines, line):
                    line = new_line
                    break
            modified_script_file.write(line)

    os.remove(script_path)
    os.rename(modified_script_path, script_path)
    print(script_path + ' fixed')


def fix_exe_files(paths: list) -> None:
    file_names = os.listdir(paths['python_folder_path'])
    for file_name in file_names:
        if file_name.split('.')[-1] == 'exe':
            file_path = paths['python_folder_path'] + '\\' + file_name
            with open(file_path, 'rb') as exe_file:
                raw_content = exe_file.read()
                offset_python = raw_content.find(
                    b'.exe\x0a\x0d\x0aPK\x03\x04\x14\x00\x00\x00\x00\x00'
                )
                if offset_python == -1:
                    continue
                start_offset = offset_python
                while raw_content[start_offset : start_offset + 2] != b'#!':
                    start_offset -= 1
                end_offset = offset_python + 4

                replace_python_path = (
                    '#!' + paths['python_folder_path'] + '\\' + paths['python_name']
                ).encode('ascii')
                new_content = (
                    raw_content[:start_offset]
                    + replace_python_path
                    + raw_content[end_offset:]
                )
            with open(file_path + '.tmp', 'wb') as modified_exe_file:
                modified_exe_file.write(new_content)
            os.remove(file_path)
            os.rename(file_path + '.tmp', file_path)
            print(file_path + ' fixed')


def create_bash_replace_line(paths: dict) -> list:
    replace_lines = []  # [([old1,old2,...],new),...]
    # 3.6 3.8
    replace_lines.append(
        (['VIRTUAL_ENV="'], 'VIRTUAL_ENV="' + paths['venv_path'] + '"\n')
    )
    # 3.6 3.8
    replace_lines.append(
        (
            [') " != x ] ; then'],
            '    if [ "x(' + paths['venv_name'] + ') " != x ] ; then\n',
        )
    )
    # 3.6 3.8 3.9
    replace_lines.append(
        ([') ${PS1:-}"'], '    PS1="(' + paths['venv_name'] + ') ${PS1:-}"\n')
    )
    # 3.9
    replace_lines.append(
        (
            ['VIRTUAL_ENV=$(cygpath'],
            'VIRTUAL_ENV=$(cygpath "' + paths['venv_path'] + '")\n',
        )
    )
    return replace_lines


def create_bat_replace_line(paths: dict) -> list:
    replace_lines = []
    # 3.6
    replace_lines.append(
        (
            ['set "VIRTUAL_ENV='],
            'set "VIRTUAL_ENV=' + paths['venv_path'] + '"\n',
        )
    )
    # 3.6
    replace_lines.append(
        (
            ['set "PROMPT=('],
            'set "PROMPT=(' + paths['venv_name'] + ') %PROMPT%"\n',
        )
    )
    # 3.8
    replace_lines.append(
        (
            ['set VIRTUAL_ENV='],
            'set VIRTUAL_ENV=' + paths['venv_path'] + '\n',
        )
    )
    # 3.8
    replace_lines.append(
        (
            ['set PROMPT=('],
            'set PROMPT=(' + paths['venv_name'] + ') %PROMPT%\n',
        )
    )
    return replace_lines


def create_ps1_replace_line(paths: dict) -> list:
    replace_lines = []
    # 3.6
    replace_lines.append(
        (
            ['$env:VIRTUAL_ENV="'],
            '$env:VIRTUAL_ENV="' + paths['venv_path'] + '"\n',
        )
    )
    # 3.6
    replace_lines.append(
        (
            ['Write-Host -NoNewline -ForegroundColor Green \'('],
            'Write-Host -NoNewline -ForegroundColor Green \'('
            + paths['venv_name']
            + ') \'\n',
        )
    )
    return replace_lines


if __name__ == '__main__':
    python_path = parse_args(sys.argv[1:])
    paths = parse_path(python_path)
    fix_activate_script(paths, 'activate', create_bash_replace_line(paths))
    fix_activate_script(paths, 'activate.bat', create_bat_replace_line(paths))
    fix_activate_script(paths, 'Activate.ps1', create_ps1_replace_line(paths))
    fix_exe_files(paths)
