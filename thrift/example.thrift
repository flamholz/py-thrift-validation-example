/**
 * @author Avi Flamholz (flamholz@gmail.com)
 * This file contains some example Thrift structures used to
 * show some of the failings of Thrift in Python.
 * 
 * @version 0.1
 */
 
namespace cpp avi.thrift.validation.example
namespace java avi.thrift.validation.example
namespace py avi.thrift.validation.example


struct Point {
	1: required double x;
	2: required double y;
}


struct Place {
	1: required string name;
	2: required Point location;
	3: optional string review;
}

