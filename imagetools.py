from PIL import Image,ImageFont, ImageDraw       # PIL version 4 - http://pillow.readthedocs.io/en/4.0.x/
import os, PIL

font = ImageFont.load_default()  # all chars sizes are 6,11
cs_font_x, cs_font_y = font.getsize(" ")
font_x = cs_font_x-1
font_y = cs_font_y-2


def createCharacterSetImage():
    # Create an image of all the chars, with rever as well
    ch_st = 32
    ch_end = 127
    w = (ch_end-ch_st) * font_x
    h = font_y
    im1cs = Image.new("1", (w,h), color=1)
    drawcs = ImageDraw.Draw(im1cs)

    for ch in range(ch_st,ch_end):
        x = (ch-ch_st) * font_x
        drawcs.text((x, -2), chr(ch), font=font)

    # replace dark pixels with black
    im2cs = Image.eval(im1cs, lambda px: 255 if px == 0 else 0)
    im3cs = Image.eval(im2cs, lambda px: 255 if px == 0 else 0)

    imcs = Image.new("1", (w*2,h), color=1)
    imcs.paste(im3cs,box=(0,0))
    imcs.paste(im2cs,box=(w,0))

    return imcs


def createImageStrip(directory, imageSize):
    """
    From a directory pull in all images and convert to one long image of a given size
    All imagines added will be square.
    The total number of images will be the high divided by length.
    :param directory: where to pull the images from
    :param imageSize: the size of each image on the strip
    :return: the resulting image strip
    """
    imageFiles = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    print(imageFiles)

    w = imageSize * len(imageFiles)
    h = imageSize
    image = PIL.Image.new("RGB", (w, h))

    for i in range(len(imageFiles)):
        imageFile = directory + "/" + imageFiles[i]
        print("Add {} named {}".format(i,imageFile))
        toAddImage = PIL.Image.open(imageFile).resize((imageSize,imageSize))
        image.paste(toAddImage, box=(i*imageSize, 0))
    return image

def splitImage(folder, image, x_images, y_images):
    """
    Split an image and store the resulting images into the folder
    :param folder: Where the images should be stored
    :param image: The initial image to break up
    :param x: The number of images in the x direction
    :param y: The number of images in the y direction
    :return: nothing
    """

    # Number of occurrances of letters depends on image size
    (ix,iy) = image.size
    ixf = int(ix/x_images)
    iyf = int(iy/y_images)

    outDirectory = "{}_split".format(folder)
    if not os.path.exists(outDirectory): os.makedirs(outDirectory)

    for y in range(y_images):
        for x in range(x_images):
            sx = x * ixf
            sy = y * iyf
            slice = image.crop(box=(sx, sy, sx+ixf-1, sy+iyf-1))
            fileName = "{}/image_x{}_y{}.png".format(outDirectory, x, y)
            slice.save(fileName)



def getColor(image):
    """
    Get the average color across the whole image
    :param image:
    :return: average color across image
    """
    isx,isy = image.size
    ipx = image.load()
    total = [0,0,0,0]

    for x in range(isx):
        for y in range(isy):
            color = ipx[x,y]
            #print("Color:{}".format(color))
            for i in range(len(color)):  # loop over color at pixel
                total[i] += color[i]
            #print("total:{}, added:{}".format(total,color))

    pixels = isx*isy
    for i in range(len(total)):  # loop over color at pixel
        total[i] = int(total[i]/pixels)
    if len(color)==3: outColor = (total[0], total[1], total[2])
    else: outColor = (total[0], total[1], total[2], total[3])
    #print("Out color:{}".format(color))

    return color


def setColor(image, color, box):
    """
    Set the background color of part of an image
    :param image: The image to alter
    :param color: The color to set the image
    :param box: The area to alter
    :return:
    """
    (xs, ys, xe, ye) = box
    (ix,iy) = image.size
    ipx = image.load()
    for x in range(xs,xe+1):
        for y in range(ys,ye+1):
            if x<ix and y<iy:
                if ipx[x,y][0]>0: ipx[x,y] = color

def findoffset(character_set, image):
    """
    Give a character set, look for the best character to represent the image
    :param character_set:
    :param image:
    :return: offset where the best char is located
    """
    csx, csy = character_set.size
    isx, isy = image.size

    ipx = image.load()
    cspx = character_set.load()
    chars = int(csx / font_x)  # number of characters in impage
    # print("chars",chars)
    # print("char set size {},{}".format(csx,csy))
    # print("image size {},{}".format(isx,isy))

    best_ch = -1
    best_sames = -1
    for ch in range(chars):
        same = 0
        csx = ch * font_x
        for x in range(font_x):
            for y in range(font_y):
                try:
                    ic = ic1 = ipx[x, y][0]
                except:
                    ic = ic1 = ipx[x, y]
                csc = csc1 = cspx[csx + x, y]
                if ic == 255:  ic = 1
                if csc == 255: csc = 1
                # print("ch:{}, x:{},y:{},csx:{}, ic:{}/{},cs:{}/{}".format(ch,x,y,csx,ic,ic1,csc,csc1))
                if ic == csc: same += 1
        if same > best_sames:
            best_sames = same
            best_ch = ch
            # print("best so far char:[{}/{}], best same:[{}]".format(best_ch,ch,best_sames,same))

    return best_ch

# ---------------------------------------------------------------------------------------------------------
#               M A I N
# ---------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    directory = "photos/cards_split"
    size = 100
    image = createImageStrip(directory, size)
    image.show()
    saveName = "{}{}.png".format(directory,size)
    image.save(saveName)

    # Split an image
    # image = PIL.Image.open('photos/cards/deck.png')
    # splitImage("photos/cards",image,13,4)