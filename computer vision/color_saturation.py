from SimpleCV import Color, Image

def color_sat(src_path):
    cans = Image(src_path)
    cans_cropped = cans.crop(0,800,2000,2000)

    red = cans.colorDistance(Color.RED)
    red_cropped = red.crop(0,800,2000,2000)

    coke_cropped = cans_cropped - red_cropped
    coke_bgr = str(coke_cropped.meanColor()).strip("()").replace(" ", "").split(',')
    coke_bgr_array = [float(i) for i in coke_bgr]

    blue = cans.colorDistance(Color.BLUE)
    blue_cropped = blue.crop(0,800,2000,2000)

    pepsi_cropped = cans_cropped - blue_cropped
    pepsi_bgr = str(pepsi_cropped.meanColor()).strip("()").replace(" ", "").split(',')
    pepsi_bgr_array = [float(i) for i in pepsi_bgr]

    print "Coke BGR:", coke_bgr_array
    print "Pepsi BGR:", pepsi_bgr_array

    if pepsi_bgr_array[0] > .8:
        purity = 'false'
    else:
        purity = 'true'
        
    return purity

color_sat_pure = color_sat('pepsi_test.jpg')
print color_sat_pure