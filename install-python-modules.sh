modules=(RPi.GPIO httplib2 google-api-python-client oauth2client Adafruit_DHT wiringpi requests)
for module in ${modules[@]}; do
    sudo pip install $module
done

#vcgencmd
sudo pip install git+https://github.com/nicmcd/vcgencmd.git

#Adafruit-DHT
sudo apt-get install build-essential python-dev
git clone https://github.com/adafruit/Adafruit_Python_DHT
cd Adafruit_Python_DHT
sudo python setup.py install
cd ..
rm -rf Adafruit_Python_DHT
