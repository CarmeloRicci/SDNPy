import serial
# Init buffer containing the received data
buffSize = 3
inBuff = [bytes(0)] * buffSize
pos = 0

done = False
messRCV = False
sampleSizeRCV = False
audioSample = []


# Create serial object
ser = serial.Serial('/dev/ttyUSB1', baudrate=12000000,rtscts=True,dsrdtr=True, timeout=0.1)
# Open serial

try:
    ser.open()
except:
    print("gia aperta")

# Start looking for the message
while done == False:
    messRCV = False
    strVal = ser.read(1)

    if strVal == ('<').encode():
        while not messRCV:
            # If message found or buff is full stop reading and save sample

            if pos == buffSize:  # and val == ('\r').encode():

                audioSample.append(int.from_bytes(inBuff[0] + inBuff[1] + inBuff[2], "big", signed="True"))
                print(len(audioSample))
                messRCV = True
                pos = 0
                inBuff = [bytes(0)] * buffSize

                # ser.reset_output_buffer()
            else:
                val = ser.read(1)
                inBuff[pos] = bytes(val)
                pos = pos + 1

