#!/usr/bin/python

from thrift.protocol import TBinaryProtocol
from thrift.transport import TTransport


def SerializeThriftMsg(msg, protocol_type=TBinaryProtocol.TBinaryProtocol):
    """Serialize a thrift message using the given protocol.
    
    The default protocol is binary.
    
    Args:
        msg: the Thrift object to serialize.
        protocol_type: the Thrift protocol class to use.
    
    Returns:
        A string of the serialized object.
    """
    msg.validate()
    transportOut = TTransport.TMemoryBuffer()
    protocolOut = protocol_type(transportOut)
    msg.write(protocolOut)
    return transportOut.getvalue()


def DeserializeThriftMsg(msg, data,
                         protocol_type=TBinaryProtocol.TBinaryProtocol):
    """Deserialize a thrift message using the given protocol.
    
    The default protocol is binary.
    
    Args:
        msg: the Thrift object to serialize.
        data: the data to read from.
        protocol_type: the Thrift protocol class to use.
    
    Returns:
        Message object passed in (post-parsing).
    """
    transportIn = TTransport.TMemoryBuffer(data)
    protocolIn = protocol_type(transportIn)
    msg.read(protocolIn)
    msg.validate()
    return msg

