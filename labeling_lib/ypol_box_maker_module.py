import os

import cv2
from .File_reader import File_reader
from .Box_maker import Box_maker
from .Config_reader import Confing_reader

def run_box_maker():


    param = Confing_reader()
    ret = param.load_cfg()

    image_dir = os.path.expanduser(param.input_image_dir)
    annotation_dir = os.path.expanduser(param.annotation_dir)
    label_dir = os.path.expanduser(param.label_dir)
    product_key = param.product_key

    reader = File_reader(image_dir, annotation_dir, label_dir ,sort_by_number_str=False)

    label_list = reader.label_name_list
    box_maker = Box_maker(len(label_list))

    while True:

        reader.update_cur_image_index()
        image = reader.get_cur_image()

        if image is not None :

            img = image.copy()
            img = box_maker.draw_box(img)

            box_maker.save_box(image.shape, reader.get_annotation_dir())
            ret_img = reader.update_box_image()

            ret_img = box_maker.draw_box(ret_img)

            label = label_list[box_maker.get_label()]

            cv2.putText(ret_img, str(label), (100, 100), 0, fontScale=3.0,
                        color=(255,255,255), thickness=3)

            cur_pos = box_maker.cur_pos

            if cur_pos is not None:

                ret_img = cv2.line(ret_img, (0,cur_pos[1]), ((1920,cur_pos[1])), (255,0,0)  )
                ret_img = cv2.line(ret_img, (cur_pos[0], 0), ((cur_pos[0], 1080)), (255, 0, 0) )

            cv2.imshow('YPOL_BOX_MAKER',ret_img)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break_flg = True
            break
        elif key == ord(" "):
            reader.move_one_step(True)
        elif key == ord("b"):
            reader.move_one_step(False)
        elif key == ord("."):
            box_maker.move_label(True)
            pass
        elif key == ord(","):
            box_maker.move_label(False)
            pass
        elif key == ord("c"):
            box_maker.clear_box(reader.get_annotation_dir())
        elif key == ord("z"):
            reader.del_before()

        elif key == ord("f") :
            if box_maker.drag_start is None :
                box_maker.btn_down = True
            elif box_maker.drag_start is not None :
                box_maker.btn_up = True

        elif key == ord("1"):
            box_maker.set_label(0)

        elif key == ord("2"):
            box_maker.set_label(1)

        elif key == ord("3"):
            box_maker.set_label(product_key)
            
            
def generate_setup_file():

    if os.path.isdir(os.path.expanduser('~/labeling_data/')) == False:
        os.mkdir(os.path.expanduser('~/labeling_data/'))

    if os.path.isdir(os.path.expanduser('~/labeling_data/img/')) == False:
        os.mkdir(os.path.expanduser('~/labeling_data/img/'))

    if os.path.isdir(os.path.expanduser('~/labeling_data/annotation/')) == False:
        os.mkdir(os.path.expanduser('~/labeling_data/annotation/'))

    f = open(os.path.expanduser('~/labeling_data/config.ini'), 'w')
    config_contents = ""
    config_contents += "[dir_config]\n"
    config_contents += "input_image_dir = ~/labeling_data/img\n"
    config_contents += "annotation_dir = ~/labeling_data/annotation\n"
    config_contents += "label_dir = ~/labeling_data/ypol.names\n"
    config_contents += "product_label_key = 3\n"
    f.write(config_contents)
    f.close()

    f = open(os.path.expanduser('~/labeling_data/ypol.names'), 'w')
    ypol_names = ""
    f.write(config_contents)
    f.close()
