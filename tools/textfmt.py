"""Read/write the two string containers used by the game.
text_mod.bin : u16 count, then entries [u16 len+2][u16 len][utf8]
outt_b       : 3-byte header, then blocks [u16 size][u16 count] entries..."""
import struct

def _entry(d, p):
    a, b = struct.unpack('>HH', d[p:p+4]); assert a == b + 2
    return d[p+4:p+4+b].decode('utf-8'), p + 4 + b

def _pack(s):
    b = s.encode('utf-8'); return struct.pack('>HH', len(b) + 2, len(b)) + b

def read_textmod(d):
    n = struct.unpack('>H', d[:2])[0]; p = 2; out = []
    for _ in range(n):
        s, p = _entry(d, p); out.append(s)
    return out, d[p:]  # tail = event script bytecode, kept verbatim

def write_textmod(strs, tail):
    return struct.pack('>H', len(strs)) + b''.join(_pack(s) for s in strs) + tail

def read_outt(d):
    head = d[:3]; p = 3; blocks = []
    while p < len(d):
        size, cnt = struct.unpack('>HH', d[p:p+4]); end = p + 2 + size; p += 4
        blk = []
        for _ in range(cnt):
            s, p = _entry(d, p); blk.append(s)
        assert p == end, (hex(p), hex(end))
        blocks.append(blk)
    return head, blocks

def write_outt(head, blocks):
    out = bytearray(head)
    for blk in blocks:
        body = b''.join(_pack(s) for s in blk)
        assert len(body) + 2 < 0x10000
        out += struct.pack('>HH', len(body) + 2, len(blk)) + body
    return bytes(out)
