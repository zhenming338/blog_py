import bcrypt


def bcrypt_encode(origin_str: str) -> str:
    # 将明文字符串编码成字节串，返回加密后的哈希字符串
    return bcrypt.hashpw(origin_str.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def bcrypt_check(origin_str: str, encode_str: str) -> bool:
    # 都需要是 bytes，decode 后传入是 str 所以要再 encode
    return bcrypt.checkpw(origin_str.encode("utf-8"), encode_str.encode("utf-8"))
