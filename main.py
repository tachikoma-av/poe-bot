import cv2
# import matplotlib.pyplot as plt
import numpy as np
import sys
import time
from getkeys import key_check
from utils import self_window, grab_screen
from math import cos,sin,radians,ceil
import win32api, win32con
# %matplotlib inline

#esli kartinka 
def do_smth_plz():
    x,y = win32api.GetCursorPos()[0], win32api.GetCursorPos()[1]
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,x,y,0,0)
    time.sleep(0.3)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,x,y,0,0)
    time.sleep(0.1)
def create_endLine_pointXY_by_angle(angle, length):
    '''
    takes angle of point, lenght of line
    returns x,y of point
    '''
    if length == 200: 
        length = 200
        start_x,start_y = 400,300
    else:start_x,start_y = 100,100
    angle = (360-angle)
    # ugol krivoy
    
    x = start_x-int(length*sin(radians(angle)))
    y = start_y-int(length*cos(radians(angle)))
    x,y = ceil(x),ceil(y)
    return x,y
def check_if_enemy_on_hover(pixel):
    '''
    img[22,330]
    '''
    if np.array_equal(pixel, [164,34,30]):
#     if img[22,330] == [164,  34,  30]:
        do_smth_plz()
        print('ITS AN ENEMY!')
        return True
    else: 
        print('nothing')
        return False
def createLineIterator(P1, P2, img):
    """
    Produces and array that consists of the coordinates and intensities of each pixel in a line between two points

    Parameters:
        -P1: a numpy array that consists of the coordinate of the first point (x,y)
        -P2: a numpy array that consists of the coordinate of the second point (x,y)
        -img: the image being processed

    Returns:
        -it: a numpy array that consists of the coordinates and intensities of each pixel in the radii (shape: [numPixels, 3], row = [x,y,intensity])     
    """
    #define local variables for readability
    imageH = img.shape[0]
    imageW = img.shape[1]
    P1X = P1[0]
    P1Y = P1[1]
    P2X = P2[0]
    P2Y = P2[1]

    #difference and absolute difference between points
    #used to calculate slope and relative location between points
    dX = P2X - P1X
    dY = P2Y - P1Y
    dXa = np.abs(dX)
    dYa = np.abs(dY)

    #predefine numpy array for output based on distance between points
    itbuffer = np.empty(shape=(np.maximum(dYa,dXa),3),dtype=np.float32)
    itbuffer.fill(np.nan)

    #Obtain coordinates along the line using a form of Bresenham's algorithm
    negY = P1Y > P2Y
    negX = P1X > P2X
    if P1X == P2X: #vertical line segment
        itbuffer[:,0] = P1X
        if negY:
            itbuffer[:,1] = np.arange(P1Y - 1,P1Y - dYa - 1,-1)
        else:
            itbuffer[:,1] = np.arange(P1Y+1,P1Y+dYa+1)              
    elif P1Y == P2Y: #horizontal line segment
        itbuffer[:,1] = P1Y
        if negX:
            itbuffer[:,0] = np.arange(P1X-1,P1X-dXa-1,-1)
        else:
            itbuffer[:,0] = np.arange(P1X+1,P1X+dXa+1)
    else: #diagonal line segment
        steepSlope = dYa > dXa
        if steepSlope:
            slope = dX.astype(np.float32)/dY.astype(np.float32)
            if negY:
                itbuffer[:,1] = np.arange(P1Y-1,P1Y-dYa-1,-1)
            else:
                itbuffer[:,1] = np.arange(P1Y+1,P1Y+dYa+1)
            itbuffer[:,0] = (slope*(itbuffer[:,1]-P1Y)).astype(np.int) + P1X
        else:
            slope = dY.astype(np.float32)/dX.astype(np.float32)
            if negX:
                itbuffer[:,0] = np.arange(P1X-1,P1X-dXa-1,-1)
            else:
                itbuffer[:,0] = np.arange(P1X+1,P1X+dXa+1)
            itbuffer[:,1] = (slope*(itbuffer[:,0]-P1X)).astype(np.int) + P1Y

    #Remove points outside of image
    colX = itbuffer[:,0]
    colY = itbuffer[:,1]
    itbuffer = itbuffer[(colX >= 0) & (colY >=0) & (colX<imageW) & (colY<imageH)]

    #Get intensities from img ndarray
    itbuffer[:,2] = img[itbuffer[:,1].astype(np.uint),itbuffer[:,0].astype(np.uint)]

    return itbuffer

