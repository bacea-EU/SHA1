def left_rotate(n, b):
    return ((n << b) | (n >> (32 - b))) & 0xFFFFFFFF

def sha1(s):
    message = bytearray(s, 'utf-8')
    orig_len_in_bits = (8 * len(message)) & 0xFFFFFFFFFFFFFFFF
    message.append(0x80)
    
    while (len(message) * 8 + 64) % 512 != 0:
        message.append(0)
    
    message += orig_len_in_bits.to_bytes(8, 'big')
    
    h0, h1, h2, h3, h4 = (
        0x67452301,
        0xEFCDAB89,
        0x98BADCFE,
        0x10325476,
        0xC3D2E1F0,
    )
    
    #512 bit chunks
    for i in range(0, len(message), 64):
        w = [0] * 80
        chunk = message[i:i + 64]
        
        for j in range(16):
            w[j] = int.from_bytes(chunk[j * 4:(j * 4) + 4], 'big')
        
        for j in range(16, 80):
            w[j] = left_rotate(w[j - 3] ^ w[j - 8] ^ w[j - 14] ^ w[j - 16], 1)
        
        a, b, c, d, e = h0, h1, h2, h3, h4
        
        for j in range(80):
            if 0 <= j <= 19:
                f = (b & c) | ((~b) & d)
                k = 0x5A827999
            elif 20 <= j <= 39:
                f = b ^ c ^ d
                k = 0x6ED9EBA1
            elif 40 <= j <= 59:
                f = (b & c) | (b & d) | (c & d)
                k = 0x8F1BBCDC
            else:
                f = b ^ c ^ d
                k = 0xCA62C1D6
            
            temp = (left_rotate(a, 5) + f + e + k + w[j]) & 0xFFFFFFFF
            e, d, c, b, a = d, c, left_rotate(b, 30), a, temp
        
        h0 = (h0 + a) & 0xFFFFFFFF
        h1 = (h1 + b) & 0xFFFFFFFF
        h2 = (h2 + c) & 0xFFFFFFFF
        h3 = (h3 + d) & 0xFFFFFFFF
        h4 = (h4 + e) & 0xFFFFFFFF
    
    return ''.join(f'{x:08x}' for x in [h0, h1, h2, h3, h4])



if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        s = sys.argv[1]
        print(f"SHA1('{s}') = {sha1(s)}")
    else:
        print("Usage: python script.py <string> OR \"<string>\"")
