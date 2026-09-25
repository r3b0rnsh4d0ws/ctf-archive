/*
 * challenge.c  -  "Score Quest" reverse-engineering challenge.
 *
 * The game: guess a number (1-10), +100 per correct guess. Reaching the target
 * score of 100000 by playing normally is effectively impossible.
 *
 * The flag is stored ENCRYPTED (see flag_data.h) and is only ever decrypted in
 * RAM for the split second it is printed. It is never present in plaintext on
 * disk or in a memory dump taken during normal play.
 *
 * Anti-debug: if a debugger is detected, the decryption seed is corrupted so the
 * flag prints as garbage. This defeats "attach with gdb and read the flag" approaches.
 *
 * Intended solution: reverse-engineer the score gate and trigger the reveal
 * mechanism (e.g. patch the comparison / raise the score) so reveal_flag() runs
 * in a NON-debugged process.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stddef.h>
#include <time.h>

#ifdef _WIN32
#include <windows.h>
#else
#include <sys/ptrace.h>
#include <unistd.h>
#endif

#include "flag_data.h"

#define TARGET 100000

/* ---- SplitMix64 PRNG (keystream generator) ---- */
static unsigned long long splitmix64(unsigned long long *s) {
    *s += 0x9E3779B97F4A7C15ULL;
    unsigned long long z = *s;
    z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9ULL;
    z = (z ^ (z >> 27)) * 0x94D049BB133111EBULL;
    z = z ^ (z >> 31);
    return z;
}

/* ---- Obfuscated seed reconstruction ----
 * The seed is never stored as a single constant. It is rebuilt from scattered
 * pieces so it is not a trivial "find the constant" in a disassembler. */
static unsigned long long recover_seed(void) {
    unsigned long long seed = SEED_XOR ^ SEED_MASK;

    /* Fold in unrelated-looking constants (matches gen_flag.py). */
    static const unsigned long long PI_A = 0x243F6A8885A308D3ULL;
    static const unsigned long long PI_B = 0x13198A2E03707344ULL;
    seed ^= (PI_A + PI_B);
    return seed;
}

/* ---- Anti-debug ----
 * Returns non-zero when a debugger is attached. */
static int under_debugger(void) {
#ifdef _WIN32
    return IsDebuggerPresent();
#else
    /* PTRACE_TRACEME fails (-1) if a tracer is already present. */
    if (ptrace(PTRACE_TRACEME, 0, 0, 0) == -1)
        return 1;
    /* Detach so the process is not left traced. */
    ptrace(PTRACE_DETACH, 0, 0, 0);
    return 0;
#endif
}

/* ---- Decrypt the flag into out[] (caller allocates ENC_FLAG_LEN+1) ----
 * If a debugger is present the seed is mangled on purpose -> garbage output. */
static void decrypt_flag(unsigned char *out) {
    unsigned long long seed = recover_seed();
    if (under_debugger())
        seed ^= 0xDEADBEEFCAFEBABEULL; /* corrupt -> flag becomes garbage */

    unsigned long long s = seed;
    for (size_t i = 0; i < ENC_FLAG_LEN; i += 8) {
        unsigned long long k = splitmix64(&s);
        for (size_t j = 0; j < 8 && (i + j) < ENC_FLAG_LEN; j++)
            out[i + j] = ENC_FLAG[i + j] ^ ((k >> (8 * j)) & 0xFF);
    }
}

/* ---- The reveal mechanism: only fires when score >= TARGET ---- */
static void reveal_flag(int score) {
    if (score < TARGET) {
        printf("[!] Score %d is not enough. You need %d to reveal the flag.\n",
               score, TARGET);
        return;
    }

    unsigned char buf[ENC_FLAG_LEN + 1];
    decrypt_flag(buf);
    buf[ENC_FLAG_LEN] = '\0';

    printf("\n========================================\n");
    printf("  CONGRATULATIONS - SCORE GATE PASSED\n");
    printf("  FLAG: %s\n", (char *)buf);
    printf("========================================\n");
}

int main(void) {
    int score = 0;
    srand((unsigned)time(NULL));

    printf("========================================\n");
    printf("          S C O R E   Q U E S T\n");
    printf("========================================\n");
    printf("Guess the secret number (1-10). +100 per correct guess.\n");
    printf("Reach a score of %d to reveal the flag.\n", TARGET);
    printf("Enter 0 to give up.\n\n");

    while (1) {
        int secret = rand() % 10 + 1;
        int guess;

        printf("[score: %d] guess (1-10): ", score);
        if (scanf("%d", &guess) != 1)
            break;

        if (guess == 0) {
            printf("You gave up with score %d.\n", score);
            break;
        }

        if (guess == secret) {
            score += 100;
            printf("Correct! +100\n");
        } else {
            printf("Wrong. (the number was %d)\n", secret);
        }

        /* The score gate that guards the flag. */
        if (score >= TARGET) {
            reveal_flag(score);
            break;
        }
    }

    return 0;
}
