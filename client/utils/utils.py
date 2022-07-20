import struct


from pb.pd_class import BasePb, msg_types


def encode_msg(msg_type, msg: dict):
    msg_id = list(msg_types.keys()).index(msg_type)
    msg_name = msg_types.get(msg_type, None)
    msg_class: BasePb = msg_name() if msg_type else None
    if msg_class is None:
        return None
    msg_class.set_val(**msg)
    msg_id_bytes = (msg_id).to_bytes(2, byteorder='big')
    return msg_id_bytes + msg_class.encode()


def encode_msg_class(msg_type, msg_class):
    msg_id = list(msg_types.keys()).index(msg_type)
    msg_id_bytes = (msg_id).to_bytes(2, byteorder='big')
    return msg_id_bytes + msg_class.encode()


def decode_msg(msg):
    msg_type_bytes = msg[:2]
    # 大端序解码, 返回元组
    msg_type_id = struct.unpack('>H', msg_type_bytes)[0]
    msg_class_obj = msg_types[list(msg_types.keys())[msg_type_id]]
    if not msg_class_obj:
        return None
    msg_info_bytes = msg[2:]
    msg_class = msg_class_obj()
    msg_class.decode(msg_info_bytes)
    return msg_class


