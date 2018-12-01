from PIL import Image

im = Image.open('assets/taco.png')
base = Image.new("RGB", (800,800), "white")

base.paste(im)
base.show()
