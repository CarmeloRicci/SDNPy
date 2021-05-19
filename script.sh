# edit your /etc/opkg/distfeeds.conf, uncomment lines 2 and 5. Run opkg update, then run opkg install nano
opkg install nano


opkg update
opkg install git git-http ca-bundle
opkg install python3
opkg install python-urllib3
opkg install python3-pip

python3 -m pip install --upgrade pip
pip3.6 install wheel
pip3.6 install pytz

opkg install python3-setuptools
opkg install python3-dev


cd /tmp
rm -rf SDNPy
git clone https://github.com/CarmeloRicci/SDNPy.git
cd SDNPy 
python3 main.py

cd /tmp
rm -rf SDNPy-SDNWiMesh
wget https://github.com/CarmeloRicci/SDNPy/archive/SDNWiMesh.zip
unzip SDNWiMesh.zip
rm SDNWiMesh.zip
cd SDNPy-SDNWiMesh
python3 main.py



opkg update

opkg install python3

opkg install python3-pip