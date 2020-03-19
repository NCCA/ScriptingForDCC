#!/Applications/Autodesk/maya2019/Maya.app/Contents/bin/mayapy

import maya.standalone
import unittest
import MayaImage as mi

class TestMayaImage(unittest.TestCase):
  @classmethod
  def setUpClass(self):
    print('doing setup')
    
  def testConstructFromWidthHeight(self) :
    image=mi.MayaImage(width=100,height=200)
    self.assertEqual(image.width,100)
    self.assertEqual(image.height,200)
    
  def testThrowFromBadFilename(self) :
    with self.assertRaises(ValueError) :
      _=mi.MayaImage(200)

if __name__ == '__main__' :
  maya.standalone.initialize(name='python')
  unittest.main()
  print('closing down maya-standalone')
  maya.standalone.uninitialize()