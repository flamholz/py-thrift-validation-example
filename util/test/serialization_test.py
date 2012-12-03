#!/usr/bin/python

from util import serialization

from thrift.protocol.TProtocol import TProtocolException
from avi.thrift.validation.test.ttypes import TestMessage, EmbeddedMessage

import unittest


class SerializationTest(unittest.TestCase):
        
    def testSerializeFailure(self):
        m = TestMessage()
        self.assertRaises(
            TProtocolException, serialization.SerializeThriftMsg, m)
    
    def testDeserializeFailure(self):
        # Test simple string data.
        self.assertRaises(Exception, serialization.DeserializeThriftMsg,
                          TestMessage(), "data")
            
        # Test another message entirely.
        m = EmbeddedMessage(timestamp=1)
        data = serialization.SerializeThriftMsg(m)
        self.assertRaises(
            TProtocolException, serialization.DeserializeThriftMsg,
            TestMessage(), data)
    
    def testSerializeDeserialize(self):
        m = TestMessage(id=1, name='avi')
        out = serialization.SerializeThriftMsg(m)
        outm = serialization.DeserializeThriftMsg(TestMessage(), out)
        self.assertEquals(m, outm)
        
        embedded = EmbeddedMessage(timestamp=1)
        m.embedded = embedded
        out = serialization.SerializeThriftMsg(m)
        outm = serialization.DeserializeThriftMsg(TestMessage(), out)
        self.assertEquals(m, outm)
        
        
if __name__ == '__main__':
    unittest.main()
