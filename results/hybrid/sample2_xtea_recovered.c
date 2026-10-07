#include <stdio.h>
#include <stdlib.h>
#include <string.h>
unsigned int sample2_xtea_round(unsigned int v0, unsigned int v1, unsigned int k0, unsigned int k1) {
    unsigned int sum = 0x9E3779B9U;
    unsigned int res = v0;

    if (v1 & 1U) {
        res += (((v1 << 4) ^ (v1 >> 5)) + v1) ^ (sum + k0);
    } else {
        res += (((v1 << 3) ^ (v1 >> 4)) + v1) ^ (sum + k1);
    }

    if (res > 0x7FFFFFFFU) {
        res = (res << 1) ^ 0x1BU;
    } else {
        res = (res >> 1) + 0x42U;
    }
    return res;
}

int main(int argc, char **argv) {
    if (argc < 5) {
        printf("Usage: %s <v0> <v1> <k0> <k1>\n", argv[0]);
        return 1;
    }
    unsigned int v0 = (unsigned int)strtoul(argv[1], 0, 0);
    unsigned int v1 = (unsigned int)strtoul(argv[2], 0, 0);
    unsigned int k0 = (unsigned int)strtoul(argv[3], 0, 0);
    unsigned int k1 = (unsigned int)strtoul(argv[4], 0, 0);
    unsigned int out_val = sample2_xtea_round(v0, v1, k0, k1);
    printf("0x%08X\n", out_val);
    return 0;
}
