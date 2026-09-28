int printf(const char *format, ...);

int sample3_parser(const char *input) {
    if (!input || !*input) {
        return -1;
    }
    int state = 0;
    int value = 0;
    int sign = 1;
    int i = 0;

    while (input[i] != '\0' && input[i] != ';') {
        char c = input[i];
        if (c == ':') {
            state = 1;
        } else if (state == 0) {
            if (c >= 'A' && c <= 'Z') {
                value += (c - 'A' + 1) * 10;
            }
        } else if (state == 1) {
            if (c == '-') {
                sign = -1;
            } else if (c >= '0' && c <= '9') {
                value = (value * 10) + (c - '0');
            }
        }
        i++;
    }
    return value * sign;
}

int main(int argc, char **argv) {
    if (argc < 2) {
        printf("Usage: %s <string>\n", argv[0]);
        return 1;
    }
    int out_val = sample3_parser(argv[1]);
    printf("%d\n", out_val);
    return 0;
}