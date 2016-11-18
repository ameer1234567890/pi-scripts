maker_key="`cat /home/pi/.maker_key`"
i=0
while [ ! $ping ]; do
  i=$((i+1))
  if [ $i -gt 4 ]; then
    exit 2
  fi
  file="/home/pi/pi-scripts/speedtest.log"
  speedtest --simple > $file
  ping=`cat $file | grep Ping | cut -d " " -f 2`
  download=`cat $file | grep Download | cut -d " " -f 2`
  upload=`cat $file | grep Upload | cut -d " " -f 2`
  if [ $ping ]; then
    url="https://maker.ifttt.com/trigger/speedtest/with/key/$maker_key?value1=$ping&value2=$download&value3=$upload"
    curl $url
  fi
done
