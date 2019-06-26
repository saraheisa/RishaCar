#!/usr/bin/env python#!/usr/bin/env python
import unittest 
from handlers.drives import DrivesHandler
 
class CarTest(unittest):


  def getTest(self):
    assert(DrivesHandler.get(20),)




  def postTest(self):
    assert(DrivesHandler.post(),)  




  def deleteTest(self):
    assert(DrivesHandler.delete(),)

  def putTest(self):
    assert(DrivesHandler.put(),)  

   def verifyTest(self):
    assert(DrivesHandler.verify_data(),)