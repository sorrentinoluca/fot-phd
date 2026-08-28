# Verbalizer V2 validation report

## Scope and freeze integrity

- Frozen commit and HEAD: `3fd960a192bafacbaabce9471e3c3614d6b2d2db`.
- Frozen tag: `verbalizer-v2-pre-validation`.
- Pre-validation Git status: clean.
- All four frozen SHA-256 hashes matched `VERBALIZER_V2_FREEZE.md`.
- Evaluated data: fault batches 6–7 for F1/F8/F10/F13 and Normal N6–N7 only.
- Fault batches 8–10 and Normal N8–N10 were not read.
- Frozen features, thresholds, renderer, config, similarity, and `top_k=4` were not changed.

## Normal validation

| Scope | Feature | Positive windows | Fraction | Development reference |
|---|---|---:|---:|---:|
| N6 | level | 0/10 | 0.0% | 1/50 (2.0%) |
| N6 | trend | 2/10 | 20.0% | 1/50 (2.0%) |
| N6 | residual | 0/10 | 0.0% | 1/50 (2.0%) |
| N6 | diff | 0/10 | 0.0% | 1/50 (2.0%) |
| N6 | any-primary | 2/10 | 20.0% | 3/50 (6.0%) |
| N7 | level | 0/10 | 0.0% | 1/50 (2.0%) |
| N7 | trend | 0/10 | 0.0% | 1/50 (2.0%) |
| N7 | residual | 1/10 | 10.0% | 1/50 (2.0%) |
| N7 | diff | 2/10 | 20.0% | 1/50 (2.0%) |
| N7 | any-primary | 2/10 | 20.0% | 3/50 (6.0%) |
| N6-N7 | level | 0/20 | 0.0% | 1/50 (2.0%) |
| N6-N7 | trend | 2/20 | 10.0% | 1/50 (2.0%) |
| N6-N7 | residual | 1/20 | 5.0% | 1/50 (2.0%) |
| N6-N7 | diff | 2/20 | 10.0% | 1/50 (2.0%) |
| N6-N7 | any-primary | 4/20 | 20.0% | 3/50 (6.0%) |

## Similarity and margins

| Comparison | Label | Validation median | Validation Q1–Q3 | Development median | Development Q1–Q3 | Δ median |
|---|---|---:|---:|---:|---:|---:|
| validation_intra | F1 | 0.9892 | 0.9892–0.9892 | 0.9905 | 0.9889–0.9913 | -0.0013 |
| validation_intra | F10 | 0.9935 | 0.9935–0.9935 | 0.9898 | 0.9889–0.9923 | 0.0037 |
| validation_intra | F13 | 0.8970 | 0.8970–0.8970 | 0.8858 | 0.8781–0.8961 | 0.0112 |
| validation_intra | F8 | 0.8956 | 0.8956–0.8956 | 0.9043 | 0.8988–0.9089 | -0.0087 |
| validation_intra | Normal | 0.9984 | 0.9984–0.9984 | 0.9990 | 0.9982–0.9990 | -0.0005 |
| validation_inter | F1__F10 | 0.9053 | 0.9046–0.9057 | 0.9049 | 0.9005–0.9065 | 0.0004 |
| validation_inter | F1__F13 | 0.7985 | 0.7890–0.8081 | 0.7746 | 0.7614–0.7795 | 0.0239 |
| validation_inter | F1__F8 | 0.8320 | 0.8240–0.8404 | 0.7942 | 0.7818–0.8088 | 0.0378 |
| validation_inter | F1__Normal | 0.9142 | 0.9138–0.9146 | 0.9115 | 0.9106–0.9124 | 0.0027 |
| validation_inter | F10__F13 | 0.7465 | 0.7345–0.7587 | 0.7205 | 0.7069–0.7304 | 0.0260 |
| validation_inter | F10__F8 | 0.7790 | 0.7640–0.7939 | 0.7442 | 0.7190–0.7496 | 0.0348 |
| validation_inter | F10__Normal | 0.9772 | 0.9754–0.9791 | 0.9779 | 0.9757–0.9811 | -0.0007 |
| validation_inter | F13__F8 | 0.8520 | 0.8481–0.8538 | 0.8528 | 0.8438–0.8592 | -0.0008 |
| validation_inter | F13__Normal | 0.7420 | 0.7286–0.7555 | 0.7137 | 0.7016–0.7176 | 0.0282 |
| validation_inter | F8__Normal | 0.7781 | 0.7643–0.7920 | 0.7384 | 0.7102–0.7437 | 0.0397 |
| validation_to_development_same_class | F1 | 0.9889 | 0.9863–0.9897 | 0.9905 | 0.9889–0.9913 | -0.0017 |
| validation_to_development_same_class | F10 | 0.9922 | 0.9911–0.9927 | 0.9898 | 0.9889–0.9923 | 0.0023 |
| validation_to_development_same_class | F13 | 0.8886 | 0.8765–0.8911 | 0.8858 | 0.8781–0.8961 | 0.0029 |
| validation_to_development_same_class | F8 | 0.8983 | 0.8869–0.9017 | 0.9043 | 0.8988–0.9089 | -0.0060 |
| validation_to_development_same_class | Normal | 0.9986 | 0.9980–0.9989 | 0.9990 | 0.9982–0.9990 | -0.0004 |
| margin | F1 | 0.0751 | 0.0751–0.0751 | 0.0790 | undefined–undefined | -0.0040 |
| margin | F10 | 0.0163 | 0.0163–0.0163 | 0.0119 | undefined–undefined | 0.0045 |
| margin | F13 | 0.0450 | 0.0450–0.0450 | 0.0330 | undefined–undefined | 0.0120 |
| margin | F8 | 0.0436 | 0.0436–0.0436 | 0.0515 | undefined–undefined | -0.0079 |
| margin | Normal | 0.0212 | 0.0212–0.0212 | 0.0210 | undefined–undefined | 0.0002 |

