from particular_admin.app import db
from particular_admin.util.crypto import hash_to_id, id_to_hash


class Base(object):
    class ValidationError(Exception):
        pass

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class HashIdsBase(object):
    @classmethod
    def hash_to_id(cls, id_hash):
        return hash_to_id(id_hash, salt=cls.HASH_IDS_SALT)

    @property
    def hash_id(self):
        return id_to_hash(self.id, salt=self.HASH_IDS_SALT)
