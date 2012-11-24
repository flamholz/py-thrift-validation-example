#!/usr/bin/python

from util import validation

from thrift.protocol.TProtocol import TProtocolException
from avi.thrift.validation.test.ttypes import TestMessage, EmbeddedMessage

import unittest


class TestThriftUtil(unittest.TestCase):
        
    def testDeepValidate(self):
        m = TestMessage(id=1, name='avi')
        validation.DeepValidate(m)
        
        # Should fail - embedded.timestamp unset.
        embedded = EmbeddedMessage()
        m.embedded = embedded
        self.assertRaises(TProtocolException,
                          validation.DeepValidate, m)
        
        # Should pass now.
        embedded.timestamp = 1
        validation.DeepValidate(m)
        
        # Should fail - map contains invalid embedded message.
        embedded2 = EmbeddedMessage()
        m.map_embedded = {9: embedded2}
        self.assertRaises(TProtocolException,
                          validation.DeepValidate, m)
        
        # Should pass now.
        embedded2.timestamp = 2
        validation.DeepValidate(m)
        
        # Should still pass
        m.map_embedded[10] = embedded2
        validation.DeepValidate(m)
        
        # Should fail - list contains invalid message.
        embedded3 = EmbeddedMessage()
        m.list_embdedded = [embedded3]
        self.assertRaises(TProtocolException,
                          validation.DeepValidate, m)
        
        # Should pass now.
        embedded3.timestamp = 3
        validation.DeepValidate(m)
        
        
if __name__ == '__main__':
    unittest.main()