## Fault temporal evidence

The following tables reproduce structured counts without assigning a diagnostic mechanism.

### F1

#### Batch 6 (`case_01`)

| Feature | System active windows | Active fraction | Initial | Late | Dominant variables |
|---|---:|---:|---:|---:|---|
| level | 8/8 | 1.000 | 2 | 2 | XMEAS-1, XMEAS-4, XMEAS-18, XMEAS-34 |
| trend | 6/8 | 0.750 | 2 | 0 | XMEAS-1, XMEAS-11, XMEAS-10, XMEAS-21 |
| residual | 4/8 | 0.500 | 2 | 0 | XMEAS-20, XMEAS-31, XMEAS-29, XMEAS-18 |
| diff | 1/8 | 0.125 | 1 | 0 | XMEAS-10 |
| rapid | 1/8 | 0.125 | 1 | 0 | XMEAS-10 |

Dominant-variable details:

- level: XMEAS-1: active=8/8 (1.000), signs +8/-0, consistency=1.000, late=1.000, run=8; XMEAS-4: active=8/8 (1.000), signs +0/-8, consistency=1.000, late=1.000, run=8; XMEAS-18: active=8/8 (1.000), signs +7/-1, consistency=0.875, late=1.000, run=7; XMEAS-34: active=5/8 (0.625), signs +4/-1, consistency=0.800, late=1.000, run=4
- trend: XMEAS-1: active=6/8 (0.750), signs +3/-3, consistency=0.500, late=0.000, run=1; XMEAS-11: active=6/8 (0.750), signs +3/-3, consistency=0.500, late=0.000, run=1; XMEAS-10: active=4/8 (0.500), signs +2/-2, consistency=0.500, late=0.000, run=1; XMEAS-21: active=4/8 (0.500), signs +2/-2, consistency=0.500, late=0.000, run=1
- residual: XMEAS-20: active=4/8 (0.500), late=0.000, run=4; XMEAS-31: active=4/8 (0.500), late=0.000, run=4; XMEAS-29: active=4/8 (0.500), late=0.000, run=4; XMEAS-18: active=4/8 (0.500), late=0.000, run=4
- diff: XMEAS-10: active=1/8 (0.125), late=0.000, run=1
- rapid: XMEAS-10: active=1/8 (0.125), late=0.000, run=1

#### Batch 7 (`case_02`)

| Feature | System active windows | Active fraction | Initial | Late | Dominant variables |
|---|---:|---:|---:|---:|---|
| level | 8/8 | 1.000 | 2 | 2 | XMEAS-1, XMEAS-4, XMEAS-18, XMEAS-34 |
| trend | 6/8 | 0.750 | 2 | 0 | XMEAS-1, XMEAS-11, XMEAS-34, XMEAS-38 |
| residual | 4/8 | 0.500 | 2 | 0 | XMEAS-20, XMEAS-31, XMEAS-11, XMEAS-18 |
| diff | 2/8 | 0.250 | 1 | 0 | XMEAS-37, XMEAS-10, XMEAS-31, XMEAS-34 |
| rapid | 1/8 | 0.125 | 1 | 0 | XMEAS-10, XMEAS-31, XMEAS-34 |

Dominant-variable details:

