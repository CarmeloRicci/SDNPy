import subprocess
result = subprocess.Popen("cat /dev/ttyS1", shell=True, stdout=subprocess.PIPE)
s = result.stdout.read()
s1 = s.decode('utf-8', 'ignore')
print(s1)
