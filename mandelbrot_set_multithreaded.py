import time
from threading import Thread
import multiprocessing
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor

WIDTH = 640

scale = 1
cenX = 0
cenY = 0

x = 0
y = 0
aspectRatio = 16/9

precission = 200

HEIGHT = round(WIDTH / aspectRatio)

_thread_count = multiprocessing.cpu_count()
colomnsPerThread = round(WIDTH / _thread_count)

img = np.full((HEIGHT, WIDTH), 255)

def fc(z: complex, c: complex, n: int) -> int:
    if (z*z.conjugate()).real >= 4 or n == precission:
        return n
    return fc(z*z + c, c, n + 1)

def draw(start: int, end: int):
    global x, y, scale
    for i in range(HEIGHT):
        for j in range(start, end):
            x = (j - WIDTH / 2) * 4 / WIDTH * aspectRatio / scale + cenX
            y = (i - HEIGHT / 2) * 4 / HEIGHT / scale + cenY
            z = complex(x, y)
            c = complex(x, y)
            img[i][j] = precission - fc(z, c, 0)

fig, ax = plt.subplots()
obj = ax.imshow(img)
plt.axis('off')

def startThreads():
    start = time.time()
    threads = [ Thread(target=draw, args=(i * colomnsPerThread, (i + 1) * colomnsPerThread)) for i in range(_thread_count) ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    print(time.time() - start)
    plt.imshow(img, cmap='plasma')
    plt.show()

def onclick(event):
    global scale, fig
    if event.button == 'up':
        scale -= scale * 0.5
        print('zoom out')
    else:
        scale += scale * 0.5
        print('zoom in')
    startThreads()
    
def onKeyPress(event):
    global cenX, cenY
    print(event.key)
    if event.key == 'right':
        cenX += 0.5 / scale
    if event.key == 'left':
        cenX -= 0.5 / scale
    if event.key == 'up':
        cenY -= 0.5 / scale
    if event.key == 'down':
        cenY += 0.5 / scale
    startThreads()

zoom = fig.canvas.mpl_connect('scroll_event', onclick)
move = fig.canvas.mpl_connect('key_press_event', onKeyPress)

startThreads()

plt.imsave('{}x{}.png'.format(WIDTH, HEIGHT), img)