# #1st init
# debugging = 0# 0 or 1, 1 is debug, 0 is realprocess
# # real one
# if debugging != 1:
#     game = self_window()
#     for i in list(range(4))[::-1]:
#         print(i+1)
#         time.sleep(1)
#     img = (grab_screen(region=(game.differenceX,game.differenceY,800+game.differenceX-1,600+game.differenceY-1)))
#     cursor_pos = game.cursor_pos()
#     file_name = 'img_cursorPos.npy'
#     examples = [img, cursor_pos,game]
#     np.save(file_name,examples)
# #debug
# else:
    
#     file_name = 'img_cursorPos.npy'
#     examples = list(np.load(file_name))
#     img, cursor_pos, game = examples[0], examples[1], examples[2]

"""
# start
"""


vec = 315# po gradusam iz 360, gde 0 - verh, 90 - pravo, 180 - niz, 270 - levo
game = self_window()

for i in list(range(4))[::-1]:
    print(i+1)
    time.sleep(1)
other_route_vector = None
enemy_spotted = False
paused = False
while True:
    if not paused:
        img = (grab_screen(region=(game.differenceX,game.differenceY,800+game.differenceX-1,600+game.differenceY-1)))
        if enemy_spotted is True:
            enemy_spotted = check_if_enemy_on_hover(img[22,330])
            if enemy_spotted is True:
                continue
    #     cursor_pos = game.cursor_pos()
    #     file_name = 'img_cursorPos.npy'
    #     examples = [img, cursor_pos,game]
    #     np.save(file_name,examples)

        #read minimap
        minimap = img[4:154, 646:796]# visota sverhu, shirina sleva
        minimap = minimap[40:110,40:110]# 70x70 # - vidimost' zoni na kotoryuy mojno clicknut'


        minimap = cv2.resize(minimap,(200,200))
        # minimap[90:110, 90:120] = 0
        # nalozhit_img1_na_img2(img1,img2)
        minimap = cv2.medianBlur(minimap,3)
        minimap = cv2.Canny(minimap,100,200)
        minimap[96:106, 94:106] = 0
        minimap_bit = minimap.copy()
        #i tut otmechai tochku dvijeniya
        movement_vector = vec
        """
        if movment_vector is OKAY:
            move(vector)
        else:
            perebirai vectora slevanapravo

        """

        cv2.imwrite('zxc.png', minimap)
        minimap = cv2.imread('zxc.png')


        minimap = cv2.resize(minimap,(800,800))
        minimap = minimap[100:700,0:800]


        #collect mask of white pixels
#         non_black_pixels_mask = np.any(minimap != [0, 0, 0], axis=-1)
#         #apply mask to img
#         img_copy1 = img.copy()
#         img_copy = img_copy1[0:600,0:800]

