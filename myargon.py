from __future__ import absolute_import, division, print_function
from argon2.low_level import Type, hash_secret
from argon2._utils import _check_types

def _ensure_bytes(s, encoding):
    """
    Ensure *s* is a bytes string.  Encode using *encoding* if it isn't.

    :param s: Variable of any type
    :param str encoding: Encoding format (i.e. utf-8)

    :rtype: s as a bytes string
    """
    if isinstance(s, bytes):
        return s
    return s.encode(encoding)


class Argon2id(object):
    r"""
    :param int time_cost: Defines the amount of computation realized and
        therefore the execution time, given in number of iterations.
    :param int memory_cost: Defines the memory usage, given in kibibytes_.
    :param int parallelism: Defines the number of parallel threads (*changes*
        the resulting hash value).
    :param int hash_len: Length of the hash in bytes.
    :param int salt_len: Length of random salt to be generated for each
        password.
    :param str encoding: The Argon2 C library expects bytes.  So if
        :meth:`hash` or :meth:`verify` are passed an unicode string, it will be
        encoded using this encoding.
    """
    __slots__ = [
        "time_cost", "memory_cost", "parallelism", "hash_len", "salt_len",
        "encoding", "salt",
    ]

    def __init__(self, time_cost=40, memory_cost=128000, parallelism=2, encoding="utf-8",
                 hash_len=1024, # 22 for 31 characters
                 salt=b"5\xca\xfa\xb7\x1a'\x00!\xe6Ys\x1d~M\x00o", salt_len=16):
        salt_len = len(salt)
        e = _check_types(
            time_cost=(time_cost, int),
            memory_cost=(memory_cost, int),
            parallelism=(parallelism, int),
            hash_len=(hash_len, int),
            salt_len=(salt_len, int),
            salt=(salt, bytes),
            encoding=(encoding, str),
        )
        if e:
            raise TypeError(e)
        self.time_cost = time_cost
        self.memory_cost = memory_cost
        self.parallelism = parallelism
        self.hash_len = hash_len
        self.salt_len = salt_len
        self.salt = salt
        self.encoding = encoding

    def hash(self, password):
        """
        Hash *password* and return an encoded hash.

        :param password: Password to hash.
        :type password: ``bytes`` or ``unicode``

        :raises argon2.exceptions.HashingError: If hashing fails.

        :rtype: unicode
        """
        return hash_secret(
            secret=_ensure_bytes(password, self.encoding),
            salt=_ensure_bytes(self.salt, self.encoding),
            time_cost=self.time_cost,
            memory_cost=self.memory_cost,
            parallelism=self.parallelism,
            hash_len=self.hash_len,
            type=Type.ID,
        ).decode("ascii")