- level: XMEAS-1: active=8/8 (1.000), signs +8/-0, consistency=1.000, late=1.000, run=8; XMEAS-4: active=8/8 (1.000), signs +0/-8, consistency=1.000, late=1.000, run=8; XMEAS-18: active=8/8 (1.000), signs +7/-1, consistency=0.875, late=1.000, run=7; XMEAS-34: active=4/8 (0.500), signs +3/-1, consistency=0.750, late=1.000, run=3
- trend: XMEAS-1: active=6/8 (0.750), signs +3/-3, consistency=0.500, late=0.000, run=1; XMEAS-11: active=5/8 (0.625), signs +2/-3, consistency=0.600, late=0.000, run=1; XMEAS-34: active=4/8 (0.500), signs +2/-2, consistency=0.500, late=0.000, run=1; XMEAS-38: active=4/8 (0.500), signs +2/-2, consistency=0.500, late=0.000, run=1
- residual: XMEAS-20: active=4/8 (0.500), late=0.000, run=4; XMEAS-31: active=4/8 (0.500), late=0.000, run=4; XMEAS-11: active=4/8 (0.500), late=0.000, run=4; XMEAS-18: active=4/8 (0.500), late=0.000, run=4
- diff: XMEAS-37: active=2/8 (0.250), late=0.000, run=1; XMEAS-10: active=1/8 (0.125), late=0.000, run=1; XMEAS-31: active=1/8 (0.125), late=0.000, run=1; XMEAS-34: active=1/8 (0.125), late=0.000, run=1
- rapid: XMEAS-10: active=1/8 (0.125), late=0.000, run=1; XMEAS-31: active=1/8 (0.125), late=0.000, run=1; XMEAS-34: active=1/8 (0.125), late=0.000, run=1

### F8

#### Batch 6 (`case_03`)

| Feature | System active windows | Active fraction | Initial | Late | Dominant variables |
|---|---:|---:|---:|---:|---|
| level | 7/8 | 0.875 | 1 | 2 | XMEAS-34, XMEAS-28, XMEAS-1, XMEAS-18 |
| trend | 8/8 | 1.000 | 2 | 2 | XMEAS-1, XMEAS-20, XMEAS-34, XMEAS-31 |
| residual | 8/8 | 1.000 | 2 | 2 | XMEAS-1, XMEAS-20, XMEAS-10, XMEAS-16 |
| diff | 4/8 | 0.500 | 0 | 1 | XMEAS-31, XMEAS-10, XMEAS-1, XMEAS-23 |
| rapid | 4/8 | 0.500 | 0 | 1 | XMEAS-31, XMEAS-10, XMEAS-1, XMEAS-23 |

Dominant-variable details:

- level: XMEAS-34: active=7/8 (0.875), signs +7/-0, consistency=1.000, late=1.000, run=7; XMEAS-28: active=7/8 (0.875), signs +7/-0, consistency=1.000, late=1.000, run=7; XMEAS-1: active=7/8 (0.875), signs +1/-6, consistency=0.857, late=1.000, run=6; XMEAS-18: active=6/8 (0.750), signs +1/-5, consistency=0.833, late=1.000, run=5
- trend: XMEAS-1: active=8/8 (1.000), signs +3/-5, consistency=0.625, late=1.000, run=3; XMEAS-20: active=8/8 (1.000), signs +4/-4, consistency=0.500, late=1.000, run=2; XMEAS-34: active=7/8 (0.875), signs +3/-4, consistency=0.571, late=1.000, run=3; XMEAS-31: active=7/8 (0.875), signs +3/-4, consistency=0.571, late=1.000, run=2
- residual: XMEAS-1: active=8/8 (1.000), late=1.000, run=8; XMEAS-20: active=8/8 (1.000), late=1.000, run=8; XMEAS-10: active=8/8 (1.000), late=1.000, run=8; XMEAS-16: active=8/8 (1.000), late=1.000, run=8
- diff: XMEAS-31: active=2/8 (0.250), late=0.500, run=1; XMEAS-10: active=2/8 (0.250), late=0.000, run=1; XMEAS-1: active=1/8 (0.125), late=0.500, run=1; XMEAS-23: active=1/8 (0.125), late=0.000, run=1
- rapid: XMEAS-31: active=2/8 (0.250), late=0.500, run=1; XMEAS-10: active=2/8 (0.250), late=0.000, run=1; XMEAS-1: active=1/8 (0.125), late=0.500, run=1; XMEAS-23: active=1/8 (0.125), late=0.000, run=1

#### Batch 7 (`case_04`)

