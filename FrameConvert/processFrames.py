#!/usr/bin/env python
from __future__ import print_function
import OpenImageIO as oiio
import sys,os
import argparse

def processFrame(number,inDir,inFile,outDir,outFileType,fileType) :
  #print('{} {} {} {}'.format(number,inFile,outDir,outFileType))
    # Read a camera raw, crop and write out to a tiff
  buf = oiio.ImageBuf(inDir+'/'+inFile)
  spec = buf.spec()
  print('wxh {} {}'.format(spec.width,spec.height))
  cropped = oiio.ImageBuf()

  oiio.ImageBufAlgo.resize (cropped,buf, roi=oiio.ROI(0,spec.width/4,0,spec.height/4,0,1,0,3))
  #cropped.write( inFileName[0:inFileName.find('.') ]+'.png')

  borderSize=50
  final = oiio.ImageBuf(oiio.ImageSpec((spec.width/4)+borderSize ,(spec.height/4)+(borderSize), 3, oiio.FLOAT))
  oiio.ImageBufAlgo.fill(final,[0.1,0.1,0.1])
  oiio.ImageBufAlgo.paste(final, borderSize/2, borderSize/2, 0, 0, cropped)

  oiio.ImageBufAlgo.render_text(final,borderSize/2 , 20, "Show : Inferno : Shot 01" , 20, "OpenSans-Bold" )
  frame='Frame {0:05d} File {1}'.format(number,inFile)
  oiio.ImageBufAlgo.render_text(final,borderSize/2 , (spec.height/4)+borderSize-5, frame , 20, "OpenSans-Bold" )

  final.write( outDir+'/'+inFile[0:inFile.find('.'+fileType) ]+'.'+outFileType)
  print('Writing {}'.format(outDir+'/'+inFile[0:inFile.find('.'+fileType) ]+'.'+outFileType))

def main(inDir,outDir,fileType,outFileType) :
  print('{} {} {} {}'.format(inDir,outDir,fileType,outFileType))
  frames=os.listdir(inDir)
  for num,inFile in enumerate(frames) :
    if inFile.lower().endswith(tuple(fileType)) :
      processFrame(num,inDir,inFile,outDir,outFileType,fileType)



if __name__ == '__main__':

  
  parser = argparse.ArgumentParser(description='Modify render parameters')

  parser.add_argument('--inputdir', '-i', nargs='?', type=str, required=True,
                      help='input directory for frames')

  parser.add_argument('--outputdir', '-o', nargs='?', type=str, required=True,
                      help='output directory for frames')
  

  parser.add_argument('--inFileType', '-if', nargs='?', const='dng', default='dng',type=str,
                      help='output directory for frames')
  parser.add_argument('--outFileType', '-of', nargs='?', const='tiff', default='tiff',type=str,
                      help='output directory for frames')


  args = parser.parse_args()

  # check to see if directory exists
  if os.path.isdir(args.inputdir) == False :
    print('{} is not a valid directory'.format(args.inputdir))
    sys.exit()
  if os.path.isdir(args.outputdir) == False :
    print('creating directory {}'.format(args.outputdir))
    try :
      os.mkdir(args.outputdir)
    except :
      print('error making directory')
      sys.exit()  

  main(args.inputdir,args.outputdir,args.inFileType,args.outFileType)