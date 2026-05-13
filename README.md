Install Guidelines
wget https://github.com/martyn6000/netbox-contracts/archive/refs/tags/v1.7.tar.gz
tar -xvf v1.7.1.tar.gz
cd netbox-contracts-1.7.1
pip3 install setuptools
python setup.py install
vi /opt/netbox/netbox/netbox/configuration.py
## Add 'netbox_contracts', to the Plugins section
pip install drf-yasg
cd /opt/netbox/netbox/
python3 manage.py migrate
sudo systemctl restart netbox netbox-rq  
