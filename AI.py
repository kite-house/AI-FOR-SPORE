def load(exit, mode):
    import time
    import cv2
    import mss
    import numpy as np
    import win10toast
    import pyautogui

    def mouse_control(x,y):
        try:
            pyautogui.moveTo(x,y)
        except Exception:
            pass
        else:
            pyautogui.mouseDown(button='right')

    
    mon = {"top": 0, "left": 0, "width": 1920, "height": 1080}
    sct = mss.mss()


    while True:
        time.sleep(0.5)
        if str(exit).split(' ')[2] == 'stopped':
            win10toast.ToastNotifier().show_toast('AI FOR SPORE','Program finish')
            quit()

        img = np.asarray(sct.grab(mon))

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        if mode == 'carnivorous':
            lower = np.array([144,90,114])
            upper = np.array([203,132,164])


        elif mode == 'herbivorous':
            lower = np.array([50, 100, 100])
            upper = np.array([70, 255, 255])

        else:
            raise SystemError()

        mask = cv2.inRange(hsv, lower, upper)
    
        
        # Создание контуров
        
        contours, hierarchy = cv2.findContours(mask.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

        # ПОЛУЧЕНИЕ сведений об местоположений контуров в соотвествие с x,y

        def location_determination(contours):
            list_coordinates = []
            for c in contours:
                if cv2.contourArea(c) <= 50 :
                    continue    
                x,y,w,h = cv2.boundingRect(c)
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255,0), 2)
                xy = x,y
                list_coordinates.append(xy)
               
            list_coordinates = np.array(list_coordinates)
            midlesize = np.array((1920 / 2, 1080 / 2))
            distances = np.linalg.norm(list_coordinates-midlesize, axis=1)
            min_index = np.argmin(distances)
            x, y = list_coordinates[min_index]
            print(f'x : {x}, y: {y}')
            return x,y

        # наведение указателя на обьект
        

        try:
            x,y = location_determination(contours)
        except Exception:
            print("Not Object")
        else:
            mouse_control(x,y)