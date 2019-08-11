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

```
sudo hciconfig hci0 down
sudo hciconfig hci0 up
```


## Audio recording
```
alsamixer -c 0
```