import hashlib

def DataHash(data: str, salt: str = None, algorithm: str = 'sha256') -> str:
    # 盐值不为空的情况下，加盐处理
    if salt is not None:
        data = data + salt
    # 将输入的字符串数据转换为字节
    data_bytes = data.encode('utf-8')
    
    # 根据algorithm选择哈希算法
    if algorithm.lower() == 'md5':
        hash_obj = hashlib.md5(data_bytes)
    elif algorithm.lower() == 'sha1':
        hash_obj = hashlib.sha1(data_bytes)
    elif algorithm.lower() == 'sha256':
        hash_obj = hashlib.sha256(data_bytes)
    else:
        raise ValueError(f"Unsupported hash algorithm: {algorithm}")
    
    # 返回十六进制格式的哈希字符串
    return hash_obj.hexdigest()