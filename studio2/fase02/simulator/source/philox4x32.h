#ifndef FOT_TEP_PHILOX4X32_H
#define FOT_TEP_PHILOX4X32_H

#include <stdint.h>

typedef struct {
    uint32_t v[4];
} fot_philox4x32_counter;

typedef struct {
    uint32_t v[2];
} fot_philox4x32_key;

static inline uint32_t fot_philox_mul_hi(uint32_t left, uint32_t right) {
    return (uint32_t)(((uint64_t)left * (uint64_t)right) >> 32);
}

static inline fot_philox4x32_counter fot_philox4x32_10(
    fot_philox4x32_counter counter,
    fot_philox4x32_key key
) {
    static const uint32_t multiplier_0 = UINT32_C(0xD2511F53);
    static const uint32_t multiplier_1 = UINT32_C(0xCD9E8D57);
    static const uint32_t key_increment_0 = UINT32_C(0x9E3779B9);
    static const uint32_t key_increment_1 = UINT32_C(0xBB67AE85);
    unsigned round;

    for (round = 0; round < 10; ++round) {
        const uint32_t high_0 = fot_philox_mul_hi(multiplier_0, counter.v[0]);
        const uint32_t low_0 = multiplier_0 * counter.v[0];
        const uint32_t high_1 = fot_philox_mul_hi(multiplier_1, counter.v[2]);
        const uint32_t low_1 = multiplier_1 * counter.v[2];
        const fot_philox4x32_counter next = {{
            high_1 ^ counter.v[1] ^ key.v[0],
            low_1,
            high_0 ^ counter.v[3] ^ key.v[1],
            low_0
        }};
        counter = next;
        key.v[0] += key_increment_0;
        key.v[1] += key_increment_1;
    }
    return counter;
}

static inline uint32_t fot_philox_word(uint64_t key_seed, uint64_t stream_id, uint64_t draw_index) {
    const uint64_t block_index = draw_index / UINT64_C(4);
    const unsigned lane = (unsigned)(draw_index % UINT64_C(4));
    const fot_philox4x32_counter counter = {{
        (uint32_t)block_index,
        (uint32_t)(block_index >> 32),
        (uint32_t)stream_id,
        (uint32_t)(stream_id >> 32)
    }};
    const fot_philox4x32_key key = {{
        (uint32_t)key_seed,
        (uint32_t)(key_seed >> 32)
    }};
    return fot_philox4x32_10(counter, key).v[lane];
}

static inline double fot_philox_uniform(uint64_t key_seed, uint64_t stream_id, uint64_t draw_index) {
    return (double)fot_philox_word(key_seed, stream_id, draw_index) / 4294967296.0;
}

#endif
