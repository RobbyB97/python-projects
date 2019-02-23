"""
    Author: Robert Bergers
    Credit: https://code.tutsplus.com/tutorials/
        how-to-build-a-python-bot-that-can-play-web-games--active-11117
        *Converted to different version of Python, used different libraries
    School assignment: Bot that automatically plays sushi-go-round
    First real exposure to Python
"""


import win32api #Used to control mouse and keyboard.
import win32con #Used to control mouse and keyboard.
import pyscreenshot as ImageGrab #Allows bot to take screenshots
import pyscreenshot as ImageOps #Allows bot to pull information from screenshots
from PIL import ImageOps #Allows bot to pull information from screenshots
import pydoc
import os
import time #Used to time bot's actions
from numpy import * #Access to numpy classes
import numpy

class Resources:
    """
    Dictionaries used to keep track of ingredients when they are used or bought.
    """

foodOnHand = {
    'shrimp': 5,
    'rice': 10,
    'nori': 10,
    'fishegg': 10,
    'salmon': 5,
    'unagi': 5
    }

foodCaliroll = {'shrimp': 0,
                'rice': 2,
                'nori': 1,
                'fishegg': 1,
                'salmon': 0,
                'unagi': 0}

foodGunkan = {'shrimp': 0,
              'rice': 1,
              'nori': 1,
              'fishegg': 2,
              'salmon': 0,
              'unagi': 0}

foodOnigiri = {'shrimp': 0,
               'rice': 2,
               'nori': 1,
               'fishegg': 1,
               'salmon': 0,
               'unagi': 0}

foodBuyShrimp = {'shrimp': 10,
                 'rice': 0,
                 'nori': 0,
                 'fishegg': 0,
                 'salmon': 0,
                 'unagi': 0}

foodBuyRice = {'shrimp': 0,
               'rice': 10,
               'nori': 0,
               'fishegg': 0,
               'salmon': 0,
               'unagi': 0}

foodBuyNori = {'shrimp': 0,
               'rice': 0,
               'nori': 10,
               'fishegg': 0,
               'salmon': 0,
               'unagi': 0}

foodBuyFishegg = {'shrimp': 0,
                  'rice': 0,
                  'nori': 0,
                  'fishegg': 10,
                  'salmon': 0,
                  'unagi': 0}

foodBuySalmon = {'shrimp': 0,
                 'rice': 0,
                 'nori': 0,
                 'fishegg': 0,
                 'salmon': 10,
                 'unagi': 0}

foodBuyUnagi = {'shrimp': 0,
                'rice': 0,
                'nori': 0,
                'fishegg': 0,
                'salmon': 0,
                'unagi': 10}


class Sums:
    """
    The pixel sums for each type of food from each seat in the game.
    checkFood() compares a pixel sum to the values in these dictionaries.
    """

sushiTypeOne = {
    'Onigiri': 2173,
    'Caliroll': 2557,
    'Gunkan': 2227
    }

sushiTypeTwo = {
    'Onigiri': 2109,
    'Caliroll': 2303,
    'Gunkan': 1973
    }

sushiTypeThree = {
    'Onigiri': 5916,
    'Caliroll': 6300,
    'Gunkan': 5970
    }

sushiTypeFour = {
    'Onigiri': 2237,
    'Caliroll': 2430,
    'Gunkan': 2100
    }

sushiTypeFive = {
    'Onigiri': 2173,
    'Caliroll': 2557,
    'Gunkan': 2227
    }

sushiTypeSix = {
    'Onigiri': 2109,
    'Caliroll': 2303,
    'Gunkan': 1973
    }

class Cord:
    """
    Coordinates on the screen for different
    items the bot has to click on to play the game.
    """

    f_shrimp = (30, 307)
    f_rice = (88, 312)
    f_nori = (35, 361)
    f_fishegg = (103, 341)
    f_salmon = (42, 409)
    f_unagi = (80, 417)

    phone = (558, 319)

    menu_toppings = (542, 241)
    t_shrimp = (482, 181)
    t_unagi = (581, 187)
    t_nori = (499, 249)
    t_fishegg = (578, 239)
    t_salmon = (492, 284)
    t_exit = (585, 309)

    menu_rice = (491, 264)
    buy_rice = (550, 268)

    menu_sake = (509, 281)
    buy_sake = (550, 268)

    sake_rice_exit = (572, 307)

    d_normal = (486, 261)
    d_express = (577, 265)
    d_exit = (574, 312)


