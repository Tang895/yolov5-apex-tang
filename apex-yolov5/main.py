import pynput.mouse

from .grabscreen import grab_screen
import win32con,win32gui
import torch
from .apex_model import  load_model
from utils.general import  non_max_suppression,scale_boxes,xyxy2xywh
from utils.augmentations import letterbox
import cv2,time
import numpy as np
global lock
from .mouse_lock import MouseLock, lock
device = 'cuda' if torch.cuda.is_available() else 'cpu'
half = device != 'cpu'
imgsz = 640
conf_thres = 0.4
iou_thres = 0.05
#screen_width, screren_ = (1920, 1080)  # 1280 * 1024
screen_width,screen_height = (2560,1440)
#截屏区域
offet_Shot_Screen = 20 #屏幕截图偏移量,
#默认16：9, 1920x1080 , 960, 540是屏幕中心，根据自己的屏幕修改
left_top_x = screen_width//2 - offet_Shot_Screen*16
left_top_y = screen_height//2 - offet_Shot_Screen*9
right_bottom_x = screen_width//2 + offet_Shot_Screen*16
right_bottom_y = screen_height//2 + offet_Shot_Screen*9
shot_Width = 2*offet_Shot_Screen*16  #截屏区域的实际大小需要乘以2，因为是计算的中心点
shot_Height = 2*offet_Shot_Screen*9


window_Name="apex-tang"
auto = True
model = load_model()
lock_mode = False  #don's edit this
lock_button="left" #无用，apex为按住鼠标左或者右其中一个为就为lock模式，建议在游戏设置按住开镜
isShowDebugWindow = True  #可修改为True，会出现调试窗口
isRightKeyDown = False
isLeftKeyDown = False
isX2KeyDown = False
mouseFlag = 0   #0, 1 2 3

def on_click(x, y, button, pressed):
    global lock_mode, isX2Down
    if button == button.x2: # 使用鼠标上面一个侧键切换锁定模式，需要在apex设置中调整按键避免冲突
        isX2Down = pressed
        lock_mode = pressed
        print(f'isX2Down: {isX2Down}')
        
# ...or, in a non-blocking fashion:
listener = pynput.mouse.Listener(
    on_click=on_click)
listener.start()
names = model.module.names if hasattr(model, 'module') else model.names
def main():
    mouselock = MouseLock(shot_Width, shot_Height)
    while(True):
        t0 = time.time()
        img0 = grab_screen(region=(left_top_x, left_top_y, right_bottom_x, right_bottom_y))
        img0 = cv2.resize(img0, (shot_Width, shot_Height))
        stride = model.stride
        img = letterbox(img0, imgsz, stride=stride,auto=model.pt)[0]
        img = img.transpose((2, 0, 1))[::-1]
        img = np.ascontiguousarray(img)

        img = torch.from_numpy(img).to(model.device)
        img = img.half() if model.fp16 else img.float()
        img /= 255

        if len(img.shape) == 3:
            img = img[None] # img = img.unsqueeze(0)

        pred = model(img, augment=False, visualize=False)
        pred = non_max_suppression(pred, conf_thres, iou_thres, agnostic=False)
        #print(pred)

        aims = []
        for i, det in enumerate(pred):
            gn = torch.tensor(img0.shape)[[1, 0, 1, 0]]
            if len(det):
                det[:, :4] = scale_boxes(img.shape[2:], det[:, :4], img0.shape).round()

                for *xyxy, conf, cls in reversed(det):
                    # bbox:(tag, x_center, y_center, x_width, y_width)
                    """
                    0 ct_head  1 ct_body  2 t_head  3 t_body
                    """
                    xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()  # normalized xywh
                    line = (cls, *xywh)  # label format
                    aim = ('%g ' * len(line)).rstrip() % line
                    aim = aim.split(' ')
                    #print("aim:",aim)
                    aims.append(aim)
        if len(aims):
            mouselock.set_lock_state(lock_mode)
            mouselock.lock(aims)
            print(f"set mouse lock state to {lock_mode}")
            # print(f"mouse lock state: {lock_state}")
            for i, det in enumerate(aims):
                tag, x_center, y_center, width, height = det
                x_center, width = shot_Width * float(x_center), shot_Width * float(width)
                y_center, height = shot_Height * float(y_center), shot_Height * float(height)
                top_left = (int(x_center - width / 2.0), int(y_center - height / 2.0))
                bottom_right = (int(x_center + width / 2.0), int(y_center + height / 2.0))
                color = (0, 0, 255)  # BGR
                if(isShowDebugWindow):
                    cv2.rectangle(img0, top_left, bottom_right, color, thickness=3)
        else:
            mouselock.set_lock_state(False) # no target, unlock

        if(isShowDebugWindow):
            cv2.namedWindow(window_Name, cv2.WINDOW_NORMAL)
            cv2.resizeWindow(window_Name, shot_Width//2, shot_Height//2)
            #global t0
            cv2.putText(img0, "FPS:{:.1f}".format(1.0 / (time.time() - t0)), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 2,(0, 255, 0), 4)
            cv2.imshow(window_Name, img0)

            t0 = time.time()
            hwnd = win32gui.FindWindow(None, window_Name)
            CVRECT = cv2.getWindowImageRect(window_Name)
            win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                mouselock.set_exit_flag(True)
                break
main()
