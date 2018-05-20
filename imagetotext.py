import os, PIL
import imagetools

def createSymbilPhoto(image, color=False, testing=False, testSize=3):
    # Number of occurrances of letters depends on image size
    font_x = imagetools.font_x
    font_y = imagetools.font_y
    (ix,iy) = image.size
    ixf = int(ix/font_x)
    iyf = int(iy/font_y)
    start_x = start_y = 0    # Screen position to do work on

    # Set up the character set stuff
    im_cs = imagetools.createCharacterSetImage()
    csix, csiy = im_cs.size

    imnew = image.crop(box=(0,0,ixf*font_x,iyf*font_y))        # copy image so original is not changed
    imbw = image.convert("1")   # convert to black and white

    if testing:
        start_x, start_y = 100, 100
        ixf,iyf  = testSize, testSize
        print("Image size: {},{}".format(ix, iy))
        print("CharacterSet: Image size:[{}/{}]".format(csix, csiy))
        print("Font size {}/{}".format(font_x, font_y))
        imnew.paste(im_cs)

    # Set up draw tool on image
    draw = PIL.ImageDraw.Draw(imnew)

    if True:
        for y in range(iyf):
            for x in range(ixf):
                sx=x*font_x+start_x
                sy=y*font_y+start_y
                imboxbw = imbw.crop( box=(sx,sy,sx+font_x,sy+font_y) )


                # Paste pcture back on left
                if testing:
                    draw.rectangle( (sx-start_x,sy-start_y+50,sx-start_x+font_x-1, sy-start_y+50+font_y-1), fill=1)
                    imnew.paste(imboxbw,box=(sx-start_x,sy-start_y+50))

                # char set based 2
                os = imagetools.findoffset(im_cs,imboxbw)
                #print("x:{}, y:{}, char offset:{}, color:{}".format(sx,sy,os,color))
                draw.rectangle((sx,sy,sx+font_x-1,sy+font_y-1), fill=1)
                imsym = im_cs.crop( box=(os*font_x,0,os*font_x+font_x,font_y) )
                imnew.paste(imsym,box=(sx,sy))
                if color:
                    imbox = image.crop(box=(sx, sy, sx + font_x, sy + font_y))
                    boxcolor = imagetools.getColor(imbox)
                    imagetools.setColor(imnew,boxcolor,((sx,sy,sx+font_x-1,sy+font_y-1)))
    return imnew

def createSymbilPhotoDirectory(inDirectory, color=False, testing=False, testSize=3):
    """
    create new symbol images from photos found in folder.
    :param directory: where to pull the images from
    :return:
    """

    imageFiles = [f for f in os.listdir(inDirectory) if os.path.isfile(os.path.join(inDirectory, f))]
    print(imageFiles)
    if color: outDirectory = inDirectory + "_sym_col"
    else:     outDirectory = inDirectory + "_sym_bw"
    if not os.path.exists(outDirectory): os.makedirs(outDirectory)

    for i in range(len(imageFiles)):
        imageInFile  = inDirectory  + "/" + imageFiles[i]
        imageOutFile = outDirectory + "/" + imageFiles[i]
        print("Add {} named {}".format(i, imageOutFile))
        inImage  = PIL.Image.open(imageInFile)
        outImage = createSymbilPhoto(inImage, color, testing, testSize)
        #outImage.show()
        outImage.save(imageOutFile)


# ---------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------
#               M A I N
# ---------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    #im0 = Image.open('gn800x800.png')      # get image
    #im0 = Image.open('gas.png')            # get image
    #im0 = Image.open('g.png')              # get image
    #im0 = Image.open('images/j1.png')      # get image
    #im0 = Image.open('work/group.png')     # get image
    im0 = PIL.Image.open('cats/download.jpg')   # small
    #im0 = Image.open('p2.png')             # get image

    im1 = createSymbilPhoto(im0, testing=False, testSize=1)

    im1.show()
    #im1.save("im1.png")

    #createSymbilPhotoDirectory("team", color=False)
    #createSymbilPhotoDirectory("team", color=True)

