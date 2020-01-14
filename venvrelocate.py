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
    if not os.path.exists(activate_path):
        return
    activate_file = open(activate_path, 'r')
    modified_activate_file = open(modified_activate_path, 'w')
    linux_targetenv_path = targetenv_path.replace('\\', '/')
    linux_targetenv_path = '/'+linux_targetenv_path
    linux_targetenv_path = linux_targetenv_path.replace(':', '')
    for line in activate_file:
        if 'VIRTUAL_ENV=\"' in line:
            line = 'VIRTUAL_ENV=\"'+targetenv_path+'\"\n'
        modified_activate_file.write(line)
    activate_file.close()
    modified_activate_file.close()
    os.remove(activate_path)
    os.rename(modified_activate_path, activate_path)
    print(activate_path+' fixed')


def fix_activate_bat(targetenv_path):
    env_name = targetenv_path.split('\\')[-1]
    activate_path = targetenv_path+'\\Scripts\\activate.bat'
    modified_activate_path = targetenv_path+'\\Scripts\\activate.bat.tmp'
    if not os.path.exists(activate_path):
        return
    activate_file = open(activate_path, 'r')
    modified_activate_file = open(modified_activate_path, 'w')
    for line in activate_file:
        if "set \"VIRTUAL_ENV=" in line:
            line = "set \"VIRTUAL_ENV="+targetenv_path+'\"\n'
        if "set \"PROMPT=(" in line:
            line = "set \"PROMPT=("+env_name+") %PROMPT%\"\n"
        modified_activate_file.write(line)
    activate_file.close()
    modified_activate_file.close()
    os.remove(activate_path)
    os.rename(modified_activate_path, activate_path)
    print(activate_path+' fixed')


def fix_activate_ps1(targetenv_path):
    env_name = targetenv_path.split('\\')[-1]
    activate_path = targetenv_path+'\\Scripts\\activate.ps1'
    modified_activate_path = targetenv_path+'\\Scripts\\activate.ps1.tmp'
    if not os.path.exists(activate_path):
        return
    activate_file = open(activate_path, 'r')
    modified_activate_file = open(modified_activate_path, 'w')
    for line in activate_file:
        if "$env:VIRTUAL_ENV=\"" in line:
            line = "$env:VIRTUAL_ENV=\""+targetenv_path+'\"\n'
        if "Write-Host -NoNewline -ForegroundColor Green \'(" in line:
            line = "Write-Host -NoNewline -ForegroundColor Green \'(" + \
                env_name+") \'\n"
        modified_activate_file.write(line)
    activate_file.close()
    modified_activate_file.close()
    os.remove(activate_path)
    os.rename(modified_activate_path, activate_path)
    print(activate_path+' fixed')


def fix_exe_interpreter(targetenv_path, modified_python_name):
    scriptexe_names = os.listdir(targetenv_path+'\\Scripts')
    for scriptexe_name in scriptexe_names:
        if scriptexe_name.split('.')[-1] == 'exe' and scriptexe_name != 'python.exe' and scriptexe_name != 'pythonw.exe' and scriptexe_name != modified_python_name:
            scriptexe_path = targetenv_path+'\\Scripts\\'+scriptexe_name
            scriptexe_file = open(scriptexe_path, 'rb')
            rawcontent = scriptexe_file.read()
            if modified_python_name:
                offset_python = offset_python = rawcontent.find(
                    bytes(modified_python_name, 'ascii')+b'\x0a\x0d\x0aPK')
            else:
                offset_python = rawcontent.find(b'python.exe\x0a\x0d\x0aPK')
            if offset_python == -1:
                continue
            if modified_python_name:
                end_offset = offset_python+len(modified_python_name)
                replace_python_path = ('#!'+targetenv_path +
                                       '\\Scripts\\'+modified_python_name).encode('ascii')
            else:
                end_offset = offset_python+10
                replace_python_path = ('#!'+targetenv_path +
                                       '\\Scripts\\python.exe').encode('ascii')
            start_offset = offset_python
            while rawcontent[start_offset:start_offset+2] != b'#!':
                start_offset -= 1
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
    if len(sys.argv) != 2 and len(sys.argv) != 3:
        print('Usage: python '+sys.argv[0] +
              ' <VENV_PATH> (modified_python_name)')
        exit()
    targetenv_path = sys.argv[1]
    targetenv_path = get_fullpath(targetenv_path)
    if len(sys.argv) == 3:
        modified_python_name = sys.argv[2]
    else:
        modified_python_name = None
    fix_activate(targetenv_path)
    fix_activate_bat(targetenv_path)
    fix_activate_ps1(targetenv_path)
    fix_exe_interpreter(targetenv_path, modified_python_name)
