import subprocess
from time import sleep
a=0
while True:
    print("Invio")
    a=a+1
    result = subprocess.Popen("echo "+str(a)+"\" my message\" > /dev/ttyS1", shell=True, stdout=subprocess.PIPE)
    s = result.stdout.read()
    s1 = s.decode('utf-8', 'ignore')
    sleep(1)

    