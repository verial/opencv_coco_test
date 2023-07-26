# BYTE_ARRAYS = {
#     (-1, -1): [0xFF, 0x01, 0x00, 0x14, 0x05, 0x00, 0x1A],  # DOWN LEFT
#     (1, 1): [0xFF, 0x01, 0x00, 0x0C, 0x05, 0x00, 0x12],  # UP LEFT
#     (1, -1): [0xFF, 0x01, 0x00, 0x12, 0x05, 0x00, 0x18],  # DOWN RIGHT
#     (-1, 1): [0xFF, 0x01, 0x00, 0x04, 0x05, 0x00, 0x0A],  # UP RIGHT
#     (0, -1): [0xFF, 0x01, 0x00, 0x10, 0x05, 0x00, 0x16],  # Down
#     (0, 1): [0xFF, 0x01, 0x00, 0x08, 0x05, 0x00, 0x0E],  # Up
#     (-1, 0): [0xFF, 0x01, 0x00, 0x02, 0x05, 0x00, 0x08],  # Right
#     (1, 0): [0xFF, 0x01, 0x00, 0x04, 0x05, 0x00, 0x0A],  # Left
# }


def move_camera_to_target(dx, dy):
    # Determine the direction and amount of movement required
    if dx == None and dy == None:
        return bytearray([0xFF, 0x01, 0x00, 0x0F, 0x00, 0x00, 0xF0])
    if (dx <= 7 and dx >= -7) and (dy <= 7 and dy >= -7):
        return bytearray([0xFF, 0x01, 0x00, 0x00, 0x00, 0x00, 0x01])

    # if dx != 0:
    #     dx = dx // abs(dx)
    # if dy != 0:
    #     dy = dy // abs(dy)

    if dx < -7: # - право
        command = bytearray([0xFF, 0x01, 0x00, 0x02, 0x07, 0x00, 0x0A])

    if dx > 7: # + лево
        command = bytearray([0xFF, 0x01, 0x00, 0x04, 0x07, 0x00, 0x1C])

    if dy < -7: # - вниз
        command = bytearray([0xFF, 0x01, 0x00, 0x10, 0x07, 0x00, 0x18])

    if dy > 7: # + вверх
        command = bytearray([0xFF, 0x01, 0x00, 0x08, 0x07, 0x00, 0x10])

    # direction = (dx, dy)
    return command
