from PIL import Image, ImageDraw      # PIL version 4 - http://pillow.readthedocs.io/en/4.0.x/
import imagetools

def findoffset(imageStrip, image, testing=False):
    """
    Give an imagestrip, look for the best one to represent the image
    :param imageStrip: a strip of images
    :param image: The image to find best match for
    :return: offset where the best image is located
    """
    ssx,ssy = imageStrip.size
    isx,isy = image.size
    if ssy != isy or ssy !=isx:
        print("Wrong size")
        quit()
    size = isx

    ipx = image.load()
    spx = imageStrip.load()
    chars = int(ssx/ssy)         # number of images in imageStrip
    if testing:
        print("image strip count",chars)
        print("image strip size {},{}".format(ssx,ssy))
        print("image size {},{}".format(isx,isy))

    best_ch = 0
    best_diff = -1
    for ch in range(chars):     # repeat number of strip images
        diffsum = 0
        ssx = ch * size
        for x in range(size):
            for y in range(size):
                #print("ch:{}, x:{},y:{}, ssx:{}".format(ch, x, y, ssx))
                ic = ipx[x,y]
                sc = spx[ssx+x,y]
                #print("ch:{}, x:{},y:{},ssx:{}, ic:{},cs:{}".format(ch, x, y, ssx, ic, sc))
                diff = abs(ic[0]-sc[0]) + abs(ic[1]-sc[1]) + abs(ic[2]-sc[2])
                diffsum += diff
                #print("diffsum:{}, diff:{}, ch:{}, x:{},y:{},ssx:{}, ic:{},cs:{}".
                #      format(diffsum, diff, ch, x, y, ssx, ic, sc))
        if best_diff == -1: best_diff = diffsum
        if diffsum < best_diff:
            best_diff = diffsum
            best_ch = ch
        #print("best so far :[{}/{}], best same:[{}/{}]".
        #      format(best_ch,ch,best_diff,diffsum))

    return best_ch


def createPortraitCollage(strip, inImage, testing=False, testSize=5):
    """
    Create an image which is made up of loads of other little images from the strip
    :param strip: Loads of pictures in a strip, all the same size and square
    :param inImage: The input image to convert into a collage of smaller images
    :return: The create image
    """

    # Number of occurances of letters depends on image size
    ssx, ssy = strip.size
    size = ssy
    image = inImage.copy()
    (ix,iy) = image.size
    ixf = int(ix/size)
    iyf = int(iy/size)

    # Screen position to do work on
    start_x = 0
    start_y = 0
    if testing:
        start_x = 350
        start_y = 250
        print("Image size: {},{}".format(ix,iy))
        print("Strip: images({}), Image size:[{}]".format(ssx/ssy,size))
        image.paste(strip)
        iyf = testSize
        ixf = testSize

    # Set up draw tool on image
    draw = ImageDraw.Draw(image)

    if True:
        for y in range(iyf):
            for x in range(ixf):
                #print("x/y:{}/{}".format(x,y))
                sx=x*size+start_x   # pull the section of the image
                sy=y*size+start_y
                im2 = image.crop( box=(sx,sy,sx+size,sy+size) )

                # Paste picture back on left
                if testing:
                    draw.rectangle((sx-start_x,sy-start_y+50,sx-start_x+size-1,sy-start_y+50+size-1), fill=1)
                    image.paste(im2,box=(sx-start_x,sy-start_y+50))

                # char set based 2
                os = findoffset(strip, im2, testing)
                #print("x:{}, y:{}, char offset:{}".format(sx,sy,os))
                draw.rectangle((sx,sy,sx+size-1,sy+size-1), fill=1)
                im2 = strip.crop( box=(os*size,0,os*size+size,size) )
                image.paste(im2,box=(sx,sy))
    return image


def getStrip(directory, size, recreate=False):
    """
    Create a photo strip of the files in the directory. If one already exists then use it.
    Also save the created strip into the strips directory
    :param directory:
    :param size: number of pixels per photo to add to strip
    :return: The strip
    """
    stripFile = "strips/"+directory+"_"+str(size)+".png"
    print("stripFile:{}".format(stripFile))
    if recreate==False:
        try:
            strip = Image.open(stripFile)  # get image
            return strip
        except:
            print("Let's create this strip file")

    strip = imagetools.createImageStrip(directory,size)
    strip.save(stripFile)
    return strip

# ---------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------
#               M A I N
# ---------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    strip = getStrip('images2',12)  # get image
    #strip.show()
    #quit()

    im1 = Image.open('work/lea.png')  # get image

    im2 = createPortraitCollage(strip, im1, testing=True, testSize=5)

    im2.show()
    #im2.save("im1.png")
