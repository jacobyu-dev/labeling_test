import cv2

def nothing(x):
    pass

class Box_maker:

    def __init__(self,num_label):
        cv2.setMouseCallback('YPOL_BOX_MAKER', self.onmouse)
        cv2.createTrackbar('label_bar', 'YPOL_BOX_MAKER', 0, num_label-1, nothing)
        self.selection = None
        self.drag_start = None
        self.num_label = num_label
        self.btn_down = False
        self.btn_up = False
        self.cur_pos = None

    def onmouse(self, event, x, y, flags, param):

        
        self.cur_pos = [x,y]

        '''
        if self.btn_down == True :
            self.drag_start = (x, y)
            self.btn_down = False

        if self.drag_start:
            xmin = min(x, self.drag_start[0])
            ymin = min(y, self.drag_start[1])
            xmax = max(x, self.drag_start[0])
            ymax = max(y, self.drag_start[1])

            if (xmax > xmin) and (ymax > ymin):
                self.selection = [xmin, ymin, xmax, ymax]

        if self.btn_up == True:
            self.drag_start = None
            self.btn_up = False
        '''

        
        
        if event == cv2.EVENT_LBUTTONDOWN:
            self.drag_start = (x, y)

        if self.drag_start:
            xmin = min(x, self.drag_start[0])
            ymin = min(y, self.drag_start[1])
            xmax = max(x, self.drag_start[0])
            ymax = max(y, self.drag_start[1])

            if (xmax > xmin) and (ymax > ymin) :
                self.selection = [xmin, ymin, xmax, ymax]

        if event == cv2.EVENT_LBUTTONUP:
            self.drag_start = None

        


    def get_label(self):
        label_idx = cv2.getTrackbarPos('label_bar', 'YPOL_BOX_MAKER')
        return label_idx


    def set_label(self,idx):

        if idx >= self.num_label :
            idx = self.num_label
        elif idx < 0 :
            idx = 0

        cv2.setTrackbarPos('label_bar', 'YPOL_BOX_MAKER', idx)

    def move_label(self, is_foward):

        cur_label = self.get_label()
        if is_foward == True:
            if cur_label +1 < self.num_label :
                cur_label += 1

        if is_foward == False:
            if cur_label -1 >= 0 :
                cur_label -= 1

        cv2.setTrackbarPos('label_bar', 'YPOL_BOX_MAKER', cur_label)


    def save_box( self, imshape, annotation_dir ):

        if (self.drag_start == None) and (self.selection != None):

            im_height = imshape[0]
            im_width =  imshape[1]

            xmin = self.selection[0]
            ymin = self.selection[1]
            xmax = self.selection[2]
            ymax = self.selection[3]

            label = self.get_label()
            if (xmax > xmin) and (xmin>=0) and (xmax < im_width) and (ymax > ymin) and (ymin>=0) and (ymax < im_height) :
                with open(annotation_dir, "a") as f:
                    f.write(str(label)+" "+str(xmin)+" "+str(ymin)+" "+str(xmax)+" "+str(ymax) + "\n")
                self.selection = None

    def draw_box(self,image):

        if (self.drag_start is not None) and (self.selection is not None):
            ret_img = cv2.rectangle(image, (self.selection[0], self.selection[1]), (self.selection[2], self.selection[3]), (255,0,0), 3)
            return ret_img
        else:
            return image

    def clear_box(self,annotation_dir):
        with open(annotation_dir, "w") as f:
            pass
