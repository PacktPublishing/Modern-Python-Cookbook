"""Python Cookbook

Chapter 12, recipe 7 -- server.

Define the user and their credentials.
"""
import hashlib
import os
import base64

class User:
    '''
    An individual user's information and password.

    >>> details = {'name': 'xander', 'email': 'x@example.com',
    ...     'year': 1985, 'twitter': 'https://twitter.com/PacktPub' }
    >>> u = User(**details)
    >>> u.set_password('OpenSesame')
    >>> u.check_password('opensesame')
    False
    >>> u.check_password('OpenSesame')
    True
    >>> u.password  # doctest: +SKIP
    'sha384$71wZJlWxXqN93ZozJEPzxF2v9ZiSXWchGLS1XQzL$pjV2rcVt0M1s4zLfOkU9cafp_2tBFkRIIvjaj9jAZHuaFMUAH6ebU3dGvxqEQCvF'
    '''
    DIGEST = 'sha384'
    ROUNDS = 100000
    def __init__(self, **document):
        self.name = document['name']
        self.year = document['year']
        self.email = document['email']
        self.twitter = document['twitter']
        self.password = None

    def set_password(self, password):
        salt = os.urandom(30)
        hash = hashlib.pbkdf2_hmac(
            self.DIGEST, password.encode('utf-8'), salt, self.ROUNDS)
        self.password = '$'.join(
            [self.DIGEST,
             base64.urlsafe_b64encode(salt).decode('ascii'),
             base64.urlsafe_b64encode(hash).decode('ascii')
            ]
        )

    def check_password(self, password):
        digest, b64_salt, b64_expected_hash = self.password.split('$')
        salt = base64.urlsafe_b64decode(b64_salt)
        expected_hash = base64.urlsafe_b64decode(b64_expected_hash)
        computed_hash = hashlib.pbkdf2_hmac(
            digest, password.encode('utf-8'), salt, self.ROUNDS)
        return computed_hash == expected_hash

    def to_json(self):
        return vars(self)

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=1)