| Feature | System active windows | Active fraction | Initial | Late | Dominant variables |
|---|---:|---:|---:|---:|---|
| level | 8/8 | 1.000 | 2 | 2 | XMEAS-18, XMEAS-1, XMEAS-20, XMEAS-34 |
| trend | 8/8 | 1.000 | 2 | 2 | XMEAS-1, XMEAS-20, XMEAS-15, XMEAS-11 |
| residual | 8/8 | 1.000 | 2 | 2 | XMEAS-1, XMEAS-20, XMEAS-10, XMEAS-18 |
| diff | 8/8 | 1.000 | 2 | 2 | XMEAS-10, XMEAS-31, XMEAS-29, XMEAS-1 |
| rapid | 8/8 | 1.000 | 2 | 2 | XMEAS-10, XMEAS-31, XMEAS-29, XMEAS-1 |

Dominant-variable details:

- level: XMEAS-18: active=8/8 (1.000), signs +4/-4, consistency=0.500, late=1.000, run=2; XMEAS-1: active=7/8 (0.875), signs +4/-3, consistency=0.571, late=1.000, run=2; XMEAS-20: active=7/8 (0.875), signs +4/-3, consistency=0.571, late=0.500, run=2; XMEAS-34: active=6/8 (0.750), signs +1/-5, consistency=0.833, late=0.500, run=4
- trend: XMEAS-1: active=8/8 (1.000), signs +4/-4, consistency=0.500, late=1.000, run=2; XMEAS-20: active=8/8 (1.000), signs +3/-5, consistency=0.625, late=1.000, run=2; XMEAS-15: active=8/8 (1.000), signs +3/-5, consistency=0.625, late=1.000, run=2; XMEAS-11: active=7/8 (0.875), signs +2/-5, consistency=0.714, late=0.500, run=3
- residual: XMEAS-1: active=8/8 (1.000), late=1.000, run=8; XMEAS-20: active=8/8 (1.000), late=1.000, run=8; XMEAS-10: active=8/8 (1.000), late=1.000, run=8; XMEAS-18: active=8/8 (1.000), late=1.000, run=8
- diff: XMEAS-10: active=7/8 (0.875), late=1.000, run=6; XMEAS-31: active=5/8 (0.625), late=1.000, run=2; XMEAS-29: active=4/8 (0.500), late=0.500, run=1; XMEAS-1: active=4/8 (0.500), late=0.000, run=2
- rapid: XMEAS-10: active=7/8 (0.875), late=1.000, run=6; XMEAS-31: active=5/8 (0.625), late=1.000, run=2; XMEAS-29: active=4/8 (0.500), late=0.500, run=1; XMEAS-1: active=4/8 (0.500), late=0.000, run=2

### F10

#### Batch 6 (`case_05`)

| Feature | System active windows | Active fraction | Initial | Late | Dominant variables |
|---|---:|---:|---:|---:|---|
| level | 8/8 | 1.000 | 2 | 2 | XMEAS-18 |
| trend | 6/8 | 0.750 | 1 | 2 | XMEAS-18, XMEAS-21, XMEAS-1 |
| residual | 8/8 | 1.000 | 2 | 2 | XMEAS-18, XMEAS-38, XMEAS-37 |
| diff | 8/8 | 1.000 | 2 | 2 | XMEAS-18, XMEAS-37, XMEAS-38, XMEAS-41 |
| rapid | 8/8 | 1.000 | 2 | 2 | XMEAS-18, XMEAS-38, XMEAS-37 |

Dominant-variable details:

- level: XMEAS-18: active=8/8 (1.000), signs +3/-5, consistency=0.625, late=1.000, run=4
- trend: XMEAS-18: active=6/8 (0.750), signs +1/-5, consistency=0.833, late=1.000, run=4; XMEAS-21: active=1/8 (0.125), signs +0/-1, consistency=1.000, late=0.500, run=1; XMEAS-1: active=1/8 (0.125), signs +0/-1, consistency=1.000, late=0.000, run=1
- residual: XMEAS-18: active=8/8 (1.000), late=1.000, run=8; XMEAS-38: active=2/8 (0.250), late=0.000, run=1; XMEAS-37: active=1/8 (0.125), late=0.000, run=1
- diff: XMEAS-18: active=8/8 (1.000), late=1.000, run=8; XMEAS-37: active=1/8 (0.125), late=0.000, run=1; XMEAS-38: active=1/8 (0.125), late=0.000, run=1; XMEAS-41: active=1/8 (0.125), late=0.000, run=1
- rapid: XMEAS-18: active=8/8 (1.000), late=1.000, run=8; XMEAS-38: active=1/8 (0.125), late=0.000, run=1; XMEAS-37: active=1/8 (0.125), late=0.000, run=1

