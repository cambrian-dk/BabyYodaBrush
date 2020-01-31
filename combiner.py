from PIL import Image

for i in range(1, 88):
    try:
        jpeg = Image.open(str(i) + ".jpg")
        png = Image.open(str(i) + ".png")
    except:
        continue
    convertedpng = png.convert('RGB')
    targetwidth = jpeg.size[0]
    targetheight = jpeg.size[1]
    resizedpng = convertedpng.resize((targetwidth, targetheight), Image.ANTIALIAS)
    newwidth = resizedpng.size[0] + jpeg.size[0]
    newheight = resizedpng.size[1]
    new_img = Image.new('RGB', (newwidth, newheight))
    new_img.paste(resizedpng,(0, 0))
    new_img.paste(jpeg, (resizedpng.size[0], 0))
    new_img.save(str(i) + 'combined.jpg')
    
