from sqlalchemy.ext.declarative import declared_attr
class BaseModel:

    @classmethod
    def from_dict(cls, data: dict):
        obj = cls()
        for k, v in data.items():
            if hasattr(obj, k):
                setattr(obj, k, v)
        return obj

    def to_dict(self):
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }
