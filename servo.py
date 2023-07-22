import serial

#НОМЕР COM ПОРТА
ser = serial.Serial('COM6', 1200)
ser.close()

image_width = 640
image_height = 480

def send_pelco_d_command(command):
    ser.write(command)


def move_camera_to_target(target_center):
    print('Moving camera to target')
    # Calculate the center of the image
    target_center = target_center[0], target_center[1]
    image_center = image_width // 2, image_height // 2
    # Calculate the difference between the target center and the image center
    dx = target_center[0] - image_center[0]
    dy = target_center[1] - image_center[1]
    print(dx, dy)
    # Determine the direction and amount of movement required
    pan_speed = 0
    tilt_speed = 0

    if abs(dx) > 10:
        pan_speed = 1 if dx > 0 else -1

    if abs(dy) > 10:
        tilt_speed = 1 if dy > 0 else -1
    # Construct the Pelco-D command
    pan_command = bytearray([0xFF, 0x01, 0x00, 0x00, 0x00, pan_speed, 0xFF])
    tilt_command = bytearray([0xFF, 0x01, 0x00, 0x00, tilt_speed, 0x00, 0xFF])

    # Send the Pelco-D commands to move the camera
    send_pelco_d_command(pan_command)
    send_pelco_d_command(tilt_command)
    print('1')
    return