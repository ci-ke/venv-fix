import os
import sys


def get_fullpath(path):
    if os.path.isdir(path):
        dirs = os.listdir(path)
        if 'Scripts' in dirs and 'Lib' in dirs:
            fullpath = os.path.realpath(path)
            return fullpath
    print('path is not a virtualenv')
    exit()


def fix_activate(targetenv_path):
    activate_path = targetenv_path+'\\Scripts\\activate'
    modified_activate_path = targetenv_path+'\\Scripts\\activate.tmp'
    activate_file = open(activate_path, 'r')
    modified_activate_file = open(modified_activate_path, 'w')
    linux_targetenv_path = targetenv_path.replace('\\', '/')
    linux_targetenv_path = '/'+linux_targetenv_path
    linux_targetenv_path = linux_targetenv_path.replace(':', '')
    for line in activate_file:
        if 'VIRTUAL_ENV="$(if [ "$OSTYPE" "==" "cygwin" ]; then cygpath -u' in line:
            line = 'VIRTUAL_ENV="$(if [ "$OSTYPE" "==" "cygwin" ]; then cygpath -u \'' + \
                targetenv_path+'\'; else echo \''+linux_targetenv_path+'\'; fi;)"\n'
        modified_activate_file.write(line)
    activate_file.close()
    modified_activate_file.close()
    os.remove(activate_path)
    os.rename(modified_activate_path, activate_path)
    print(activate_path+' fixed')


def fix_activate_bat(targetenv_path):
    env_name = targetenv_path.split('\\')[-1]
    activate_bat_path = targetenv_path+'\\Scripts\\activate.bat'
    modifiedactivate_bat_path = targetenv_path+'\\Scripts\\activate.bat.tmp'
    activate_bat_file = open(activate_bat_path, 'r')
    modified_activate_bat_file = open(modifiedactivate_bat_path, 'w')
    for line in activate_bat_file:
        if "set \"VIRTUAL_ENV=" in line:
            line = "set \"VIRTUAL_ENV="+targetenv_path+'\"\n'
        if "set \"PROMPT=(" in line:
            line = "set \"PROMPT=("+env_name+") %PROMPT%\"\n"
        modified_activate_bat_file.write(line)
    activate_bat_file.close()
    modified_activate_bat_file.close()
    os.remove(activate_bat_path)
    os.rename(modifiedactivate_bat_path, activate_bat_path)
    print(activate_bat_path+' fixed')


def fix_activate_xsh(targetenv_path):
    activate_xsh_path = targetenv_path+'\\Scripts\\activate.xsh'
    modified_activate_xsh_path = targetenv_path+'\\Scripts\\activate.xsh.tmp'
    activate_xsh_file = open(activate_xsh_path, 'r')
    modified_activate_xsh_file = open(modified_activate_xsh_path, 'w')
    for line in activate_xsh_file:
        if '$VIRTUAL_ENV = r"' in line:
            line = '$VIRTUAL_ENV = r"'+targetenv_path+'"\n'
        modified_activate_xsh_file.write(line)
    activate_xsh_file.close()
    modified_activate_xsh_file.close()
    os.remove(activate_xsh_path)
    os.rename(modified_activate_xsh_path, activate_xsh_path)
    print(activate_xsh_path+' fixed')


def fix_exe_interpreter(targetenv_path):
    scriptexe_names = os.listdir(targetenv_path+'\\Scripts')
    for scriptexe_name in scriptexe_names:
        if scriptexe_name.split('.')[-1] == 'exe' and scriptexe_name != 'python.exe' and scriptexe_name != 'pythonw.exe':
            scriptexe_path = targetenv_path+'\\Scripts\\'+scriptexe_name
            scriptexe_file = open(scriptexe_path, 'rb')
            rawcontent = scriptexe_file.read()
            offset_python = rawcontent.find(b'python.exe\x0a\x0d\x0aPK')
            if offset_python == -1:
                continue
            end_offset = offset_python+10
            start_offset = offset_python
            while rawcontent[start_offset:start_offset+2] != b'#!':
                start_offset -= 1
            replace_python_path = ('#!'+targetenv_path +
                                   '\\Scripts\\python.exe').encode()
            newcontent = rawcontent[:start_offset] + \
                replace_python_path+rawcontent[end_offset:]
            scriptexe_file.close()
            modified_scriptexe_file = open(scriptexe_path+'.tmp', 'wb')
            modified_scriptexe_file.write(newcontent)
            modified_scriptexe_file.close()
            os.remove(scriptexe_path)
            os.rename(scriptexe_path+'.tmp', scriptexe_path)
            print(scriptexe_path+' fixed')


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print('Usage: python '+sys.argv[0]+' <VENV_PATH>')
        exit()
    targetenv_path = sys.argv[1]
    targetenv_path = get_fullpath(targetenv_path)
    fix_activate(targetenv_path)
    fix_activate_bat(targetenv_path)
    fix_activate_xsh(targetenv_path)
    fix_exe_interpreter(targetenv_path)