#### Batch 7 (`case_06`)

| Feature | System active windows | Active fraction | Initial | Late | Dominant variables |
|---|---:|---:|---:|---:|---|
| level | 7/8 | 0.875 | 2 | 1 | XMEAS-18 |
| trend | 8/8 | 1.000 | 2 | 2 | XMEAS-18, XMEAS-1 |
| residual | 8/8 | 1.000 | 2 | 2 | XMEAS-18, XMEAS-38 |
| diff | 7/8 | 0.875 | 1 | 2 | XMEAS-18 |
| rapid | 7/8 | 0.875 | 1 | 2 | XMEAS-18 |

Dominant-variable details:

- level: XMEAS-18: active=7/8 (0.875), signs +2/-5, consistency=0.714, late=0.500, run=4
- trend: XMEAS-18: active=8/8 (1.000), signs +6/-2, consistency=0.750, late=1.000, run=5; XMEAS-1: active=1/8 (0.125), signs +0/-1, consistency=1.000, late=0.000, run=1
- residual: XMEAS-18: active=8/8 (1.000), late=1.000, run=8; XMEAS-38: active=1/8 (0.125), late=0.000, run=1
- diff: XMEAS-18: active=7/8 (0.875), late=1.000, run=7
- rapid: XMEAS-18: active=7/8 (0.875), late=1.000, run=7

### F13

#### Batch 6 (`case_07`)

| Feature | System active windows | Active fraction | Initial | Late | Dominant variables |
|---|---:|---:|---:|---:|---|
| level | 8/8 | 1.000 | 2 | 2 | XMEAS-10, XMEAS-24, XMEAS-18, XMEAS-34 |
| trend | 8/8 | 1.000 | 2 | 2 | XMEAS-15, XMEAS-30, XMEAS-34, XMEAS-28 |
| residual | 8/8 | 1.000 | 2 | 2 | XMEAS-7, XMEAS-16, XMEAS-13, XMEAS-21 |
| diff | 5/8 | 0.625 | 0 | 2 | XMEAS-10, XMEAS-16, XMEAS-7, XMEAS-13 |
| rapid | 4/8 | 0.500 | 0 | 1 | XMEAS-10, XMEAS-7, XMEAS-16, XMEAS-13 |

Dominant-variable details:

- level: XMEAS-10: active=8/8 (1.000), signs +3/-5, consistency=0.625, late=1.000, run=2; XMEAS-24: active=7/8 (0.875), signs +2/-5, consistency=0.714, late=1.000, run=4; XMEAS-18: active=7/8 (0.875), signs +3/-4, consistency=0.571, late=1.000, run=3; XMEAS-34: active=7/8 (0.875), signs +3/-4, consistency=0.571, late=1.000, run=3
- trend: XMEAS-15: active=8/8 (1.000), signs +4/-4, consistency=0.500, late=1.000, run=2; XMEAS-30: active=8/8 (1.000), signs +5/-3, consistency=0.625, late=1.000, run=2; XMEAS-34: active=8/8 (1.000), signs +5/-3, consistency=0.625, late=1.000, run=2; XMEAS-28: active=8/8 (1.000), signs +5/-3, consistency=0.625, late=1.000, run=2
- residual: XMEAS-7: active=8/8 (1.000), late=1.000, run=8; XMEAS-16: active=8/8 (1.000), late=1.000, run=8; XMEAS-13: active=8/8 (1.000), late=1.000, run=8; XMEAS-21: active=8/8 (1.000), late=1.000, run=8
- diff: XMEAS-10: active=4/8 (0.500), late=0.500, run=4; XMEAS-16: active=3/8 (0.375), late=0.500, run=3; XMEAS-7: active=3/8 (0.375), late=0.500, run=3; XMEAS-13: active=3/8 (0.375), late=0.500, run=3
- rapid: XMEAS-10: active=4/8 (0.500), late=0.500, run=4; XMEAS-7: active=3/8 (0.375), late=0.500, run=3; XMEAS-16: active=3/8 (0.375), late=0.500, run=3; XMEAS-13: active=3/8 (0.375), late=0.500, run=3

#### Batch 7 (`case_08`)

