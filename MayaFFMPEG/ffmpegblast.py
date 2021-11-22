import maya.api.OpenMaya as OpenMaya
import maya.api.OpenMayaUI as OpenMayaUI
import maya.OpenMayaUI as omui
from PySide2 import (QtCore,QtWidgets)
import sys,array,random
import subprocess as sp
import ctypes
import uuid

from shiboken2 import wrapInstance

def get_main_window() :
  window = omui.MQtUtil.mainWindow()
  return wrapInstance(int(window),QtWidgets.QDialog)

 
class EncodeDialog(QtWidgets.QDialog):

  def __init__(self, parent=get_main_window()):
    super().__init__(parent)
    self.p = None  # Default empty value.
    self.btn = QtWidgets.QPushButton("Execute",self)
    self.btn.pressed.connect(self.start_process)


  def start_process(self):

    if self.p is None:  # No process running.
      print("start")
      self.p = QtCore.QProcess()  # Keep a reference to the QProcess (e.g. on self) while it's running.
      self.p.finished.connect(self.process_finished)  # Clean up once complete.
      self.p.started.connect(self.process_started)  # Clean up once complete.
      self.view = OpenMayaUI.M3dView.active3dView()
      self.width = self.view.portWidth()
      self.height = self.view.portHeight()
      self.image = OpenMaya.MImage()
      print(self.width,self.height)
      ffmpeg = "/Applications/ffmpeg"

      command = [  '-f', 'rawvideo',  '-pixel_format', 'rgba' ,
      '-video_size' ,'{}x{}'.format(self.width,self.height) , 
      '-i', '-' , 
      '-vf', 'vflip', # frambuffer flipped
      #'-crf' ,'20', 
      '-preset' ,'slow' ,
      #'-tune','animation',
      '-c:v' ,'libx264', 
      #'-vcodec', 'mpeg4',
      '-y', '/Users/jmacey/TestMaya.mp4']      
      self.p.start(ffmpeg, command)
      print(self.p.readAllStandardOutput())

      self.p.waitForFinished()

  def process_started(self) :

    for i in range(1,85) :
      cmds.currentTime(i)
      self.view.readColorBuffer(self.image, True)
      self.p.write(QtCore.QByteArray(bytearray(image_to_bytearray(self.image))))
    self.p.closeWriteChannel()


  def process_finished(self):
    self.p = None
    print("finished")



if __name__ == "__main__" :
  
  w = EncodeDialog()
  w.show()

