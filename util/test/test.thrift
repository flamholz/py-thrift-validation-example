/**
 * @author Avi Flamholz (flamholz@ridewithvia.com)
 * Structures used for testing recursive validation.
 */
 
namespace cpp avi.thrift.validation.test
namespace java avi.thrift.validation.test
namespace py avi.thrift.validation.test


struct EmbeddedMessage {
	1: required i32 timestamp;
}

struct TestMessage {
	1: required i32 id;
	2: required string name;
	3: optional EmbeddedMessage embedded;
	4: optional map<i32, EmbeddedMessage> map_embedded;
	5: optional list<EmbeddedMessage> list_embdedded;
}
