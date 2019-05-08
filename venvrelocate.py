import os
import sys

if len(sys.argv) == 1:
    print('Usage: python '+sys.argv[0]+' <VENV_ABSOLUTE_PATH>')
    exit()

targetenv_path = sys.argv[1]
env_name = targetenv_path.split('\\')[-1]
activatebat_path = targetenv_path+'\\Scripts\\activate.bat'
modifiedactivatebat_path = targetenv_path+'\\Scripts\\activate.bat.tmp'
activatebat_file = open(activatebat_path, 'r')
modified_activatebat_file = open(modifiedactivatebat_path, 'w')
for line in activatebat_file:
    if "set \"VIRTUAL_ENV=" in line:
        line = "set \"VIRTUAL_ENV="+targetenv_path+'\"\n'
    if "set \"PROMPT=(" in line:
        line = "set \"PROMPT=("+env_name+") %PROMPT%\"\n"
    modified_activatebat_file.write(line)
activatebat_file.close()
modified_activatebat_file.close()
os.remove(activatebat_path)
os.rename(modifiedactivatebat_path, activatebat_path)
print(activatebat_path+' fixed')

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
