#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int coreutils_base64_encode_block(unsigned int b0, unsigned int b1, unsigned int b2,
                                  int len, char *out) {
    static const char base64_table[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
    int i = 0;

    // Encode first 6-bit group from b0
    out[i++] = base64_table[(b0 >> 2) & 0x3F];

    // Encode second 6-bit group from b0 and b1
    if (len > 1) {
        out[i++] = base64_table[((b0 & 0x03) << 4) | ((b1 >> 4) & 0x0F)];
    }

    // Encode third 6-bit group from b1 and b2
    if (len > 2) {
        out[i++] = base64_table[((b1 & 0x0F) << 2) | ((b2 >> 6) & 0x03)];
    }

    // Encode fourth 6-bit group from b2
    if (len > 3) {
        out[i++] = base64_table[b2 & 0x3F];
    } else if (len == 3) {
        out[i++] = '=';
    } else if (len == 2) {
        out[i++] = '=';
        out[i++] = '=';
    }

    return i;
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
