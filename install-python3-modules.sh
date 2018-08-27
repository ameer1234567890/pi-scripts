# Install build tools
sudo apt-get install build-essential python-dev libjpeg-dev libtiff5-dev libopenjp2-7-dev

modules=(RPi.GPIO httplib2 google-api-python-client oauth2client requests Pillow psutil speedtest)
for module in ${modules[@]}; do
    pip3 install $module
done

#vcgencmd
pip3 install git+https://github.com/nicmcd/vcgencmd.git

#Adafruit-DHT
git clone https://github.com/adafruit/Adafruit_Python_DHT
cd Adafruit_Python_DHT
python3 setup.py install
cd ..
rm -rf Adafruit_Python_DHT

#Adafruit-GPIO
git clone https://github.com/adafruit/Adafruit_Python_GPIO
cd Adafruit_Python_GPIO
python3 setup.py install
cd ..
rm -rf Adafruit_Python_GPIO

#Adafruit-SSD1306
git clone https://github.com/adafruit/Adafruit_Python_SSD1306
cd Adafruit_Python_SSD1306
python3 setup.py install
cd ..
rm -rf Adafruit_Python_SSD1306
