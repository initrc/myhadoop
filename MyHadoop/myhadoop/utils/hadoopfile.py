'''
Created on Dec 10, 2011

@author: david
'''
import os
import tempfile
import shutil
import subprocess
import time
from django.conf import settings

class HadoopFile(object):
    '''
    upload files
    '''
    def __init__(self, source):
        '''
        constructor
        '''
        self.source = source
        self.APP_DIR = os.path.realpath(os.path.join(settings.PROJECT_PATH, "myhadoop"))
        self.INPUT_DIR = os.path.realpath(os.path.join(self.APP_DIR, "input"))
        self.OUTPUT_DIR = os.path.realpath(os.path.join(self.APP_DIR, "static", "output"))
        self.SCRIPT = os.path.realpath(os.path.join(self.APP_DIR, "scripts", "hadoop.sh"))

    def execute(self):
        _, filepath = tempfile.mkstemp(prefix=self.source.name, dir=self.INPUT_DIR)
        with open(filepath, 'wb') as dest:
            shutil.copyfileobj(self.source, dest)
        print(filepath)
        print(self.OUTPUT_DIR)
        # call script
        filename = os.path.basename(filepath) + ".tar.gz"
        subprocess.call([self.SCRIPT, filename, filepath, self.OUTPUT_DIR])
        # check if output file has been created
        while not os.path.exists(os.path.join(self.OUTPUT_DIR, filename)):
            time.sleep(1)
        result = filename
        return result
