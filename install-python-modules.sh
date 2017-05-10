modules=(RPi.GPIO httplib2 google-api-python-client oauth2client requests Pillow psutil)
for module in ${modules[@]}; do
    sudo pip install $module
done

#vcgencmd
sudo pip install git+https://github.com/nicmcd/vcgencmd.git

# Install build tools
sudo apt-get install build-essential python-dev

#Adafruit-DHT
git clone https://github.com/adafruit/Adafruit_Python_DHT
cd Adafruit_Python_DHT
sudo python setup.py install
cd ..
sudo rm -rf Adafruit_Python_DHT

#Adafruit-GPIO
git clone https://github.com/adafruit/Adafruit_Python_GPIO
cd Adafruit_Python_GPIO
sudo python setup.py install
cd ..
sudo rm -rf Adafruit_Python_GPIO

#Adafruit-SSD1306
git clone https://github.com/adafruit/Adafruit_Python_SSD1306
cd Adafruit_Python_SSD1306
sudo python setup.py install
cd ..
sudo rm -rf Adafruit_Python_SSD1306
