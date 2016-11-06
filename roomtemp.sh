maker_key="`cat ~/.maker_key`"
temp0=$(cat /sys/bus/w1/devices/28-031663113dff/w1_slave | grep 't=' | cut -d '=' -f 2)
temp1=$(($temp0/1000))
temp2=$(($temp0/100))
tempM=$(($temp2 %$temp1))
temp=$temp1.$tempM

url="https://maker.ifttt.com/trigger/roomtemp/with/key/$maker_key?value1=$temp"
curl $url > /dev/null 2>&1
