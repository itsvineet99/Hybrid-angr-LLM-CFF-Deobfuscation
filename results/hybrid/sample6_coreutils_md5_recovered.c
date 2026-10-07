#include <stdio.h>
#include <stdlib.h>
#include <string.h>
unsigned int coreutils_md5_step(unsigned int a, unsigned int b, unsigned int c,
                                unsigned int d, unsigned int x, unsigned int s,
                                unsigned int ac, int round_type) {
    unsigned int f = 0;
    if (round_type == 0) {
        /* F(b, c, d) = (b & c) | (~b & d) */
        f = (b & c) | ((~b) & d);
    } else if (round_type == 1) {
        /* G(b, c, d) = (b & d) | (c & ~d) */
        f = (b & d) | (c & (~d));
    } else if (round_type == 2) {
        /* H(b, c, d) = b ^ c ^ d */
        f = b ^ c ^ d;
    } else {
        /* I(b, c, d) = c ^ (b | ~d) */
        f = c ^ (b | (~d));
    }

    a += f + x + ac;
    /* Circular left shift */
    a = (a << s) | (a >> (32 - s));
    a += b;
    return a;
}

int main(int argc, char **argv) {
    if (argc < 9) {
        printf("Usage: %s <a> <b> <c> <d> <x> <s> <ac> <round_type>\n", argv[0]);
        return 1;
    }
    unsigned int a = (unsigned int)strtoul(argv[1], 0, 0);
    unsigned int b = (unsigned int)strtoul(argv[2], 0, 0);
    unsigned int c = (unsigned int)strtoul(argv[3], 0, 0);
    unsigned int d = (unsigned int)strtoul(argv[4], 0, 0);
    unsigned int x = (unsigned int)strtoul(argv[5], 0, 0);
    unsigned int s = (unsigned int)strtoul(argv[6], 0, 0);
    unsigned int ac = (unsigned int)strtoul(argv[7], 0, 0);
    int round_type = (int)strtoul(argv[8], 0, 0);

    unsigned int res = coreutils_md5_step(a, b, c, d, x, s, ac, round_type);
    printf("0x%08X\n", res);
    return 0;
}
