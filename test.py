import serial

#НОМЕР COM ПОРТА
ser = serial.Serial('COM6', 1200)
ser.close()


def send_pelco_d_command(command):
    ser.open()
    ser.write(command)

pan_command = bytearray([0xFF, 0x01, 0x00, 0x04, 0x20, 0x00, 0x44]) #

send_pelco_d_command(pan_command)