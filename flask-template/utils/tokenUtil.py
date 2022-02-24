import time
import jwt

class TokenHelper(object):
    exptime = time.time() + 60 * 30 * 2 * 24 * 3
    secret = 'iam'

    def __init__(self):
        pass

    @classmethod
    def encrpyt_token(cls, username):
        """
        iss：该JWT的签发者，是否使用是可以选择的。
        sub：该JWT所面向的用户，是否使用是可选的。
        aud：接收该JWT的一方，是否使用是可选的。
        exp（expires）：什么时候过期，是一个UNIX的时间戳，是否使用是可选的。默认设置为：30分钟
        iat（issued at）：在什么时候签发UNIX时间，是否使用是可选的。
        nbf（not before）：如果当前时间在nbf的时间之前，则Token不被接受，一般都会留几分钟，是否使用是可选的。
        :return:
        """
        payloads = {
            'iss': 'issue by class Token',
            'sub': 'sub for all user when trying to login',
            'iat': time.time(),
            'username':username,
            "exp": cls.exptime
        }
        encoded_jwt = jwt.encode(payloads, cls.secret, algorithm='HS256')
        return encoded_jwt

    @classmethod
    def decrypt_token(cls, token):
        """
        encoded_jwt = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJJQU0gSldUIEJ1aWxkZXIiLCJpYXQiOjE1ODQzNDA0NjkuOTE5ODQxLCJ1c2VybmFtZSI6Inl1bGlhbmh1aTEiLCJ1dWlkIjoiOTQwYjBhZTgtNWEwNi0xMWVhLWEzNWItZjEwNWMyOGI2NDE2IiwiZXhwIjoxNTg0MzQyMjY5LjkxOTg0MX0.zITnwaB0zsuyO1kiyYBG5IFWEy5FewDGSJAj1eJ-uEg'
        decode_jwt = jwt.decode(encoded_jwt, 'iam', algorithms=['HS256'])
        print('decode_jwt',decode_jwt)
        :param token:
        :param secret:
        :return:
        """
        try:
            decode_jwt = jwt.decode(token, cls.secret, algorithms=['HS256'])
            return decode_jwt
        except jwt.exceptions.InvalidSignatureError as e:
            return {'error':'Signature verification failed'}

if __name__ == "__main__":
    # a = TokenHelper().encrpyt_token("username")
    a = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJpc3N1ZSBieSBjbGFzcyBUb2tlbiIsInN1YiI6InN1YiBmb3IgYWxsIHVzZXIgd2hlbiB0cnlpbmcgdG8gbG9naW4iLCJpYXQiOjE2Mjk1NDAzMjEuODA4NDQ4MywidXNlcm5hbWUiOiIxIiwiZXhwIjoxNjI5NTQyMTIxLjQzMjU1NTR9._gQ0fOlqhM-NzV_Ca3T5eyOtFedbwdApm-OkYr5y3Aw"
    # print(a)
    a = TokenHelper().decrypt_token(a)
    print(a)
    

