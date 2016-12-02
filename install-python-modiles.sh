modules=(RPi.GPIO httplib2 google-api-python-client oauth2client Adafruit_DHT wiringpi requests)
for module in ${modules[@]}; do
    sudo pip install $module
done
