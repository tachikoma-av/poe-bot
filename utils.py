import numpy as np
from grabscreen import grab_screen
import cv2
import time
from getkeys import key_check
import os
import win32gui
import win32api, win32con

class self_window():
    character = None
    def __init__(self):
        self.differenceX, self.differenceY = seek_for_window()
        self.window_region = (self.differenceX,self.differenceY,800+self.differenceX-1,600+self.differenceY-1)
        self.running = True
    def cursor_pos(self):
        tup = win32api.GetCursorPos()
        x = tup[0] - self.differenceX
        y = tup[1] - self.differenceY
        return (x,y)
    def right_click_without_move(self):
        x,y = win32api.GetCursorPos()[0], win32api.GetCursorPos()[1]
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
        time.sleep(0.07)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
    def click(self,x,y):
        x = x + self.differenceX
        y = y + self.differenceY

        # add slight move!
        # print(win32api.GetCursorPos())
        win32api.SetCursorPos((x,y))
        time.sleep(0.2)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
        time.sleep(0.07)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
    def screenshot(self):
        img_rgb = grab_screen(region=(self.differenceX,self.differenceY,800+self.differenceX-1,600+self.differenceY-1))
        cv2.imwrite('screen.png',img_rgb)
def callback(hwnd, extra):
    # if win32gui.GetWindowText(hwnd) == 'Path of Exile': 
    rect = win32gui.GetWindowRect(hwnd)
    x = rect[0]
    y = rect[1]
    return (x+8, y+31)
    w = rect[2] - x
    h = rect[3] - y
    print("Window %s:" % win32gui.GetWindowText(hwnd))
    print("\tLocation: (%d, %d)" % (x, y))
    print("\t    Size: (%d, %d)" % (w, h))
    #img_rgb = grab_screen(region=(x+8,y+31,800+x+7,600+y+30))
    # print_img(img_rgb)
    
def seek_for_window():
    hwnd = win32gui.FindWindow(None, "Path of Exile")
    print('window found')
    difference = callback(hwnd,None)
    return difference[0], difference[1]
    import pdb; pdb.set_trace()
    
def zseek_for_login_page():
    while True:
        last_time = time.time()
        # img_rgb = grab_screen(region=(33,31,832,630)) 833 631
        img_rgb = grab_screen(region=(0,0,1024,768))
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        # back_img = img_rgb[60:110, 390:440]
        # (Pdb) cv2.imwrite('obj.png',back_img)
        template = cv2.imread('clue.png',0)
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where( res >= threshold)
        for pt in zip(*loc[::-1]):
#             width_difference, height_difference = (pt[0]-390,pt[1]-60)
            cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 1)
            # pt[0] + 10        pt[0] + w
            #cv2.line(img_rgb, (540, pt[1] + round(h/2) ), (540, pt[1] + round(h/2) ), (255,0,0), 4)
        print_img(img_rgb)
        cv2.imwrite('res.png',img_rgb)
        import pdb; pdb.set_trace()
        # print('loop took {} seconds'.format(time.time()-last_time))

def print_img(img):
    cv2.imshow("test", img); cv2.waitKey(0); cv2.destroyAllWindows()
# # def test():
#     last_time = time.time()
#     img_rgb = cv2.imread('main_menu.png')
#     img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
#     template = cv2.imread('login_button.png',0)
#     w, h = template.shape[::-1]
#     res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
#     threshold = 0.8
#     loc = np.where( res >= threshold)
#     counter = 1
#     for pt in zip(*loc[::-1]):
#         # cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
#         import pdb; pdb.set_trace()# pt[0] + 10        pt[0] + w
#         cv2.line(img_rgb, (540, pt[1] + round(h/2) ), (540, pt[1] + round(h/2) ), (255,0,0), 4)
#     print_img(img_rgb)
#     cv2.imwrite('res.png',img_rgb)
#     # print('loop took {} seconds'.format(time.time()-last_time))
def save_img(img,name):
    cv2.imwrite( str(name)+".jpg",img)
def create_backup_img(width,height):
    file_name = 'backup_data.npy'
    region = (0,0,1024,768)#x = 1024, y = 768
    screen = grab_screen(region=(0,0,1024,768))
    print_img(screen)
    if os.path.isfile(file_name):
        print('File exists, loading previous data!')
        training_data = list(np.load(file_name))
    else:
        print('File does not exist, starting fresh!')
        training_data = []
    screen = grab_screen(region=region)
    #print_img(screen)
    training_data.append([screen])
    np.save(file_name,training_data)

def load_arr():
    return list(np.load('backup_data.npy'))

def utils_main():
    screen = grab_screen(region=(0,0,1024,768))
    screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    logo_part = screen[100:200, 400:500]

    #click(log_in)

    import pdb; pdb.set_trace()
# test()