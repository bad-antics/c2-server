"""Encryption for C2 communications"""
import hashlib, os, base64

class C2Crypto:
    def __init__(self, key=None):
        self.key = key or os.urandom(32)
    
    def encrypt(self, data):
        if isinstance(data, str): data = data.encode()
        iv = os.urandom(16)
        keystream = self._keystream(self.key, iv, len(data))
        ct = bytes(a ^ b for a, b in zip(data, keystream))
        tag = hashlib.sha256(self.key + iv + ct).digest()[:16]
        return base64.b64encode(iv + ct + tag).decode()
    
    def decrypt(self, data):
        raw = base64.b64decode(data)
        iv, ct, tag = raw[:16], raw[16:-16], raw[-16:]
        expected = hashlib.sha256(self.key + iv + ct).digest()[:16]
        if tag != expected: raise ValueError("Decryption failed - tampered data")
        keystream = self._keystream(self.key, iv, len(ct))
        return bytes(a ^ b for a, b in zip(ct, keystream))
    
    def _keystream(self, key, iv, length):
        stream = b""
        ctr = bytearray(iv)
        while len(stream) < length:
            stream += hashlib.sha256(key + bytes(ctr)).digest()
            ctr[-1] = (ctr[-1] + 1) % 256
        return stream[:length]