class Blank:
    """
    These are the pixel sums of each seat without a bubble,
    letting the program know there is no request at that seat.
    """
    seat_1 = 17258
    seat_2 = 16546
    seat_3 = 1462
    seat_4 = 24838
    seat_5 = 16888
    seat_6 = 11078


def check_bubs():
    """ Logic for clearing tables and checking for orders.

    Uses get_seat_one - get_seat_six methods, checking the state of the sushiTypeOne - sushiTypeSix
    classes.
    If they equal one of the food types, that food is sent to makeFood()
    If not, the table is cleared and the next seat is checked in an infinite loop.

    :return:
    """
    checkFood()
    s1 = get_seat_one()
    if s1 == sushiTypeOne['Onigiri'] or s1 == sushiTypeOne['Caliroll'] or s1 == sushiTypeOne['Gunkan']:
        if sushiTypeOne.has_key(s1):
            if s1 == sushiTypeOne['Onigiri']:
                makeFood('onigiri')
            elif s1 == sushiTypeOne['Caliroll']:
                makeFood('caliroll')
            elif s1 == sushiTypeOne['Gunkan']:
                makeFood('gunkan')
        else:
            print 'sushi not found!\n sushiType = %i' % s1
    else:
        print 'Table 1 unoccupied'

    clear_tables()
    checkFood()
    s2 = get_seat_two()
    if s2 != Blank.seat_2:
        if s2 == sushiTypeTwo['Onigiri'] or s2 == sushiTypeTwo['Caliroll'] or s2 == sushiTypeTwo['Gunkan']:
            if s2 == sushiTypeTwo['Onigiri']:
                makeFood('onigiri')
            elif s2 == sushiTypeTwo['Caliroll']:
                makeFood('caliroll')
            elif s2 == sushiTypeTwo['Gunkan']:
                makeFood('gunkan')
        else:
            print 'sushi not found!\n sushiType = %i' % s2

    else:
        print 'Table 2 unoccupied'

    checkFood()
    s3 = get_seat_three()
    if s3 == sushiTypeThree['Onigiri'] or s3 == sushiTypeThree['Caliroll'] or s3 == sushiTypeThree['Gunkan']:
        if sushiTypeThree.has_key(s3):
            if s3 == sushiTypeThree['Onigiri']:
                makeFood('onigiri')
            elif s3 == sushiTypeThree['Caliroll']:
                makeFood('caliroll')
            elif s3 == sushiTypeThree['Gunkan']:
                makeFood('gunkan')
        else:
            print 'sushi not found!\n sushiType = %i' % s3

    else:
        print 'Table 3 unoccupied'

    checkFood()
    s4 = get_seat_four()
    if s4 == sushiTypeFour['Onigiri'] or s4 == sushiTypeFour['Caliroll'] or s4 == sushiTypeFour['Gunkan']:
        if sushiTypeFour.has_key(s4):
            if s4 == sushiTypeFour['Onigiri']:
                makeFood('onigiri')
            elif s4 == sushiTypeFour['Caliroll']:
                makeFood('caliroll')
            elif s4 == sushiTypeFour['Gunkan']:
                makeFood('gunkan')
        else:
            print 'sushi not found!\n sushiType = %i' % s4

    else:
        print 'Table 4 unoccupied'

    clear_tables()
    checkFood()
    s5 = get_seat_five()
    if s5 == sushiTypeFive['Onigiri'] or s5 == sushiTypeFive['Caliroll'] or s5 == sushiTypeFive['Gunkan']:
        if sushiTypeFive.has_key(s5):
            if s5 == sushiTypeFive['Onigiri']:
                makeFood('onigiri')
            elif s5 == sushiTypeFive['Caliroll']:
                makeFood('caliroll')
            elif s5 == sushiTypeFive['Gunkan']:
                makeFood('gunkan')
        else:
            print 'sushi not found!\n sushiType = %i' % s5

    else:
        print 'Table 5 unoccupied'

    checkFood()
    s6 = get_seat_six()
    if s6 != Blank.seat_6:
        if s6 == sushiTypeSix['Onigiri'] or s6 == sushiTypeSix['Caliroll'] or s6 == sushiTypeSix['Gunkan']:
            if s6 == sushiTypeSix['Onigiri']:
                makeFood('onigiri')
            elif s6 == sushiTypeSix['Caliroll']:
                makeFood('caliroll')
            elif s6 == sushiTypeSix['Gunkan']:
                makeFood('gunkan')
        else:
            print 'sushi not found!\n sushiType = %i' % s6

    else:
        print 'Table 6 unoccupied'

    clear_tables()


