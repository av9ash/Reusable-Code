import subprocess


def exec_command(cmd):
    try:
        _proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        _output = _proc.stdout.read().decode('utf-8', errors='ignore')
        _proc.stdout.close()
        return _output

    except Exception as e:
        pass
        print(e)
        return None


# print(exec_command('ls'))
