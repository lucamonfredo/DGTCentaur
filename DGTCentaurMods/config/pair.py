import time
import select
import bluetooth
import subprocess
import psutil
from DGTCentaurMods.display import epaper

epaper.initEpaper()
time.sleep(3)

for p in psutil.process_iter(attrs=['pid', 'name']):
    if "bt-agent" in p.info["name"]:
        p.kill()
        time.sleep(3)

p = subprocess.Popen(['/usr/bin/bluetoothctl'], stdout=subprocess.PIPE, stdin=subprocess.PIPE, universal_newlines=True,
                     shell=True)
poll_obj = select.poll()
poll_obj.register(p.stdout, select.POLLIN)
p.stdin.write("power on\n")
p.stdin.flush()
p.stdin.write("discoverable on\n")
p.stdin.flush()
p.stdin.write("pairable on\n")
p.stdin.flush()
time.sleep(4)
p.terminate()

epaper.writeText(0,"Pair Now use")
epaper.writeText(1,"any passcode if")
epaper.writeText(2,"prompted.")
epaper.writeText(4,"Times out in")
epaper.writeText(5,"one minute.")


p = subprocess.Popen(['/usr/bin/bt-agent --capability=NoInputNoOutput -p /etc/bluetooth/pin.conf'],stdout=subprocess.PIPE,stdin=subprocess.PIPE,shell = True)
poll_obj = select.poll()
poll_obj.register(p.stdout, select.POLLIN)
t = time.time()
running = 1
spamyes = 0
spamtime = 0;
while time.time() - t < 60 and running == 1:
    poll_result = poll_obj.poll(0)
    if spamyes == 1:
        if time.time() - spamtime < 20:
            p.stdin.write(b'yes\n')
            time.sleep(1)
        else:
            print("terminating")
            p.terminate()
            running = 0
    if poll_result and spamyes == 0:
        line = p.stdout.readline()
        if b'Device:' in line:
            print("detected")
            p.stdin.write(b'yes\n')
            epaper.writeText(8,"Pairing")
            spamyes = 1
            spamtime = time.time()
        print(line)
    r = p.poll()
    if r is not None:
        running = 0

epaper.clearScreen()
time.sleep(3)
