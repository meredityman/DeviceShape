## Check i2c address
```
i2cdetect -y 1
```

## Check bluetooth devices

Scan for bluetooth devices
```
sudo hcitool -i hci0 lescan 
```
Check connected devices
```
sudo hcitool -i hci0 con
```


## Audio recording
```
alsamixer -c 0
```