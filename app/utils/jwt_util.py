import jwt
import datetime
from typing import Optional, Dict

class JWTUtil:
    SECRET_KEY = 'your-secret-key'  # 建议使用环境变量管理
    ALGORITHM = 'HS256'
    EXPIRE_SECONDS = 3600  # 默认过期时间：1小时

    @classmethod
    def generate_token(cls, payload: Dict, expire_seconds: Optional[int] = None) -> str:
        """
        生成 JWT Token
        :param payload: 自定义数据字典
        :param expire_seconds: 可选，token过期时间（秒）
        :return: JWT字符串
        """
        expire = datetime.datetime.utcnow() + datetime.timedelta(seconds=expire_seconds or cls.EXPIRE_SECONDS)
        payload_to_encode = payload.copy()
        payload_to_encode['exp'] = expire
        token = jwt.encode(payload_to_encode, cls.SECRET_KEY, algorithm=cls.ALGORITHM)
        return token

    @classmethod
    def decode_token(cls, token: str) -> Optional[Dict]:
        """
        解析并验证 JWT Token
        :param token: JWT字符串
        :return: 解码后的payload字典，若验证失败则返回None
        """
        try:
            decoded = jwt.decode(token, cls.SECRET_KEY, algorithms=[cls.ALGORITHM])
            return decoded
        except jwt.ExpiredSignatureError:
            print("Token已过期")
        except jwt.InvalidTokenError:
            print("无效的Token")
        return None
