from tkinter import Tk, Canvas
from PIL import Image, ImageFont, ImageDraw, ImageTk

root = Tk()
root.title("Custom Font Example with Pillow")
root.geometry("400x240")

# Lataa mukautettu fonttitiedosto
font_path = "/home/jaakko/Lataukset/Serif/cmunorm.ttf"
custom_font = ImageFont.truetype(font_path, 20)

# Luo kuva, johon fontti piirretään
image = Image.new("RGB", (400, 240), "white")
draw = ImageDraw.Draw(image)
draw.text((10, 10), "Tervetuloa käyttämään Tkinter-ohjelmaa!", font=custom_font, fill="black")

# Näytä kuva Tkinterissä
canvas = Canvas(root, width=400, height=240)
canvas.pack()
tk_image = ImageTk.PhotoImage(image)
canvas.create_image(0, 0, anchor="nw", image=tk_image)

root.mainloop()
