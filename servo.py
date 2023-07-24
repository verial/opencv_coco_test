import serial
from pelcod import PelcoDevice

p = PelcoDevice(port='COM6', baudrate=1200, timeout_=0)
#НОМЕР COM ПОРТА
# ser = serial.Serial('COM6', 1200)
# ser.close()

image_width = 640
image_height = 480

# def send_pelco_d_command(command):
#     # ser.open()
#     # ser.write(command)
#     print(command)

def move_camera_to_target(target_center):
    # Calculate the center of the image
    target_center = target_center[0], target_center[1]
    image_center = image_width // 2, image_height // 2
    # Calculate the difference between the target center and the image center
    dx = target_center[0] - image_center[0]
    dy = target_center[1] - image_center[1]
    # Determine the direction and amount of movement required
    # pan_command = bytearray([])
    # tilt_command = bytearray([])

    if dx == 0 and dy == 0:
        print('Nice')
        return

    if dx < 0: # - лево
        p.move_by_step('LEFT', 0.01)

    if dx > 0: # + право
        p.move_by_step('RIGHT', 0.01)

    if dy < 0: # + верх
        p.move_by_step('UP', 0.01)

    if dy > 0: # - вниз
        p.move_by_step('DOWN', 0.01)
    return