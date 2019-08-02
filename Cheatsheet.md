## Check i2c address
```
i2cdetect -y 1
```

## Check bluetooth devices

Scan for bluetooth devices
```
hcitool -i hci0 lescan 
```
Check connected devices
```
hcitool -i hci0 con
```