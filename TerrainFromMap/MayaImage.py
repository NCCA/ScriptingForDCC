import maya.api.OpenMaya as OpenMaya
import uuid

class MayaImage :
  """ The main class, needs to be constructed with a filename """
  def __init__(self,filename) :
    """ constructor pass in the name of the file to load (absolute file name with path) """
    # create an MImage object
    self.image=OpenMaya.MImage()
    # read from file MImage should handle errors for us so no need to check
    self.image.readFromFile(filename)
    self.width,self.height=self.image.getSize()
    # get the pixel data
    self.charPixelPtr = uuid.ctypes.cast(self.image.pixels(), uuid.ctypes.POINTER(uuid.ctypes.c_char) )

    # query to see if it's an RGB or RGBA image, this will be True or False
    self.hasAlpha=self.image.isRGBA()
    # if we are doing RGB we step into the image array in 3's
    # data is always packed as RGBA even if no alpha present
    self.imgStep=4



  def getPixel(self,x,y) :
    """ get the pixel data at x,y and return a 3/4 tuple depending upon type """
    # check the bounds to make sure we are in the correct area
    if x<0 or x>self.width :
      print "error x out of bounds\n"
      return
    if y<0 or y>self.height :
      print "error y our of bounds\n"
      return
    # now calculate the index into the 1D array of data
    index=(y*self.width*4)+x*4
    # grab the pixels
    red = int(ord(self.charPixelPtr[index]))
    green = int(ord(self.charPixelPtr[index+1]))
    blue = int(ord(self.charPixelPtr[index+2]))
    alpha=int(ord(self.charPixelPtr[index+3]))
    #print type(red),green,blue,alpha
    return (red,green,blue,alpha)

  def getRGB(self,x,y) :
    r,g,b,_=self.getPixel(x,y)
    return (r,g,b)