| Feature | System active windows | Active fraction | Initial | Late | Dominant variables |
|---|---:|---:|---:|---:|---|
| level | 8/8 | 1.000 | 2 | 2 | XMEAS-10, XMEAS-18, XMEAS-38, XMEAS-33 |
| trend | 8/8 | 1.000 | 2 | 2 | XMEAS-21, XMEAS-30, XMEAS-24, XMEAS-34 |
| residual | 8/8 | 1.000 | 2 | 2 | XMEAS-7, XMEAS-16, XMEAS-13, XMEAS-10 |
| diff | 6/8 | 0.750 | 1 | 2 | XMEAS-10, XMEAS-16, XMEAS-7, XMEAS-13 |
| rapid | 6/8 | 0.750 | 1 | 2 | XMEAS-10, XMEAS-16, XMEAS-7, XMEAS-13 |

Dominant-variable details:

- level: XMEAS-10: active=8/8 (1.000), signs +5/-3, consistency=0.625, late=1.000, run=3; XMEAS-18: active=6/8 (0.750), signs +3/-3, consistency=0.500, late=1.000, run=3; XMEAS-38: active=6/8 (0.750), signs +3/-3, consistency=0.500, late=1.000, run=3; XMEAS-33: active=6/8 (0.750), signs +3/-3, consistency=0.500, late=1.000, run=3
- trend: XMEAS-21: active=8/8 (1.000), signs +6/-2, consistency=0.750, late=1.000, run=3; XMEAS-30: active=8/8 (1.000), signs +3/-5, consistency=0.625, late=1.000, run=3; XMEAS-24: active=8/8 (1.000), signs +3/-5, consistency=0.625, late=1.000, run=3; XMEAS-34: active=8/8 (1.000), signs +4/-4, consistency=0.500, late=1.000, run=2
- residual: XMEAS-7: active=8/8 (1.000), late=1.000, run=8; XMEAS-16: active=8/8 (1.000), late=1.000, run=8; XMEAS-13: active=8/8 (1.000), late=1.000, run=8; XMEAS-10: active=8/8 (1.000), late=1.000, run=8
- diff: XMEAS-10: active=6/8 (0.750), late=1.000, run=4; XMEAS-16: active=4/8 (0.500), late=0.500, run=2; XMEAS-7: active=3/8 (0.375), late=0.500, run=1; XMEAS-13: active=3/8 (0.375), late=0.500, run=1
- rapid: XMEAS-10: active=6/8 (0.750), late=1.000, run=4; XMEAS-16: active=4/8 (0.500), late=0.500, run=2; XMEAS-7: active=3/8 (0.375), late=0.500, run=1; XMEAS-13: active=3/8 (0.375), late=0.500, run=1

## Top-4 dominant-variable Jaccard

| Class | Feature | Validation Jaccard | Development median [Q1, Q3] |
|---|---|---:|---:|
| F1 | level | 1.0000 | 0.6000 [0.6000, 0.9000] |
| F1 | trend | 0.3333 | 0.6000 [0.6000, 0.6000] |
| F1 | residual | 0.6000 | 0.6000 [0.6000, 0.9000] |
| F1 | diff | 0.2500 | 0.5000 [0.3333, 0.6250] |
| F1 | rapid | 0.3333 | 0.5000 [0.5000, 0.6667] |
| F10 | level | 1.0000 | 1.0000 [1.0000, 1.0000] |
| F10 | trend | 0.6667 | 0.5000 [0.5000, 0.5000] |
| F10 | residual | 0.6667 | 0.3667 [0.2000, 0.4000] |
| F10 | diff | 0.2500 | 0.5000 [0.5000, 0.8750] |
| F10 | rapid | 0.3333 | 0.5000 [0.5000, 0.8750] |
| F13 | level | 0.3333 | 0.1429 [0.0357, 0.4857] |
| F13 | trend | 0.3333 | 0.1429 [0.0000, 0.1429] |
| F13 | residual | 0.6000 | 1.0000 [0.6000, 1.0000] |
| F13 | diff | 1.0000 | 1.0000 [0.6000, 1.0000] |
| F13 | rapid | 1.0000 | 1.0000 [0.6000, 1.0000] |
| F8 | level | 0.6000 | 0.2381 [0.1429, 0.3333] |
| F8 | trend | 0.3333 | 0.1429 [0.0357, 0.2857] |
| F8 | residual | 0.6000 | 0.4667 [0.3333, 0.6000] |
| F8 | diff | 0.6000 | 1.0000 [0.7500, 1.0000] |
| F8 | rapid | 0.6000 | 1.0000 [0.7500, 1.0000] |
| Normal | level | undefined | 0.0000 [0.0000, 0.0000] |
| Normal | trend | 0.0000 | 0.0000 [0.0000, 0.0000] |
| Normal | residual | 0.0000 | 0.0000 [0.0000, 0.0000] |
| Normal | diff | 0.0000 | 0.0000 [0.0000, 0.0000] |
| Normal | rapid | 0.0000 | undefined [undefined, undefined] |

