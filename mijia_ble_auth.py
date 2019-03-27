import random

def encrypt(key, data):
    # KSA
    key_length = len(key)
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % key_length]) % 256
        S[i], S[j] = S[j], S[i]

    # PRGA
    j = 0
    keystream = []
    for i in range(len(data)):
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        keystream.append(S[(S[i] + S[j]) % 256])

    # Encrypt
    return bytes(a ^ b for a, b in zip(data, keystream))

class login:
    def __init__(self, token):
        self.token = token

    def init_ekey(self, challenge):
        tick = encrypt(self.token, challenge)
        self.ekey = bytes(a ^ b for a, b in zip(token[0:4], tick[0:4]))

    def get_response(self, challenge):
        self.init_ekey(challenge)
        return encrypt(self.ekey, b'\x93\xbf\xac\x09')

    def check_confirmation(self, confirmation):
        return encrypt(self.ekey, confirmation)[0:4] == b'\x36\x9a\x58\xc9'

class register:
    def __init__(mac, productid):
        self.mac = mac
        self.productid = productid
        self.token = bytearray(random.getrandbits(8) for _ in range(size))

    def mix_a(self):
        return bytes([self.mac[0], self.mac[2], self.mac[5], (self.productid & 0xff), (self.productid & 0xff), self.mac[4], self.mac[5], self.mac[1]])

    def mix_b(self):
        return bytes([self.mac[0], self.mac[2], self.mac[5], ((self.productid >> 8) & 0xff), self.mac[4], self.mac[0], self.mac[5], (self.productid & 0xff)])

    def get_token(self):
        return self.token

    def get_init(self):
        return encrypt(self.mix_a(), self.token)

    def check_confirmation(self, confirmation):
        return self.token == encrypt(self.mix_b(), encrypt(self.mix_a(), confirmation))

    def get_end(self):
        return encrypt(self.token, b'\xfa\x54\xab\x92')
