#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/*
 * Score Quest - a "fair" game that is impossible to win by playing.
 * Reach the target score and the flag is revealed.
 */
#define TARGET (1000 * 1000)            /* 1,000,000 - unreachable by guessing */

static const unsigned char ENC[] = { 0x35, 0x0f, 0x0e, 0x15, 0x1e, 0x23, 0x46, 0x13, 0x40, 0x06, 0x2c, 0x61, 0x1a, 0x6c, 0x25, 0x02, 0x48, 0x31, 0x01, 0x03, 0x40, 0x07, 0x3d, 0x04, 0x30, 0x43, 0x16, 0x0e, 0x01, 0x0d, 0x40, 0x2b, 0x6f, 0x3c, 0x74, 0x26, 0x14, 0x12, 0x4d, 0x26, 0x4f };
static const char KEY[] = "ScoreQuest_RE_Key_2026";
static const size_t FLAG_LEN = sizeof(ENC) - 1;

static void maybe_reveal(int score) {
    if (score >= TARGET) {
        for (size_t i = 0; i < FLAG_LEN; i++)
            putchar(ENC[i] ^ (unsigned char)KEY[i % (sizeof(KEY) - 1)]);
        putchar('\n');
    } else {
        printf("Current score: %d / %d needed to win.\n", score, TARGET);
    }
}

int main(void) {
    int score = 0;
    char buf[64];
    srand((unsigned)score + 1337);

    printf("=== SCORE QUEST ===\n");
    printf("Guess the secret number (1-10). Correct guess: +5 points.\n");
    printf("Reach the target score to win a prize.\n\n");

    while (1) {
        printf("Your guess (or 'q' to quit): ");
        if (!fgets(buf, sizeof(buf), stdin)) break;
        buf[strcspn(buf, "\n")] = 0;
        if (buf[0] == 'q' || buf[0] == 'Q') break;

        int guess = atoi(buf);
        int secret = (rand() % 10) + 1;   /* the house always knows */

        if (guess == secret) {
            score += 5;
            printf("Correct! +5\n");
        } else {
            printf("Wrong (secret was %d). No points.\n", secret);
        }
        maybe_reveal(score);
    }

    printf("Game over. Final score: %d (target %d).\n", score, TARGET);
    return 0;
}