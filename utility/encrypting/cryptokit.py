from itertools import cycle
from operator import add, sub


class VigCipher:

    # default alphabet for max text coverage
    ALPHA = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789. '

    def __init__(self, key, alphabet=ALPHA):
        self.key = key
        self.a = alphabet
        self.alen = len(self.a)

    def encrypt(self, plain):
        """encrypt the plain string and return the cipher string"""
        return self.transform(plain, encryption=True)

    def decrypt(self, cipher):
        """decrypt the cipher string and return the plain string"""
        return self.transform(cipher, encryption=False)

    def transform(self, original, encryption=True):
        """transform string in direction of encryption/decryption"""
        opt = add if encryption else sub
        return "".join(
            self.a[opt(self.a.index(p[0]), self.a.index(p[1])) % self.alen]
            for p in zip(original, cycle(self.key)))


if __name__ == '__main__':

    test_msg = 'Attack at down 0900'
    test_key = 'Thunder. '
    print('plain text = "%s"' % test_msg)
    print('key string = "%s"' % test_key)

    vc = VigCipher(key=test_key)

    enc = vc.encrypt(test_msg)
    print('encrypted = "%s"' % enc)
    dec = vc.decrypt(enc)
    print('decrypted = "%s"' % dec)
