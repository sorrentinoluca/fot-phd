#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>

#include "philox4x32.h"

typedef struct {
    fot_philox4x32_counter counter;
    fot_philox4x32_key key;
    fot_philox4x32_counter expected;
} known_answer;

int main(void) {
    static const known_answer tests[] = {
        {{{0, 0, 0, 0}}, {{0, 0}},
         {{UINT32_C(0x6627e8d5), UINT32_C(0xe169c58d), UINT32_C(0xbc57ac4c), UINT32_C(0x9b00dbd8)}}},
        {{{UINT32_MAX, UINT32_MAX, UINT32_MAX, UINT32_MAX}}, {{UINT32_MAX, UINT32_MAX}},
         {{UINT32_C(0x408f276d), UINT32_C(0x41c83b0e), UINT32_C(0xa20bc7c6), UINT32_C(0x6d5451fd)}}},
        {{{UINT32_C(0x243f6a88), UINT32_C(0x85a308d3), UINT32_C(0x13198a2e), UINT32_C(0x03707344)}},
          {{UINT32_C(0xa4093822), UINT32_C(0x299f31d0)}},
          {{UINT32_C(0xd16cfe09), UINT32_C(0x94fdcceb), UINT32_C(0x5001e420), UINT32_C(0x24126ea1)}}}
    };
    size_t test_index;

    for (test_index = 0; test_index < sizeof(tests) / sizeof(tests[0]); ++test_index) {
        const fot_philox4x32_counter actual =
            fot_philox4x32_10(tests[test_index].counter, tests[test_index].key);
        unsigned lane;
        for (lane = 0; lane < 4; ++lane) {
            if (actual.v[lane] != tests[test_index].expected.v[lane]) {
                fprintf(
                    stderr,
                    "KAT %zu lane %u: expected %08" PRIx32 ", got %08" PRIx32 "\n",
                    test_index + 1,
                    lane,
                    tests[test_index].expected.v[lane],
                    actual.v[lane]
                );
                return 1;
            }
        }
    }

    if (fot_philox_uniform(UINT64_C(1), UINT64_C(2), UINT64_C(3)) !=
        fot_philox_uniform(UINT64_C(1), UINT64_C(2), UINT64_C(3))) {
        fputs("deterministic replay failed\n", stderr);
        return 1;
    }
    if (fot_philox_word(UINT64_C(1), UINT64_C(2), UINT64_C(0)) ==
        fot_philox_word(UINT64_C(1), UINT64_C(3), UINT64_C(0))) {
        fputs("stream separation smoke test failed\n", stderr);
        return 1;
    }

    printf("OK: 3 Random123 KAT vectors, deterministic replay, stream smoke test\n");
    return 0;
}
