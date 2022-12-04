
import win32api,win32con

#
# win32api.SetCursorPos((200, 200))
from mouse import mouse_xy
import time
import pydirectinput

#mouse_xy(100,100)
time0 = time.time()
for i in range(199):
    #pydirectinput.moveTo(200,200)
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 1,1)
    #mouse_xy(-3,3)
print(time.time()-time0)



