#!/usr/bin/python

from thrift.Thrift import TType


RECURSE_ON = frozenset([TType.STRUCT,
                        TType.LIST,
                        TType.MAP,
                        TType.SET])


def _ShouldRecurse(ttype):
    """Returns True if this ttype is one we recurse on for validation."""
    return ttype in RECURSE_ON


def DeepValidate(msg):
    """Deep validation of thrift messages.
        
    Args:
        msg: a Thrift message.
    """
    assert msg is not None
    msg.validate()
    
    # Introspect the structure specification.
    # For each field, check type and decide whether to recurse.
    spec = msg.thrift_spec
    for spec_tuple in spec:
        if spec_tuple is None:
            continue
        
        mtype = spec_tuple[1]
        if not _ShouldRecurse(mtype):
            # Some primitive type that we don't validate.
            continue
        
        # Fetch the item itself.
        name = spec_tuple[2]
        attr = getattr(msg, name)
        if attr is None:
            return
        
        # Field is set and it's a message or collection, so we validate.
        if mtype == TType.STRUCT:
            DeepValidate(attr)
        elif mtype in (TType.LIST, TType.SET):
            subtype = spec_tuple[3][0]
            if _ShouldRecurse(subtype):
                for submsg in attr:
                    DeepValidate(submsg)
        elif mtype == TType.MAP:
            subtype = spec_tuple[3]
            key_type = subtype[0]
            val_type = subtype[2]
            for key, val in attr.iteritems():
                if _ShouldRecurse(key_type):
                    DeepValidate(key)
                if _ShouldRecurse(val_type):
                    DeepValidate(val)
