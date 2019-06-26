#!/usr/bin/env python#!/usr/bin/env python
import unittest 
from handlers.cars import CarsHandler
 
class CarTest(unittest):


  def getTest(self):
    assert(CarsHandler.get(20),)




  def postTest(self):
    assert(CarsHandler.post(),)  




  def deleteTest(self):
    assert(CarsHandler.delete(),)

  def putTest(self):
    assert(CarsHandler.put(),)  

   def verifyTest(self):
    assert(CarsHandler.verify_data(),)  
