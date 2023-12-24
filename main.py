import pygame
import math
import random

def average(list):
    sum = 0
    for i in list:
        sum += i
    return sum/len(list)

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

width = 60

def generate(max_x, max_y):
    alive = []
    for i in range(10):
        alive.append((random.randint(0, max_x-60), random.randint(0, max_y-60), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

    return alive

def generate_next(max_x, max_y, R, G, B):
    alive = []
    for i in range(10):
        colors = (R + random.randint(-50, 50), G + random.randint(-50, 50), B + random.randint(-50, 50))
        for i in colors:
            while i < 0:
                i+=10
        print(colors)
        alive.append((random.randint(0, max_x-60), random.randint(0, max_y-60), colors[0], colors[1], colors[2]))

    return alive


def detect_collision(m_x, m_y, target_x, target_y):
    x_dist = abs(m_x - target_x)
    y_dist = abs(m_y - target_y)
    if(x_dist < 42 and y_dist < 42):
        return True
    return False

def new_generation(times, batch):
    times = times.sort()

batch = generate(1280, 720)
batch_copy = batch.copy()
times = []
time = 0
while running:
    time += 1
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            for i in batch_copy:
                if detect_collision(pos[0], pos[1], i[0], i[1]):
                    times.append((time, batch.index(i)))
                    batch_copy.remove(i)
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")


    if (len(batch_copy) > 0): 
        for i in batch_copy:
            pygame.draw.rect(screen, (i[2], i[3], i[4]), pygame.Rect(i[0], i[1], width, width))
    
    if(len(times) == len(batch)):
        # Generate a New Batch
        print("New Generation")
        times.sort()
        use_next_batch = []
        for i in range(7, len(times)):
            use_next_batch.append(batch[times[i][1]])
        avg_R = average([use_next_batch[0][2],use_next_batch[1][2],use_next_batch[2][2]])
        avg_G = average([use_next_batch[0][3],use_next_batch[1][3],use_next_batch[2][3]])
        avg_B = average([use_next_batch[0][4],use_next_batch[1][4],use_next_batch[2][4]])
        times.clear()
        batch.clear()
        batch_copy.clear()
        batch = generate_next(1280, 720, avg_R, avg_G, avg_B)
        batch_copy = batch.copy()

    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()