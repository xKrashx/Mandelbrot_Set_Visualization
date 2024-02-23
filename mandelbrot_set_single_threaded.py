import colorsys
import tkinter as tk
import time

WIDTH = 1920

x = -0.65
y = 0
xRange = 3.4
aspectRatio = 16/9

precission = 25

HEIGHT = round(WIDTH / aspectRatio)
yRange = xRange / aspectRatio
minX = x - xRange / 2
maxY = y + yRange / 2

root = tk.Tk()
canvas = tk.Canvas(root, width = WIDTH, height = HEIGHT, bg = "black")
canvas.pack()
img = tk.PhotoImage(width = WIDTH, height = HEIGHT)
canvas.create_image((WIDTH/2, HEIGHT/2), image = img, state = "normal")

def toBase16(val: int):
    _digits = '0123456789ABCDEF'
    return '{}{}'.format(_digits[val // 16], _digits[val % 16])

def powerColor(distance, exp, const, scale):
    color = distance ** exp
    rgb = colorsys.hsv_to_rgb(const + scale * color, color, 0.5)
    return '#{}{}{}'.format(toBase16(round(rgb[0] * 255)), toBase16(round(rgb[1] * 255)), toBase16(round(rgb[2] * 255)))

def fc(z: complex, c: complex, n: int) -> int:
    if (z * z.conjugate()).real >= 4 or n == precission:
        return n
    return fc(z * z + c, c, n + 1)

def draw():
    for i in range(HEIGHT):
        for j in range(WIDTH):
            x = minX + j * xRange / WIDTH
            y = maxY - i * yRange / HEIGHT
            z = complex(x, y)
            c = complex(x, y)
            fn = fc(z, c, 0)
            color = powerColor(fn, 0.2, 0.8, 1.0)
            if fn == precission:
                img.put("black", (j, i))
            else:
                img.put(color, (j, i))

start = time.time()
draw()
print(time.time() - start)
img.write("output.png", format = "png")

root.mainloop()