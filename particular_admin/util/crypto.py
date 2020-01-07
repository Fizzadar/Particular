import hmac

from hashlib import sha1, sha512
from uuid import uuid4

from bcrypt import gensalt, hashpw
from hashids import Hashids
from pydash import memoize

from particular_admin import settings


@memoize
def _get_hashids(salt, min_length):
    return Hashids(
        salt=salt,
        min_length=min_length,
    )


def id_to_hash(id, salt='', min_length=settings.HASH_IDS_MIN_LENGTH):
    return _get_hashids(salt, min_length).encode(id)


def hash_to_id(hash, salt='', min_length=settings.HASH_IDS_MIN_LENGTH):
    ids = _get_hashids(salt, min_length).decode(hash)

    if ids:
        return ids[0]


def generate_key():
    random_string = str(uuid4()).encode()
    return sha1(random_string).hexdigest()


def check_password(password, hashed):
    '''
    Checks a password matches its hashed (database) value in constant time.
    '''

    password = password.encode('utf-8')
    hashed = hashed.encode('utf-8')

    password = sha512(password).hexdigest()

    return hmac.compare_digest(
        hashpw(password, hashed),
        hashed,
    )


def hash_password(password):
    '''
    Turn a password into a hash.
    '''

    password = password.encode('utf-8')

    password = sha512(password).hexdigest()

    return hashpw(password, gensalt(settings.BCRYPT_ROUNDS))
