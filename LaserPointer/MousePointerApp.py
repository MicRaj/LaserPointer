import pygame
import serial
import struct
from time import sleep

serialCom = serial.Serial('com7', 28800, timeout=.001)
# Colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Window Init
pygame.init()
WIN_WIDTH, WIN_HEIGHT = 1000, 600
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Mouse Track")


# pygame.display.set_icon(pygame.image.load())


def main():
    game_run = True
    pointer_x, pointer_y = 500, 500
    while game_run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif pygame.mouse.get_pressed()[0]:
                pointer_x, pointer_y = pygame.mouse.get_pos()
                pygame.mouse.set_visible(False)
                send_point(pointer_x, pointer_y)

            else:
                pygame.mouse.set_visible(True)

        WIN.fill(BLACK)

        # Draw Pointer
        pygame.draw.line(WIN, RED, (pointer_x - 10, pointer_y), (pointer_x + 10, pointer_y), 3)
        pygame.draw.line(WIN, RED, (pointer_x, pointer_y - 10), (pointer_x, pointer_y + 10), 3)

        pygame.display.update()


def send_point(x, y):
    x = translate(x, 0, WIN_WIDTH, 45, 135)
    y = translate(y, 0, WIN_HEIGHT, 60, 120)
    if 0 < x < 255 and 0 < y < 255:
        serialCom.write(struct.pack('>BB', x, y))
    # serialCom.write(y.to_bytes(1, 'big')
    # print(int(serialCom.readline()))
    # print(int(serialCom.readline()))


def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return int(rightMin + (valueScaled * rightSpan))


main()
