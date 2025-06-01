from flask import jsonify


class Result:
    def __init__(self, code=None, message=None, data=None):
        self.code = code
        self.message = message
        self.data = data

    @staticmethod
    def success(message, data=None):
        return Result(code=0, message=message, data=data)

    @staticmethod
    def fail(message):
        return Result(code=1, message=message)

    def __repr__(self):
        return f"<Result  code={self.code} , message={self.message}, data={self.data}>"

    def to_dict_json(self):
        return jsonify({"code": self.code, "message": self.message, "data": self.data})
