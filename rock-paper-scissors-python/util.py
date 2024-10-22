def str2hex(str):
    return "0x" + str.encode("utf-8").hex()

def hex2str(hex):
    return bytes.fromhex(hex[2:])