def buyFood(food):
    """Buys food

    This method takes argument food from the foodOnHand dictionary and performs the
    necessary mouse movements to buy that ingredient in the game.
    The foodOnHand value is increased by 10 and returned.

    :param food:
    :return:
    """
    if food == 'rice':
        mousePos(Cord.phone)
        time.sleep(.1)
        leftClick()
        mousePos(Cord.menu_rice)
        s = screenGrab()
        if s.getpixel(Cord.buy_rice) != (153, 157, 57):
            print 'rice is available'
            mousePos(Cord.buy_rice)
            time.sleep(.1)
            leftClick()
            mousePos(Cord.d_normal)
            foodOnHand['rice'] += 10
            time.sleep(.1)
            leftClick()
            time.sleep(2.5)
            return foodOnHand['rice']
        else:
            print 'rice is NOT available'
            mousePos(Cord.t_exit)
            leftClick()
            time.sleep(1)
            buyFood(food)
    if food == 'nori':
        mousePos(Cord.phone)
        time.sleep(.1)
        leftClick()
        mousePos(Cord.menu_toppings)
        s = screenGrab()
        if s.getpixel(Cord.t_nori) != (238, 219, 169):
            print 'nori is available'
            mousePos(Cord.t_nori)
            time.sleep(.1)
            leftClick()
            mousePos(Cord.d_normal)
            foodOnHand['nori'] += 10
            time.sleep(.1)
            leftClick()
            time.sleep(2.5)
            return foodOnHand['nori']
        else:
            print 'nori is NOT available'
            mousePos(Cord.t_exit)
            leftClick()
            time.sleep(1)
            buyFood(food)
    if food == 'fishegg':
        mousePos(Cord.phone)
        time.sleep(.1)
        leftClick()
        mousePos(Cord.menu_toppings)
        time.sleep(.05)
        leftClick()
        s = screenGrab()
        time.sleep(.1)
        if s.getpixel(Cord.t_fishegg) != (255, 250, 208):
            print 'fishegg is available'
            mousePos(Cord.t_fishegg)
            time.sleep(.1)
            leftClick()
            mousePos(Cord.d_normal)
            foodOnHand['fishegg'] += 10
            time.sleep(.1)
            leftClick()
            time.sleep(2.5)
            return foodOnHand['fishegg']
        else:
            print 'fishegg is NOT available'
            mousePos(Cord.t_exit)
            leftClick()
            time.sleep(1)
            buyFood(food)
    if food == 'shrimp':
        mousePos(Cord.phone)
        time.sleep(.1)
        leftClick()
        mousePos(Cord.menu_toppings)
        time.sleep(0.5)
        leftClick()
        s = screenGrab()
        time.sleep(.1)
        if s.getpixel(Cord.t_shrimp) != (100, 66, 59):
            print 'shrimp is available'
            mousePos(Cord.t_shrimp)
            time.sleep(.1)
            leftClick()
            mousePos(Cord.d_normal)
            foodOnHand['shrimp'] += 10
            time.sleep(.1)
            leftClick()
            time.sleep(2.5)
            return foodOnHand['shrimp']
        else:
            print 'shrimp is NOT available'
            mousePos(Cord.t_exit)
            leftClick()
            time.sleep(1)
            buyFood(food)
    if food == 'salmon':
        mousePos(Cord.phone)
        time.sleep(.1)
        leftClick()
        mousePos(Cord.menu_toppings)
        time.sleep(.5)
        leftClick()
        s = screenGrab()
        time.sleep(.1)
        if s.getpixel(Cord.t_salmon) != (238, 219, 169):
            print 'salmon is available'
            mousePos(Cord.t_salmon)
            time.sleep(.1)
            leftClick()
            mousePos(Cord.d_normal)
            foodOnHand['salmon'] += 10
            time.sleep(.1)
            leftClick()
            time.sleep(2.5)
            return foodOnHand['salmon']
        else:
            print 'salmon is NOT available'
            mousePos(Cord.t_exit)
            leftClick()
            time.sleep(1)
            buyFood(food)
    if food == 'unagi':
        mousePos(Cord.phone)
        time.sleep(.1)
        leftClick()
        mousePos(Cord.menu_toppings)
        time.sleep(.5)
        leftClick()
        s = screenGrab()
        time.sleep(.1)
        if s.getpixel(Cord.t_unagi) != (250, 198, 168):
            print 'unagi is available'
            mousePos(Cord.t_unagi)
            time.sleep(.1)
            leftClick()
            mousePos(Cord.d_normal)
            foodOnHand['unagi'] += 10
            time.sleep(.1)
            leftClick()
            time.sleep(2.5)
            return foodOnHand['unagi']
        else:
            print 'unagi is NOT available'
            mousePos(Cord.t_exit)
            leftClick()
            time.sleep(1)
            buyFood(food)


