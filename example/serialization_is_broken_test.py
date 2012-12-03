#!/usr/bin/python

from util.serialization import DeserializeThriftMsg, SerializeThriftMsg
from avi.thrift.validation.example.ttypes import Point, Place, Review

import unittest
from thrift.protocol.TProtocol import TProtocolException


class TestThriftUtil(unittest.TestCase):

    def testSerializationChecksSomeTypes(self):
        """When using a simple structure like Point, everything works fine."""
        # Point has required fields. Serialization fails if you don't set them.
        point = Point()
        self.assertRaises(TProtocolException, SerializeThriftMsg, point)
        
        # Of course, serialization works when you set fields correctly.
        point.x, point.y = 1.0, 1.2
        SerializeThriftMsg(point)

        # Point.x is a double. If it's a string then you can't serialize.
        point.x = "asdf"
        self.assertRaises(Exception, SerializeThriftMsg, point)
        
        # Same is true for point.y
        point.y = "also a string"
        self.assertRaises(Exception, SerializeThriftMsg, point)
    
    def testSerializationDoesntCheckStructs(self):
        """However, there are some oddities when you embed structures."""
        # Can't serialize empty place as it has empty fields.
        place = Place()
        self.assertRaises(TProtocolException, SerializeThriftMsg, place)
        
        # If we set the required fields, everything is fine.
        place.name = "avi's place"
        place.location = Point(x=1.0, y=1.2)
        SerializeThriftMsg(place)

        # HOWEVER, we can set the Review struct to a Point and...
        place.review = Point(x=3.4, y=1.1)
        SerializeThriftMsg(place)
        
        # SIMILARLY, we can set the Point to a Review
        place.location = Review(rating=4, text="this place is pretty great")
        SerializeThriftMsg(place)
        

if __name__ == '__main__':
    unittest.main()
