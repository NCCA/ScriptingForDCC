#!/usr/bin/env python
class Attr :

    def __init__(self,x=1.0,y=1.0) :
        self.x=x
        self.y=y

    def __str__(self) :
        ''' this method will return our data when doing something like print v '''
        return "[%r,%r]" %(self.x,self.y)

    def __getattr__(self,name) :
        print (f"the attrib {name} doesn't exist" )


    def __setattr__(self,name,value) :
        print (f"trying to set attribute {name}={value}") 
        self.__dict__[name] = value

    def __delattr__(self,name) :
        print (f"trying to delete {name} ")


a=Attr(1,1)
print (a)
print (a.w)
a.w=99
print (a.w)

del a.w