def makeFood(food):
    """Makes the food

    This method receives a food argument from check_bubs() and clicks on the necessary
    ingredients.
    The ingredients counted in the foodOnHand dictionary are decremented when they are used
    for food and returned.

    :param food:
    :return:
    """
    if food == 'caliroll':
        print 'Making a caliroll'
        foodOnHand['rice'] -= 1
        foodOnHand['nori'] -= 1
        foodOnHand['fishegg'] -= 1
        mousePos(Cord.f_rice)
        leftClick()
        time.sleep(.05)
        mousePos(Cord.f_nori)
        leftClick()
        time.sleep(.05)
        mousePos(Cord.f_fishegg)
        leftClick()
        time.sleep(.1)
        foldMat()
        time.sleep(1.5)
        return foodOnHand['rice'], foodOnHand['nori'], foodOnHand['fishegg']
    elif food == 'onigiri':
        print 'Making a onigiri'
        foodOnHand['rice'] -= 2
        foodOnHand['nori'] -= 1
        mousePos(Cord.f_rice)
        leftClick()
        time.sleep(.05)
        mousePos(Cord.f_rice)
        leftClick()
        time.sleep(.05)
        mousePos(Cord.f_nori)
        leftClick()
        time.sleep(.1)
        foldMat()
        time.sleep(.05)
        foldMat()
        time.sleep(1.5)
        return foodOnHand['rice'], foodOnHand['nori']
    elif food == 'gunkan':
        print 'Making a gunkan'
        foodOnHand['rice'] -= 1
        foodOnHand['nori'] -= 1
        foodOnHand['fishegg'] -= 2
        mousePos(Cord.f_rice)
        leftClick()
        time.sleep(.05)
        mousePos(Cord.f_nori)
        leftClick()
        time.sleep(.05)
        mousePos(Cord.f_fishegg)
        leftClick()
        time.sleep(.05)
        mousePos(Cord.f_fishegg)
        leftClick()
        time.sleep(.1)
        foldMat()
        time.sleep(1.5)
        return foodOnHand['rice'], foodOnHand['nori'], foodOnHand['fishegg']


def checkFood():
    """Checks ingredients to see if any of them need to be replenished

    This method cycles through the foodOnHand dictionary and checks each value.
    If any value is less than or equal to 4, the respective ingredient is sent to
    the buyFood() method

    :return:
    """
    for i, j in foodOnHand.items():
        if i == 'nori' or i == 'rice' or i == 'salmon' or i == 'fishegg' or i == 'unagi' or i == 'shrimp':
            if j <= 4:
                print '%s is low and needs to be replenished' % i
                buyFood(i)


def clear_tables():
    """Clears tables

    This method moves the mouse to each possible plate position and clicks to clear it.

    :return:
    """
    mousePos((82, 178))
    leftClick()

    mousePos((190, 174))
    leftClick()

    mousePos((287, 181))
    leftClick()

    mousePos((393, 178))
    leftClick()

    mousePos((487, 180))
    leftClick()

    mousePos((595, 179))
    leftClick()
    time.sleep(1)


def foldMat():
    """Folds the mat

    This method moves the mouse and clicks on the mat to fold it, the last step in
    makeFood()

    :return:
    """
    mousePos((Cord.f_rice[0] + 40, Cord.f_rice[1]))
    leftClick()
    time.sleep(.1)


