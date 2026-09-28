int printf(const char *format, ...);

int sample4_fsm(const char *events) {
    if (!events) {
        return -1;
    }
    int state = 0; /* 0: IDLE, 1: COIN_INSERTED, 2: SELECTION_MADE, 3: DISPENSED, 4: ERROR */
    int balance = 0;
    int i = 0;

    while (events[i] != '\0') {
        char ev = events[i];
        if (state == 0) {
            if (ev == 'c') {
                balance += 25;
                state = 1;
            }
        } else if (state == 1) {
            if (ev == 'c') {
                balance += 25;
            } else if (ev == 'b' && balance >= 50) {
                state = 2;
            } else if (ev == 'r') {
                balance = 0;
                state = 0;
            }
        } else if (state == 2) {
            if (ev == 'v') {
                balance -= 50;
                state = 3;
            } else if (ev == 'r') {
                balance = 0;
                state = 0;
            }
        } else if (state == 3) {
            if (ev == 'r') {
                state = 0;
            }
        } else {
            state = 4;
            break;
        }
        i++;
    }
    return (state * 100) + balance;
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
