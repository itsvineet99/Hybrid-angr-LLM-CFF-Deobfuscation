/*
 * Real-world benchmark: OpenSSL / mbedTLS AES subround primitive
 * Performs affine S-Box substitution loop, non-linear conditional diffusion, and round key XOR.
 */

int printf(const char *format, ...);
unsigned long strtoul(const char *str, char **endptr, int base);

unsigned int aes_subround(unsigned int state_word, unsigned int round_key) {
    unsigned int res = 0;
    int i = 0;
    while (i < 4) {
        unsigned char b = (unsigned char)((state_word >> (i * 8)) & 0xFF);
        unsigned char s = (unsigned char)(b ^ 0x63);
        if (b & 0x80) {
            s = (unsigned char)((s << 1) ^ 0x1B);
        } else {
            s = (unsigned char)(s << 1);
        }
        unsigned char sbox = (unsigned char)(s ^ (b >> 4) ^ 0x05);
        res |= ((unsigned int)sbox) << (i * 8);
        i++;
    }
    return res ^ round_key;
}

int main(int argc, char **argv) {
    if (argc < 3) {
        printf("Usage: %s <state_word> <round_key>\n", argv[0]);
        return 1;
    }
    unsigned int state_word = (unsigned int)strtoul(argv[1], 0, 0);
    unsigned int round_key = (unsigned int)strtoul(argv[2], 0, 0);

    unsigned int res = aes_subround(state_word, round_key);
    printf("0x%08X\n", res);
    return 0;
}