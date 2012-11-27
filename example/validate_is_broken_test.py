#!/usr/bin/python

from avi.thrift.validation.example.ttypes import Point, Place

import unittest


class TestThriftUtil(unittest.TestCase):

    def testSimpleCase(self):
        """When using a simple structure like Point, everything works fine."""
        # point.x and point.y are required and unset
        point = Point()
        self.assertRaises(Exception, point.validate)

        # point.y is required and unset
        point.x = 1.0
        self.assertRaises(Exception, point.validate)

        # both point.x and point.y are set, so point is valid.
        point.y = 1.2
        point.validate()

        # But here's something weird you should know about:
        # point.x is supposed to be a double, but if you set
        # to a string it will still validate
        point.x = 'this is not a double'
        point.validate()

    def testValidateOnComplexStructure(self):
        """Built-in validate() makes less sense on a complex structure."""

        place = Place()
        self.assertRaises(Exception, place.validate)

        # Name is insufficient - location is required as well.
        place.name = 'avis place'
        self.assertRaises(Exception, place.validate)

        # Location and name are the only required fields.
        # However, validate doesn't descend into the Point
        # and check that it too is valid. So I can set
        # place.location to an empty point and validate is
        # satisfied.
        place.location = Point()
        place.validate()

        # Worse yet, I can make it a string and that is also no problem.
        place.location = 'this is not a point'
        place.validate()


if __name__ == '__main__':
    unittest.main()