x_pad = 32
y_pad = 169


def screenGrab():
    """Gets a picture of the game

    This method uses the ImageGrab module to get a picture of the game.

    :return:
    """
    b1 = (x_pad+1, y_pad+1, x_pad+800, y_pad+600)
    im = ImageGrab.grab(b1)
    ##im.save(os.getcwd() + '\\full_snap__' + str(int(time.time())) + '.png', 'PNG')
    return im


def grab():
    """Gets pixel sum of screenGrab()

    This method gets the sum of the pixels of each food bubble to compare to the
    sushitypeOne - sushitypeSix dictionaries to read food orders.

    :return:
    """
    b1 = (x_pad+1, y_pad+1, x_pad+800, y_pad+600)
    im = ImageOps.grayscale(ImageGrab.grab(b1))
    a = numarray(im.getcolors())
    a = a.sum()
    print a
    return a


def main():
    """Starts bot

    This method calls the startGame() method, which gets through the initial menu into
    the game.
    Then check_bubs() is run until the program is terminated.

    :return:
    """
    startGame()
    while True:
        check_bubs()


if __name__ == '__main__':
    main()


def leftClick():
    """Allows bot to left click

    :return:
    """
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    print "Click."


def leftDown():
    """Allows bot to hold down left click

    :return:
    """
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(.1)
    print "Left Down."


def leftUp():
    """Allows the bot to move the mouse up

    :return:
    """
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    time.sleep(.1)
    print "Left Release"


def mousePos(cord):
    """Sets the coordinates of the mouse

    :param cord:
    :return:
    """
    win32api.SetCursorPos((x_pad + cord[0], y_pad + cord[1]))


def get_cords():
    """Retrieves and prints the coordinates of the mouse

    :return:
    """
    x, y = win32api.GetCursorPos()
    x = x - x_pad
    y = y - y_pad
    print x, y


def startGame():
    """Starts sushi-go-round

    This method navigates through the buttons of the main menu to start the game

    :return:
    """
    mousePos((302, 188))
    leftClick()
    time.sleep(.1)

    mousePos((399, 356))
    leftClick()
    time.sleep(.1)

    mousePos((573, 421))
    leftClick()
    time.sleep(.1)

    mousePos((354, 357))
    leftClick()
    time.sleep(.1)


def get_seat_one():
    """Identifies food orders from seat one and returns to check_bubs()

    This method finds the pixel sum of the order bubble above the customers head.
    The sum is compared to the sushiTypeOne dictionary values to determine the type of food.
    the pixel sum is returned to check_bubs()

    :return:
    """
    box = (x_pad + 32, y_pad + 80, x_pad + 112, y_pad + 92)
    im = ImageOps.grayscale(ImageGrab.grab(box))
    a = numarray(im.getcolors())
    a = a.sum()
    print a
    im.save(os.getcwd() + '\\seat_one__' + str(int(time.time())) + '.png', 'PNG')
    if a.sum() == sushiTypeOne['Onigiri']:
        print 'Table 1: Onigiri'
    elif a.sum() == sushiTypeOne['Caliroll']:
        print 'Table 1: Caliroll'
    elif a.sum() == sushiTypeOne['Gunkan']:
        print 'Table 1: Gunkan'
    else:
        print 'Table 1: Error'
    return a


def get_seat_two():
    """Identifies food orders from seat two and returns to check_bubs()

    This method finds the pixel sum of the order bubble above the customers head.
    The sum is compared to the sushiTypeTwo dictionary values to determine the type of food.
    the pixel sum is returned to check_bubs()

    :return:
    """
    box = (x_pad + 159, y_pad + 80, x_pad + 159 + 80, y_pad + 92)
    im = ImageOps.grayscale(ImageGrab.grab(box))
    a = numarray(im.getcolors())
    a = a.sum()
    print a
    im.save(os.getcwd() + '\\seat_two__' + str(int(time.time())) + '.png', 'PNG')
    if a.sum() == sushiTypeTwo['Onigiri']:
        print 'Table 2: Onigiri'
    elif a.sum() == sushiTypeTwo['Caliroll']:
        print 'Table 2: Caliroll'
    elif a.sum() == sushiTypeTwo['Gunkan']:
        print 'Table 2: Gunkan'
    else:
        print 'Table 2: Error'
    return a