## Dominant-variable recurrence

Full recurrence counts are in `validation_variable_recurrence.csv`. Variables recurring in both validation cases:

- F1 / diff: XMEAS-10 (dev 5/5)
- F1 / level: XMEAS-1 (dev 5/5), XMEAS-18 (dev 5/5), XMEAS-34 (dev 3/5), XMEAS-4 (dev 5/5)
- F1 / rapid: XMEAS-10 (dev 5/5)
- F1 / residual: XMEAS-18 (dev 1/5), XMEAS-20 (dev 5/5), XMEAS-31 (dev 5/5)
- F1 / trend: XMEAS-1 (dev 5/5), XMEAS-11 (dev 5/5)
- F10 / diff: XMEAS-18 (dev 5/5)
- F10 / level: XMEAS-18 (dev 5/5)
- F10 / rapid: XMEAS-18 (dev 5/5)
- F10 / residual: XMEAS-18 (dev 5/5), XMEAS-38 (dev 3/5)
- F10 / trend: XMEAS-1 (dev 1/5), XMEAS-18 (dev 5/5)
- F13 / diff: XMEAS-10 (dev 5/5), XMEAS-13 (dev 4/5), XMEAS-16 (dev 5/5), XMEAS-7 (dev 5/5)
- F13 / level: XMEAS-10 (dev 1/5), XMEAS-18 (dev 1/5)
- F13 / rapid: XMEAS-10 (dev 5/5), XMEAS-13 (dev 4/5), XMEAS-16 (dev 5/5), XMEAS-7 (dev 5/5)
- F13 / residual: XMEAS-13 (dev 5/5), XMEAS-16 (dev 5/5), XMEAS-7 (dev 5/5)
- F13 / trend: XMEAS-30 (dev 1/5), XMEAS-34 (dev 2/5)
- F8 / diff: XMEAS-1 (dev 5/5), XMEAS-10 (dev 5/5), XMEAS-31 (dev 5/5)
- F8 / level: XMEAS-1 (dev 3/5), XMEAS-18 (dev 3/5), XMEAS-34 (dev 1/5)
- F8 / rapid: XMEAS-1 (dev 5/5), XMEAS-10 (dev 5/5), XMEAS-31 (dev 5/5)
- F8 / residual: XMEAS-1 (dev 4/5), XMEAS-10 (dev 4/5), XMEAS-20 (dev 4/5)
- F8 / trend: XMEAS-1 (dev 2/5), XMEAS-20 (dev 3/5)

## F10 component-distance audit

Positive `normal_minus_same_class_distance` means validation F10 is closer to development F10 than to validation Normal for that component; negative means closer to Normal.

| Component | Distance to development F10 | Distance to validation Normal | Normal minus same-class |
|---|---:|---:|---:|
| level_signed_activity | 0.00595 | 0.00381 | -0.00213 |
| trend_signed_activity | 0.01021 | 0.00838 | -0.00183 |
| residual_late_active_fraction | 0.01951 | 0.02439 | 0.00488 |
| level_longest_same_sign_run | 0.00488 | 0.01220 | 0.00732 |
| trend_longest_same_sign_run | 0.00976 | 0.01707 | 0.00732 |
| level_late_active_fraction | 0.00610 | 0.01829 | 0.01220 |
| trend_active_fraction | 0.00884 | 0.02530 | 0.01646 |
| rapid_longest_run | 0.01006 | 0.02713 | 0.01707 |
| diff_longest_run | 0.01098 | 0.02866 | 0.01768 |
| residual_active_fraction | 0.01220 | 0.03171 | 0.01951 |
| trend_late_active_fraction | 0.01098 | 0.03049 | 0.01951 |
| residual_longest_run | 0.01006 | 0.03018 | 0.02012 |
| rapid_active_fraction | 0.00701 | 0.02713 | 0.02012 |
| level_active_fraction | 0.00274 | 0.02287 | 0.02012 |
| diff_active_fraction | 0.00793 | 0.02866 | 0.02073 |
| diff_late_active_fraction | 0.00244 | 0.02439 | 0.02195 |
| rapid_late_active_fraction | 0.00244 | 0.02439 | 0.02195 |

## Descriptive verdict

No post-hoc numerical pass/fail threshold is used. The labels below summarize
jointly the frozen similarities, margins, dominant variables, and temporal
counts relative to the observed development intervals.

### F1 — firma stabile

- Validation intra-class similarity is `0.98924`, inside the development IQR
  `[0.98893, 0.99126]` and range `[0.98574, 0.99193]`.
