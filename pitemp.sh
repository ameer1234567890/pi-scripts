maker_key="`cat /home/pi/.maker_key`"
temp_limit=50
notify_interval=1800

last_notified_timestamp=/home/pi/pi-scripts/pitemp.log
if [ ! "$last_notified_timestamp" ]; then
  date +%s >$last_notified_timestamp
fi
time_now=$(date +%H:%M)
temp0=$(cat /sys/class/thermal/thermal_zone0/temp)
temp1=$(($temp0/1000))
temp2=$(($temp0/100))
tempM=$(($temp2 %$temp1))
temp=$temp1.$tempM

url="https://maker.ifttt.com/trigger/pitemp/with/key/$maker_key?value1=$temp"
curl $url > /dev/null 2>&1

if [ $temp1 -gt $temp_limit ]; then
  time_now=$(date +%s)
  if [ ! -f $last_notified_timestamp ]; then
    expr $(date +%s) - $notify_interval - 1 > $last_notified_timestamp
  fi
  last_notified=$(cat $last_notified_timestamp)
  after_interval=$(expr $last_notified + $notify_interval)
  if [ $time_now -gt $after_interval ];then
    url="https://maker.ifttt.com/trigger/pitemp-over/with/key/$maker_key?value1=$temp"
    curl $url > /dev/null 2>&1
    date +%s > $last_notified_timestamp
    echo "High & notify - ${temp}°C"
    exit 0
  else
    echo "High but dont notify - ${temp}°C"
    exit 1
  fi
else
  echo "Not high - ${temp}°C"
fi
