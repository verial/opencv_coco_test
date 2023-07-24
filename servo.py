import serial

#НОМЕР COM ПОРТА
ser = serial.Serial('COM1', 1200)
ser.close()

image_width = 640
image_height = 480

def send_pelco_d_command(command):
    ser.open()
    ser.write(command)
    ser.close()

def move_camera_to_target(target_center):
    # Calculate the center of the image
    target_center = target_center[0], target_center[1]
    image_center = image_width // 2, image_height // 2
    # Calculate the difference between the target center and the image center
    dx = target_center[0] - image_center[0]
    dy = target_center[1] - image_center[1]
    # Determine the direction and amount of movement required
    pan_command = bytearray([0xFF, 0x01, 0x00, 0x04, 0x3F, 0x00])
    tilt_command = bytearray([0xFF, 0x01, 0x00, 0x08, 0x00, 0x3F])

    if dx == 0 and dy == 0:
        return

    if dx < 0:
        pan_command = bytearray([0xFF, 0x01, 0x00, 0x04, 0x3F, 0x00, 0x44])

    if dx > 0:
        pan_command = bytearray([0xFF, 0x01, 0x00, 0x02, 0x20, 0x00, 0x23])

    if dy < 0:
        tilt_command = bytearray([0xFF, 0x01, 0x00, 0x08, 0x00, 0x3F, 0x48])

    if dy > 0:
        tilt_command = bytearray([0xFF, 0x01, 0x00, 0x10, 0x20, 0x00, 0x31])

    send_pelco_d_command(pan_command)
    send_pelco_d_command(tilt_command)
    return