- Validation-to-development same-class median similarity is `0.98888`; the two
  validation batches have medians `0.98987` and `0.98592` against the five
  development cases.
- The margin remains positive at `0.07505`, compared with `0.07903` in
  development.
- Level top-4 Jaccard is `1.0`; all four variables recur in both validation
  cases. Residual Jaccard is `0.6`. Trend, diff, and rapid Jaccards are lower
  (`0.333`, `0.25`, `0.333`) but remain at the respective development minima.
- Both batches reproduce the development system-level temporal counts: level
  `8/8` with late activity `2/2`, trend `6/8` with late activity `0/2`, residual
  `4/8` with late activity `0/2`, and rapid `1/8` with late activity `0/2`.
  Diff is `1/8` and `2/8`, also matching the development range.

### F8 — firma parzialmente stabile

- Validation intra-class similarity is `0.89562`, inside the development range
  `[0.88424, 0.92055]` but below its IQR `[0.89876, 0.90887]`.
- Validation-to-development same-class median is `0.89827`; batch 6 has median
  `0.88495` and batch 7 `0.89849` against development.
- The margin remains positive at `0.04362`, reduced from `0.05152`.
- The recurring core is retained: XMEAS-1, XMEAS-10, and XMEAS-31 recur in both
  validation top-4 sets for diff and rapid. Their validation Jaccard is `0.6`,
  below the development minimum `0.75`. Level, trend, and residual Jaccards are
  within or above their development ranges.
- Residual and trend are active in `8/8` windows in both cases. Diff and rapid
  are active in `4/8` windows in batch 6 and `8/8` in batch 7, whereas their
  development range was `6–7/8`. Level is `7/8` in batch 6 and `8/8` in batch
  7, compared with `8/8` throughout development. Thus the class-level core is
  recognizable, but the temporal amount of diff/rapid evidence does not remain
  inside the development interval.

### F10 — firma stabile

- Validation intra-class similarity is `0.99354`, inside the development range
  `[0.98700, 0.99381]` and above its Q3. Validation-to-development same-class
  median is `0.99215`, inside the development IQR.
- F10–Normal validation median similarity is `0.97721`, compared with `0.97794`
  in development. The margin is positive and increases from `0.01188` to
  `0.01634`; no adjustment was made.
- XMEAS-18 remains the common dominant variable for level, trend, residual,
  diff, and rapid. Level Jaccard is `1.0`; trend and residual are `0.667`. Diff
  Jaccard is `0.25`, below the development minimum `0.333`, because batch 6 has
  additional secondary variables while batch 7 retains only XMEAS-18.
- The system-level temporal counts stay within development ranges: level is
  `8/8` and `7/8`, trend `6/8` and `8/8`, residual `8/8` in both, and diff/rapid
  `8/8` and `7/8`; late activity is retained.
- The component audit identifies only two components closer to validation
  Normal than to development F10: `level_signed_activity` (distance gap
  `-0.00213`) and `trend_signed_activity` (`-0.00183`). Their affine-normalized
  means are close to `0.5` because positive and negative active-window counts
  are relatively balanced across the 41 variables. All other component-family
  gaps are positive. The next-smallest separation is residual late activity
  (`+0.00488`). The generally high F10–Normal similarity also reflects the many
  equally weighted components that are inactive in both signatures.

### F13 — firma parzialmente stabile

- Validation intra-class similarity is `0.89697`, inside the development range
  `[0.86693, 0.90029]` and just above development Q3. Validation-to-development
  same-class median is `0.88863`, inside the development IQR.
- The margin remains positive and increases from `0.03300` to `0.04497`.
- The dominant residual variables XMEAS-7, XMEAS-13, and XMEAS-16 recur in both
  validation cases. Diff and rapid retain the same four-variable sets in both
  batches, giving Jaccard `1.0`; residual Jaccard is `0.6`. Level and trend
  variables remain less recurrent, as they were in development.
- Level, trend, and residual remain active in `8/8` windows with late activity
  `2/2` in both cases. Diff is active in `5/8` and `6/8`, and rapid in `4/8` and
  `6/8`; development had `7–8/8` for both. The dominant variable sets are
  stable, but their temporal active fractions are lower than the development
  range, so the complete temporal signature is only partially conserved.

## Overall descriptive conclusion

F1 and F10 preserve the development signature across similarity, margin,
dominant-variable core, and system temporal counts. F8 and F13 retain positive
margins and recognizable dominant-variable cores, but show out-of-development
changes in diff/rapid temporal activity. These observations are reported as-is;
V2 remains frozen and no test batch is opened.
