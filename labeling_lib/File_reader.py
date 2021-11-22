import os
import cv2
import random

def nothing(x):
    pass

class File_reader:

    def __init__(self,file_dir, annotation_dir, label_dir, sort_by_number_str = True):

        cv2.namedWindow('YPOL_BOX_MAKER', cv2.WINDOW_NORMAL)
        self.root_dir = file_dir
        self._cur_idx = 0
        self._pre_idx = -1
        file_name_list = os.listdir(file_dir)
        if sort_by_number_str == True :
            self.file_name_list = sorted(file_name_list, key=lambda x: int(x.split('.')[0]))
        elif sort_by_number_str == False :
            self.file_name_list = sorted(file_name_list)

        self.file_number = len(self.file_name_list)
        cv2.createTrackbar('file_list', 'YPOL_BOX_MAKER', 0, self.file_number-1, nothing)
        self.cur_image = None
        self.annotation_root_dir = annotation_dir
        self.cur_annotation_dir = None
        self.label_name_list = []

        with open(label_dir, "r") as f:
            label_names = f.readlines()
            self.num_label = len(label_names)
            for label_name in label_names :
                self.label_name_list.append(label_name.strip('\n'))
        self.color_table = self.get_color_table()
        self.annotation_copy = []


    def get_color_table(self):
        random.seed(2)
        color_table = {}
        for i in range(self.num_label):
            color_table[i] = [random.randint(0, 255) for _ in range(3)]
        return color_table


    def update_cur_image_index(self):
        idx = cv2.getTrackbarPos('file_list', 'YPOL_BOX_MAKER')
        self._cur_idx = idx

        if self._cur_idx != self._pre_idx  :
            image_dir = self.root_dir + '/' + self.file_name_list[self._cur_idx]

            self.cur_image = cv2.imread(image_dir)

            annotation_d = self.annotation_root_dir + '/' + self.file_name_list[self._cur_idx].split('.')[0] + '.txt'

            self.cur_annotation_dir = annotation_d

            is_exist = os.path.isfile(annotation_d)

            if is_exist == False :
                with open(annotation_d, "w") as f:
                    pass

    def update_box_image(self):

        ret_image = self.cur_image.copy()

        if (self.cur_image is not None) and (self.cur_annotation_dir is not None) :

            annotation_info = self.get_annotation()

            for anno in annotation_info:

                label = anno[0]
                xmin = anno[1]
                ymin = anno[2]
                xmax = anno[3]
                ymax = anno[4]

                cv2.rectangle(ret_image, (xmin, ymin), (xmax, ymax),self.color_table[label], 3)

                tx = int ( (xmax+xmin) / 2 )
                ty = int ( (ymax+ymin) / 2 )

                text_x = tx
                text_y = ty - ty/4

                cv2.putText(ret_image, self.label_name_list[label], (text_x, text_y), 0, fontScale=1.0, color=self.color_table[label], thickness=2)

        return ret_image

    def move_one_step(self, move_next = True):

        if move_next == True:
            if self._cur_idx + 1 <= self.file_number-1:
                self._cur_idx += 1
        else :
            if self._cur_idx -1 >= 0 :
                self._cur_idx -= 1

        cv2.setTrackbarPos('file_list',  'YPOL_BOX_MAKER', self._cur_idx)

    def get_current_id(self):
        return self._cur_idx

    def get_file_name_list(self):
        return self.file_name_list

    def get_cur_image(self):
        return self.cur_image

    def get_annotation_dir(self):
        return self.cur_annotation_dir

    def get_annotation(self):

        annotation_info = []

        with open(self.cur_annotation_dir, "r") as f:
            annotations = f.readlines()

            for anno_line in annotations:
                splited = anno_line.split(' ')
                tmp = []

                for spl in splited:
                    tmp.append(int(spl.rstrip('\n')))

                annotation_info.append(tmp)

        return annotation_info


    def copy_annotation(self):
        annotation = self.get_annotation()
        self.annotation_copy = []
        for anno in annotation:
            self.annotation_copy.append(anno)

    def paste_annotation(self):

        with open(self.cur_annotation_dir, "a") as f:
            for anno in self.annotation_copy:
                f.write( str(anno[0]) + " " + str(anno[1]) + " "+ str(anno[2]) + " " + str(anno[3]) + " " + str(anno[4]) + '\n' )

    def del_before(self):
        annotation = self.get_annotation()
        anno_len = len(annotation)
        idx = 0
        with open(self.cur_annotation_dir, "w") as f:
            for anno in annotation:

                if idx == anno_len - 1 :
                    break
                f.write( str(anno[0]) + " " + str(anno[1]) + " "+ str(anno[2]) + " " + str(anno[3]) + " " + str(anno[4]) + '\n' )
                idx += 1
