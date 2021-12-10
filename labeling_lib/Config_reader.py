from configparser import ConfigParser
import os

class Confing_reader:
    def __init__(self):
        self.parser = ConfigParser()

    def load_cfg(self,file_name=os.path.expanduser('~/labeling_data/config.ini')):
        try:
            self.parser.read(file_name)
            if (self.parser.sections()[0] == 'dir_config') :

                self.input_image_dir = self.parser.get('dir_config', 'input_image_dir')
                self.annotation_dir = self.parser.get('dir_config', 'annotation_dir')
                self.label_dir = self.parser.get('dir_config', 'label_dir')
                self.product_key = int(self.parser.get('dir_config', 'product_label_key'))


                return 1
            else :
                return -1
        except :
            return -1

