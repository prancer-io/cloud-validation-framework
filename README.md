# python3 package manager is pip3, install it for the system.
sudo apt-get install python3-pip
# Will require the python mongo client library for interaction
sudo pip3 install pymongo
# Will use requests library for http and https
sudo pip3 install requests.

Mongo DB version used - 3.2.21 , can be upgraded to 3.4.18 or even ater 3.6.9. The latest current release is 4.0.4
Upgrade to 4.0.4 version and check the basic connections and query APIs.

TODO - Version selection and features involved.

cd $HOME/projects/upwork/liquware/whitekite
export PYTHONPATH=`pwd`:$PYTHONPATH
echo $PYTHONPATH

python3 validator.py container1
