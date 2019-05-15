import os
import socket

#User can define `MM_SERIALIZATION_TYPE` before import to choose serialization type:
#   "pickle" (Pickle/cPickle): the standard Python (de)serialization method.  Security vulnerabilities make
#       it unsuitable for network use.
#   "json" (JSON): Comparable speed/size to pickle, but without the security vulnerabilities.  Default.
#   "msgpack": Message Pack; a high-performance (de)serialization library.  Easily-installable with
#       `pip install msgpack`, but not the default because of that.
if "MM_SERIALIZATION_TYPE" not in os.environ:
    os.environ["MM_SERIALIZATION_TYPE"] = "json"
if   os.environ["MM_SERIALIZATION_TYPE"] == "pickle":
    #print("Using pickle")
    try:    import cPickle as pickle #Only present in Python 2.*; Python 3 automatically imports the
    except: import  pickle as pickle #new equivalent of cPickle, if it's available.
    def _mm_deserialize(data):
        return pickle.loads(data)
    def _mm_serialize(data):
        return pickle.dumps(data,protocol=pickle.HIGHEST_PROTOCOL)
elif os.environ["MM_SERIALIZATION_TYPE"] == "json":
    #print("Using json")
    import json
    def _mm_deserialize(data):
        return json.loads(data)
    def _mm_serialize(data):
        return json.dumps(data).encode()
elif os.environ["MM_SERIALIZATION_TYPE"] == "msgpack":
    #print("Using msgpack")
    import msgpack
    def _mm_deserialize(data):
        return msgpack.unpackb(data,raw=False)
    def _mm_serialize(data):
        return msgpack.packb(data,use_bin_type=True)
else:
    assert False
    
import zlib

from _mm_constants import *


def mastermind_get_hostname():
    return socket.gethostname()
def mastermind_get_local_ip():
    return socket.gethostbyname(mastermind_get_hostname())

def packet_send(socket,protocol_and_udpaddress, data,compression): #E.g.: =(MM_TCP,None)
    if   compression ==  False: compression = 0
    elif compression ==   None: compression = 0
    elif compression ==   True: compression = 9
    elif compression == MM_MAX: compression = 9

    data_to_send = str(compression).encode() #length is now 1

    data_str = _mm_serialize(data)
    if compression != 0:
        data_str = zlib.compress(data_str,compression)

    length_str = str(len(data_str)).encode()
    data_to_send += (16-len(length_str))*b" "
    data_to_send += length_str #length is now 17
    data_to_send += data_str #length is now 17+len(data_str)

    try:
        if protocol_and_udpaddress[0] == MM_TCP:
            socket.sendall(data_to_send)
        else:
            if protocol_and_udpaddress[1] == None:
                socket.sendall(data_to_send)
            else:
                socket.sendto(data_to_send, protocol_and_udpaddress[1])
        return True
    except:
        return False
def packet_recv_tcp(socket):
    #TODO: In all this, if recv returns 0, then shutdown *nicely*
    info = b""
    try:
        while len(info) < 17:
            got = socket.recv( 17 - len(info) )
            if got == b"": return (None,False)
            info += got
    except:
        return (None,False)

    compression = int(info[0:1])
    length = int(info[1:])

    data_str = b""
    try:
        while len(data_str) < length:
            got = socket.recv( length - len(data_str) )
            if got == b"": return (None,False)
            data_str += got
    except:
        return (None,False)
    if compression != 0:
        data_str = zlib.decompress(data_str)

    data = _mm_deserialize(data_str)
    
    return data,True
def packet_recv_udp(socket,max_packet_size):
    data_str,address = socket.recvfrom(max_packet_size)
    info = data_str[0:17]
    data_str = data_str[17:]

    compression = int(info[0:1])
    length = int(info[1:])

    if compression != 0:
        data_str = zlib.decompress(data_str)
    
    data = _mm_deserialize(data_str)
    
    return data,address
