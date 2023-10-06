# FW UPS Pack V3 - Remote usage

## Copy sources to remote machine
1. Connect and create dir into remote machine
  ```shell
  $ ssh pi@raspberrypi.local
  (rpi)$ mkdir -p dev/fw_ups
  (rpi)$ exit
  ```
2. Copy local sources to remote machine
  ```shell
  $ rsync -av --exclude venv --exclude logs --exclude __pycache__ --exclude .git -e ssh * pi@raspberrypi.local:/home/pi/dev/fw_ups
  ```


## Prepare remote machine (only once)
1. Connect to remote machine
  ```shell
  $ ssh pi@raspberrypi.local
  ```
2. Install requirements (only once)
  ```shell
  (rpi)$ sudo apt-get install python3 libcairo2-dev libgirepository1.0-dev dbus-x11
  ```
3. Install python's requirements (only once)
  ```shell
  (rpi)$ cd dev/fw_ups
  (rpi)$ python -m venv venv           # Optional: only for venv support
  (rpi)$ source venv/bin/activate      # Optional: only for venv support
  (rpi-venv)$ pip install -R requirements.txt
  ```


## Run on remote machine
1. Connect to remote machine and cd to firmware dir
  ```shell
  $ ssh pi@raspberrypi.local
  (rpi)$ cd dev/fw_ups
  ```
2. Init DBus session (only if required)
  ```shell
  (rpi)$ env | grep DBUS_SESSION_BUS_ADDRESS
  # no response means the DBus session is required
  (rpi)$ exec dbus-run-session -- bash
  (rpi)$ env | grep DBUS_SESSION_BUS_ADDRESS
  # copy the printed output as DBUS Session
  ```
3. Activate the venv (if required)
  ```shell
  (rpi)$ source venv/bin/activate
  ```
4. Run the Python script
  ```shell
  (rpi)$ python run.py
  ```


## Monitor DBus from 2nd shell
1. Connect to remote machine with another shell
  ```shell
  $ ssh pi@raspberrypi.local
  ```
2. Set DBus session, using the value copied after his creation
  ```shell
  (rpi2)$ export DBUS_SESSION_BUS_ADDRESS=unix:path=/tmp/dbus-Qzp4nPaFAr,guid=88e4d61b4af3628519f04ede651e6f7f
  ```
3. Start the dbus monitor
  ```shell
  (rpi2)$ dbus-monitor
  ```


## Configure SSH keys to avoid password usage
1. Create a 'public_keys' on the remote machine
  ```shell
  $ ssh pi@raspberrypi.local
  (rpi)$ mkdir -p .ssh/public_keys
  (rpi)$ exit
  ```
2. Generate a new key pair and copy the public one on the remote machine
  ```shell
  $ ssh-keygen -t rsa
  #  save it in /home/USER/.ssh/id_rsa_for_rpi
  $ scp /home/USER/.ssh/id_rsa_for_rpi.pub pi@raspberrypi.local:/home/pi/.ssh/public_keys
  ```
3. Setup the new public key into remote machine
  ```shell
  $ ssh pi@raspberrypi.local
  (rpi)$ cat .ssh/pub_keys/id_rsa_for_rpi.pub >> .ssh/authorized_keys
  ```
