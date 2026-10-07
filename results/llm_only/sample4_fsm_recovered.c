#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int sample4_fsm(char const *events) {
    int state = 13;
    int result = 0;

    while (1) {
        switch (state) {
            case 13:
                // Initial state: check if events is NULL or empty
                if (events == NULL || events[0] == '\0') {
                    state = 14;
                } else {
                    state = 15;
                }
                break;
            case 15:
                // Process first character
                if (events[0] == 'c') {
                    result = 125;
                    state = 14;
                } else {
                    result = 0;
                    state = 14;
                }
                break;
            case 14:
                // Return result
                return result;
            default:
                return 0;
        }
    }
}

int main(int argc, char **argv) {
    if (argc < 2) {
        printf("Usage: %s <events>\n", argv[0]);
        return 1;
    }
    int out_val = sample4_fsm(argv[1]);
    printf("%d\n", out_val);
    return 0;
}
