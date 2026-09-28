int printf(const char *format, ...);
unsigned long strtoul(const char *str, char **endptr, int base);

unsigned int sample1_bitmix(unsigned int val) {
    unsigned int acc = val;
    if (acc & 1U) {
        acc = (acc << 5) | (acc >> 27);
        acc ^= 0x5A5A5A5AU;
    } else {
        acc = (acc >> 3) | (acc << 29);
        acc += 0x12345678U;
    }

    if (acc & 0x80000000U) {
        acc = ~acc;
        acc = (acc * 33U) + 7U;
    } else {
        acc = (acc * 17U) ^ 0xCAFEBABE0U;
    }
    return acc;
}

int main(int argc, char **argv) {
    if (argc < 2) {
        printf("Usage: %s <uint32>\n", argv[0]);
        return 1;
    }
    unsigned int in_val = (unsigned int)strtoul(argv[1], 0, 0);
    unsigned int out_val = sample1_bitmix(in_val);
    printf("0x%08X\n", out_val);
    return 0;
}
