/*
 * Real-world benchmark: GNU Coreutils Base64 block encoder primitive
 * Encodes up to 3 raw bytes into 4 base64 ASCII characters.
 */

int printf(const char *format, ...);
int sprintf(char *str, const char *format, ...);
unsigned long strtoul(const char *str, char **endptr, int base);

static const char b64_table[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";

int coreutils_base64_encode_block(unsigned int b0, unsigned int b1, unsigned int b2, int len, char *out) {
    if (len < 1 || len > 3 || !out) return -1;

    unsigned int triple = (b0 << 16) | ((len > 1 ? b1 : 0) << 8) | (len > 2 ? b2 : 0);

    out[0] = b64_table[(triple >> 18) & 0x3F];
    out[1] = b64_table[(triple >> 12) & 0x3F];
    out[2] = (len > 1) ? b64_table[(triple >> 6) & 0x3F] : '=';
    out[3] = (len > 2) ? b64_table[triple & 0x3F] : '=';
    out[4] = '\0';
    return 0;
}

int main(int argc, char **argv) {
    if (argc < 5) {
        printf("Usage: %s <b0> <b1> <b2> <len>\n", argv[0]);
        return 1;
    }
    unsigned int b0 = (unsigned int)strtoul(argv[1], 0, 0);
    unsigned int b1 = (unsigned int)strtoul(argv[2], 0, 0);
    unsigned int b2 = (unsigned int)strtoul(argv[3], 0, 0);
    int len = (int)strtoul(argv[4], 0, 0);

    char out[8];
    coreutils_base64_encode_block(b0, b1, b2, len, out);
    printf("%s\n", out);
    return 0;
}