def get_seat_three():
    """Identifies food orders from seat three and returns to check_bubs()

    This method finds the pixel sum of the order bubble above the customers head.
    The sum is compared to the sushiTypeThree dictionary values to determine the type of food.
    the pixel sum is returned to check_bubs()

    :return:
    """
    box = (290, y_pad + 80, x_pad + 290 + 80, y_pad + 92)
    im = ImageOps.grayscale(ImageGrab.grab(box))
    a = numarray(im.getcolors())
    a = a.sum()
    print a
    im.save(os.getcwd() + '\\seat_three__' + str(int(time.time())) + '.png', 'PNG')
    if a.sum() == sushiTypeThree['Onigiri']:
        print 'Table 3: Onigiri'
    elif a.sum() == sushiTypeThree['Caliroll']:
        print 'Table 3: Caliroll'
    elif a.sum() == sushiTypeThree['Gunkan']:
        print 'Table 3: Gunkan'
    else:
        print 'Table 3: Error'
    return a


def get_seat_four():
    """Identifies food orders from seat four and returns to check_bubs()

    This method finds the pixel sum of the order bubble above the customers head.
    The sum is compared to the sushiTypeFour dictionary values to determine the type of food.
    the pixel sum is returned to check_bubs()

    :return:
    """
    box = (x_pad + 411, y_pad + 80, x_pad + 411 + 80, y_pad + 92)
    im = ImageOps.grayscale(ImageGrab.grab(box))
    a = numarray(im.getcolors())
    a = a.sum()
    print a
    im.save(os.getcwd() + '\\seat_four__' + str(int(time.time())) + '.png', 'PNG')
    if a.sum() == sushiTypeFour['Onigiri']:
        print 'Table 4: Onigiri'
    elif a.sum() == sushiTypeFour['Caliroll']:
        print 'Table 4: Caliroll'
    elif a.sum() == sushiTypeFour['Gunkan']:
        print 'Table 4: Gunkan'
    else:
        print 'Table 4: Error'
    return a


def get_seat_five():
    """Identifies food orders from seat five and returns to check_bubs()

    This method finds the pixel sum of the order bubble above the customers head.
    The sum is compared to the sushiTypeFive dictionary values to determine the type of food.
    the pixel sum is returned to check_bubs()

    :return:
    """
    box = (x_pad + 537, y_pad + 80, x_pad + 537 + 80, y_pad + 92)
    im = ImageOps.grayscale(ImageGrab.grab(box))
    a = numarray(im.getcolors())
    a = a.sum()
    print a
    im.save(os.getcwd() + '\\seat_five__' + str(int(time.time())) + '.png', 'PNG')
    if a.sum() == sushiTypeFive['Onigiri']:
        print 'Table 5: Onigiri'
    elif a.sum() == sushiTypeFive['Caliroll']:
        print 'Table 5: Caliroll'
    elif a.sum() == sushiTypeFive['Gunkan']:
        print 'Table 5: Gunkan'
    else:
        print 'Table 5: Error'
    return a


def get_seat_six():
    """Identifies food orders from seat six and returns to check_bubs()

    This method finds the pixel sum of the order bubble above the customers head.
    The sum is compared to the sushiTypeSix dictionary values to determine the type of food.
    the pixel sum is returned to check_bubs()

    :return:
    """
    box = (x_pad + 663, y_pad + 80, x_pad + 663 + 80, y_pad + 92)
    im = ImageOps.grayscale(ImageGrab.grab(box))
    a = numarray(im.getcolors())
    a = a.sum()
    print a
    im.save(os.getcwd() + '\\seat_six__' + str(int(time.time())) + '.png', 'PNG')
    if a.sum() == sushiTypeSix['Onigiri']:
        print 'Table 6: Onigiri'
    elif a.sum() == sushiTypeSix['Caliroll']:
        print 'Table 6: Caliroll'
    elif a.sum() == sushiTypeSix['Gunkan']:
        print 'Table 6: Gunkan'
    else:
        print 'Table 6: Error'
    return a


def get_all_seats():
    """Used for testing

    :return:
    """
    get_seat_one()
    get_seat_two()
    get_seat_three()
    get_seat_four()
    get_seat_five()
    get_seat_six()


# sushibot
