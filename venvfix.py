import sys, os, argparse, re
from typing import Dict, List, Tuple

__version__ = '0.3.5'

non_python_exe_have = b'.exe\x0a\x0d\x0aPK\x03\x04\x14\x00\x00\x00\x00\x00'


def is_python_exe(paths: Dict[str, str]) -> bool:
    if not os.path.isfile(paths['python_path']):
        return False
    if (
        paths['python_name'] == 'pythonw.exe'
        or paths['python_name'][-4:] != '.exe'
        or paths['python_name'].find('python') == -1
    ):
        return False
    with open(paths['python_path'], 'rb') as exe_file:
        if exe_file.read().find(non_python_exe_have) != -1:
            return False
    return True


def parse_path(python_path: str) -> Dict[str, str]:
    paths = {'python_path': python_path}
    try:
        path_split = python_path.split('\\')
        paths['venv_path'] = '\\'.join(path_split[:-2])
        paths['python_folder_path'] = '\\'.join(path_split[:-1])
        paths['venv_name'] = path_split[-3]
        paths['python_name'] = path_split[-1]
    except IndexError:
        sys.exit(print('Error: bad input path'))

    if not is_python_exe(paths):
        sys.exit(print('Error: not a python interpreter'))

    if not 'pyvenv.cfg' in [s.lower() for s in os.listdir(paths['venv_path'])]:
        sys.exit(print('Error: not a venv'))

    return paths


def detect_old_name(paths: Dict[str, str]) -> str:
    try:
        with open(paths['python_folder_path'] + '\\activate', 'r') as script_file:
            mat = re.search(r'VIRTUAL_ENV.*"[a-zA-Z]:.*\\(.*)"', script_file.read())
            if mat is not None:
                return mat.group(1)
            else:
                sys.exit(print('Fatal error: can not detect old venv name'))
    except FileNotFoundError:
        sys.exit(
            print('Error: can not detect old venv name, please specify it by -n option')
        )


def parse_args() -> Tuple[Dict[str, str], str]:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'PYTHON_PATH',
        help='absolute or relative path of the python interpreter executable in venv',
    )
    parser.add_argument(
        '-n',
        '--name',
        default=None,
        metavar='OLD_NAME',
        help='old name of the venv, provide when auto detection can not work properly',
    )
    args = parser.parse_args()
    paths = parse_path(os.path.abspath(args.PYTHON_PATH))
    old_name = detect_old_name(paths) if args.name is None else args.name
    return paths, old_name


def fix_activate_script(
    paths: Dict[str, str],
    script_names: List[str],
    old_name: str,
) -> None:
    old_name = re.escape(old_name)
    for script_name in script_names:
        script_path = paths['python_folder_path'] + '\\' + script_name
        modified_script_path = script_path + '.tmp'

        if not os.path.exists(script_path):
            continue

        with open(script_path, 'r') as script_file, open(
            modified_script_path, 'w'
        ) as modified_script_file:
            raw_text = script_file.read()
            text1 = re.sub(
                r'[a-zA-Z]:\\.*\\' + old_name + r'([\n"])',
                paths['venv_path'].replace('\\', r'\\') + r'\1',
                raw_text,
            )
            text2 = re.sub(
                r'[a-zA-Z]:\\' + old_name + r'([\n"])',
                paths['venv_path'].replace('\\', r'\\') + r'\1',
                text1,
            )
            new_text = re.sub(
                r'\(' + old_name + r'\)', '(' + paths["venv_name"] + ')', text2
            )
            modified_script_file.write(new_text)

        os.remove(script_path)
        os.rename(modified_script_path, script_path)

        if raw_text != new_text:
            print(script_path + ' modified')
        else:
            print(script_path + ' no change')


def fix_exe_files(paths: Dict[str, str]) -> None:
    file_names = os.listdir(paths['python_folder_path'])
    for file_name in file_names:
        if file_name.split('.')[-1] == 'exe':
            file_path = paths['python_folder_path'] + '\\' + file_name
            modified_file_path = file_path + '.tmp'
            with open(file_path, 'rb') as exe_file:
                raw_text = exe_file.read()
                offset_python = raw_text.find(non_python_exe_have)

                if offset_python == -1:
                    continue

                start_offset = offset_python
                while raw_text[start_offset : start_offset + 2] != b'#!':
                    start_offset -= 1
                end_offset = offset_python + 4
                replace_python_path = ('#!' + paths['python_path']).encode('ascii')
                new_text = (
                    raw_text[:start_offset]
                    + replace_python_path
                    + raw_text[end_offset:]
                )
            with open(modified_file_path, 'wb') as modified_exe_file:
                modified_exe_file.write(new_text)

            os.remove(file_path)
            os.rename(modified_file_path, file_path)

            if raw_text[start_offset:end_offset] != replace_python_path:
                print(file_path + ' modified')
            else:
                print(file_path + ' no change')


def fix_python_scripts(paths: Dict[str, str]) -> None:
    file_names = os.listdir(paths['python_folder_path'])
    for file_name in file_names:
        if file_name.split('.')[-1] == 'py':
            file_path = paths['python_folder_path'] + '\\' + file_name
            modified_file_path = file_path + '.tmp'
            with open(file_path, 'r') as script_file:
                first_line = script_file.readline()

                if first_line[:2] != '#!':
                    continue

                remains = script_file.read()
                new_first_line = '#!' + paths['python_path'] + '\n'
            with open(modified_file_path, 'w') as modified_script_file:
                modified_script_file.write(new_first_line + remains)

            os.remove(file_path)
            os.rename(modified_file_path, file_path)

            if first_line != new_first_line:
                print(file_path + ' modified')
            else:
                print(file_path + ' no change')


def main() -> None:
    paths, old_name = parse_args()
    fix_activate_script(paths, ['activate', 'activate.bat', 'Activate.ps1'], old_name)
    fix_exe_files(paths)
    fix_python_scripts(paths)


if __name__ == '__main__':
    main()
