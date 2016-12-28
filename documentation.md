#Luxtronik 2.0

This documentation is an attempt to document the meaning of data supplied to the Luxtronik webinterface.

## Connection

In order to access the data, one has to create a TCP connection to port 8889 (8888 if SW version is below 1.76) and send some magic bytes.

## Commands

There are 4 commands, each has sa slightly different data structure for either request and result.

### 3002 - set parameter

Send 4 bytes with the command, 4 bytes with the parameter number and 4 bytes with the parameter value, all big endian.

``` 0x00 0x00 0x0b 0xba 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00```

The result is 4 bytes with the command and 4 bytes with the parameter value, all big endian.

### 3003 - get parameter

Send 4 bytes with the command and 4 null bytes, all big endian.

``` 0x00 0x00 0x0b 0xbb 0x00 0x00 0x00 0x00```

The result is 4 bytes with the command and 4 bytes with number of parameters, all big endian.
Once one knows the number of parameters, this ambount of 4 byte integers can be read. 

### 3004 - get calculated

Send 4 bytes with the command and 4 null bytes, all big endian.

``` 0x00 0x00 0x0b 0xbc 0x00 0x00 0x00 0x00```

The result is 4 bytes with the command, 4 bytes for the status and 4 bytes with number of parameters, all big endian.
Once one knows the number of parameters, this ambount of 4 byte integers can be read. 

### 3005 - get visibility

Send 4 bytes with the command and 4 null bytes, all big endian.

``` 0x00 0x00 0x0b 0xbd 0x00 0x00 0x00 0x00```

The result is 4 bytes with the command and 4 bytes with number of parameters, all big endian.
Once one knows the number of parameters, this ambount of bytes can be read. 

## Meaning of the data

| Number | Internal ID | Internal Text | conversion | Notes |
|---|---|---|---|---|