#         img_copy[non_black_pixels_mask] = [255,255,255]
#         img_copy1[0:600,0:800] = img_copy

        # minimap_full = np.zeros([10000, 10000, 3], dtype=np.uint8)
        # current_pos = (5000,5000) 
        # desire_pos = (1,1)

        # yFrom,yTo = ceil(current_pos[0] - minimap.shape[0] / 2), ceil(current_pos[0] + minimap.shape[0] / 2)
        # print(yFrom,yTo)
        # xFrom,xTo = ceil(current_pos[1] - minimap.shape[1] / 2), ceil(current_pos[1] + minimap.shape[1] / 2)
        # minimap_full[yFrom:yTo, xFrom:xTo] = minimap

        # minimap[93:113, 89:113] = 0
        # print(minimap.shape)
        # plt.imshow(minimap,cmap='gray')
        # plt.show()


        ####

        x,y = create_endLine_pointXY_by_angle(movement_vector,80)
        can_walk = False
        can_walk_in_percents = 0
        test_arr = createLineIterator(np.array([100,100], dtype=np.int32), np.array([x,y], dtype=np.int32),minimap_bit)
        num_of_iters = 0
        for iterx in test_arr:
            num_of_iters+=1
            if iterx[2] != 0: 
                break
        can_walk_in_percents =ceil(num_of_iters/len(test_arr)*100)
        print('can finish '+str(movement_vector)+'angle way by: '+str(can_walk_in_percents)+'%')
#         most_possible_route = [can_walk_in_percents, movement_vector, x, y]
        if can_walk_in_percents == 100:
            can_walk = True
            if other_route_vector is not None:
                for iter_num in list(range(x-200,x-160,1)):
                    if iter_num < 0: iter_num += 360
                    if other_route_vector == iter_num:
                        can_walk  = False
                        print('dont want to move back')
                        break
        if can_walk is True:
            print('doit')
            other_route_vector = movement_vector
        else:
            most_possible_route = None
            plus = True
            if other_route_vector is not None:
                movement_vector = other_route_vector
            for iter_num in list(range(1,180,1)):#5,10...95,100
                if plus is True: 
                    movement_vector += iter_num
                    plus = False
                else:
                    movement_vector -= iter_num
                    plus = True
                x,y = create_endLine_pointXY_by_angle(movement_vector,80)
                can_walk_in_percents = 0
                test_arr = createLineIterator(np.array([100,100], dtype=np.int32), np.array([x,y], dtype=np.int32),minimap_bit)
                num_of_iters = 0
                for iterx in test_arr:
                    num_of_iters+=1
                    if iterx[2] != 0: 
                        break
                can_walk_in_percents =ceil(num_of_iters/len(test_arr)*100)
                if most_possible_route is None:
                    most_possible_route = [can_walk_in_percents, movement_vector, x, y]
                else:
                    if most_possible_route[0] < can_walk_in_percents: most_possible_route = [can_walk_in_percents, movement_vector, x, y]
                trash_var = movement_vector
                if movement_vector >=360: trash_var = movement_vector - 360
                print('can finish '+str(trash_var)+' angle way by: '+str(can_walk_in_percents)+'%')
                print(x,y)
                if can_walk_in_percents == 100:
                    other_route_vector = trash_var
                    print('doit')
                    can_walk = True
                    break
            if can_walk is False:
                print('all variants are failure')
                if other_route_vector is not None:
                    movement_vector = other_route_vector +180
                can_walk_in_percents, movement_vector, x, y = most_possible_route[0], most_possible_route[1], most_possible_route[2], most_possible_route[3]
        print(can_walk_in_percents, movement_vector, x, y)
        minimap = cv2.resize(minimap,(200,200))
        cv2.line(minimap, (100,100), (x,y), (255,255,255), 2)
        x, y = create_endLine_pointXY_by_angle(movement_vector, 200)
        enemy_spotted = check_if_enemy_on_hover(img[22,330])
        game.click(x, y)# move
        cv2.imshow('minimap_path',minimap)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
        time.sleep(1)
    keys = key_check()
    if 'A' in keys:
        if paused:
            paused = False
            print('unpaused!')
            time.sleep(1)
        else:
            print('Pausing!')
            paused = True
            time.sleep(1)
    # plt.imshow(img_copy1)
    # plt.show()
    # print(minimap.shape)
    # plt.imshow(minimap,cmap='gray')
    # plt.show()
    # print(vec)