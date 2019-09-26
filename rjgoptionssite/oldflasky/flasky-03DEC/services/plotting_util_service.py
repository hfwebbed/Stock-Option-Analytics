import glob
import os
import random

class PlottingUtilServce:

    def clean_files(self,mask):
        files = glob.glob(mask)
        for filename in files:
            os.unlink(filename)

    def generate_filename(self,prefix,postfix):
        return prefix + str(random.randint(100000000, 999999999)) + postfix


