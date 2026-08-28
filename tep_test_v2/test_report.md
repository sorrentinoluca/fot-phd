# Verbalizer V2 final test report

## Frozen protocol

- Freeze commit: `3fd960a192bafacbaabce9471e3c3614d6b2d2db`.
- Validation commit: `1d9c1617b56c19d2bc71dfef7b7902df0670b537`.
- Frozen config, features, renderer, evaluator, thresholds, `top_k=4`, and similarity were unchanged.
- Test data: F1/F8/F10/F13 batches 8–10 and Normal N8–N10 only.
- No retrospective pass/fail threshold is used.

## Normal N8–N10

| Scope | Feature | Positive windows | Fraction |
|---|---|---:|---:|
| N10 | level | 0/10 | 0.0% |
| N10 | trend | 0/10 | 0.0% |
| N10 | residual | 0/10 | 0.0% |
| N10 | diff | 0/10 | 0.0% |
| N10 | rapid | 0/10 | 0.0% |
| N10 | any-primary | 0/10 | 0.0% |
| N8 | level | 0/10 | 0.0% |
| N8 | trend | 0/10 | 0.0% |
| N8 | residual | 0/10 | 0.0% |
| N8 | diff | 2/10 | 20.0% |
| N8 | rapid | 0/10 | 0.0% |
| N8 | any-primary | 2/10 | 20.0% |
| N9 | level | 0/10 | 0.0% |
| N9 | trend | 0/10 | 0.0% |
| N9 | residual | 0/10 | 0.0% |
| N9 | diff | 0/10 | 0.0% |
| N9 | rapid | 0/10 | 0.0% |
| N9 | any-primary | 0/10 | 0.0% |
| N8-N10 | level | 0/30 | 0.0% |
| N8-N10 | trend | 0/30 | 0.0% |
| N8-N10 | residual | 0/30 | 0.0% |
| N8-N10 | diff | 2/30 | 6.7% |
| N8-N10 | rapid | 0/30 | 0.0% |
| N8-N10 | any-primary | 2/30 | 6.7% |

## Similarities and margins

| Comparison | Label | Development | Validation | Test median [Q1, Q3] | Test range |
|---|---|---:|---:|---:|---:|
| test_intra | F1 | 0.9905 | 0.9892 | 0.9906 [0.9904, 0.9908] | 0.9901–0.9909 |
| test_intra | F10 | 0.9898 | 0.9935 | 0.9907 [0.9900, 0.9919] | 0.9894–0.9932 |
| test_intra | F13 | 0.8858 | 0.8970 | 0.8890 [0.8860, 0.8894] | 0.8831–0.8899 |
| test_intra | F8 | 0.9043 | 0.8956 | 0.8597 [0.8581, 0.8900] | 0.8564–0.9204 |
| test_intra | Normal | 0.9990 | 0.9984 | 0.9994 [0.9994, 0.9997] | 0.9994–1.0000 |
| test_inter | F1__F10 | 0.9049 | 0.9053 | 0.9050 [0.9044, 0.9056] | 0.9035–0.9072 |
| test_inter | F1__F13 | 0.7746 | 0.7985 | 0.7790 [0.7648, 0.7880] | 0.7630–0.7908 |
| test_inter | F1__F8 | 0.7942 | 0.8320 | 0.8242 [0.7303, 0.8398] | 0.7271–0.8406 |
| test_inter | F1__Normal | 0.9115 | 0.9142 | 0.9139 [0.9131, 0.9139] | 0.9131–0.9145 |
| test_inter | F10__F13 | 0.7205 | 0.7465 | 0.7254 [0.7113, 0.7357] | 0.7091–0.7373 |
| test_inter | F10__F8 | 0.7442 | 0.7790 | 0.7736 [0.6700, 0.7790] | 0.6664–0.7826 |
| test_inter | F10__Normal | 0.9779 | 0.9772 | 0.9793 [0.9761, 0.9796] | 0.9755–0.9802 |
| test_inter | F13__F8 | 0.8528 | 0.8520 | 0.8453 [0.8362, 0.8488] | 0.8245–0.8612 |
| test_inter | F13__Normal | 0.7137 | 0.7420 | 0.7176 [0.7051, 0.7359] | 0.7045–0.7365 |
| test_inter | F8__Normal | 0.7384 | 0.7781 | 0.7728 [0.6620, 0.7803] | 0.6620–0.7803 |
| test_to_development_same_class | F1 | 0.9905 | 0.9889 | 0.9898 [0.9880, 0.9905] | 0.9868–0.9936 |
| test_to_validation_same_class | F1 | 0.9905 | 0.9892 | 0.9894 [0.9883, 0.9910] | 0.9876–0.9921 |
| test_to_development_same_class | F10 | 0.9898 | 0.9922 | 0.9919 [0.9896, 0.9937] | 0.9871–0.9944 |
| test_to_validation_same_class | F10 | 0.9898 | 0.9935 | 0.9926 [0.9922, 0.9930] | 0.9893–0.9944 |
| test_to_development_same_class | F13 | 0.8858 | 0.8886 | 0.8945 [0.8851, 0.9009] | 0.8710–0.9133 |
| test_to_validation_same_class | F13 | 0.8858 | 0.8970 | 0.8852 [0.8790, 0.8928] | 0.8722–0.9111 |
| test_to_development_same_class | F8 | 0.9043 | 0.8983 | 0.8997 [0.8855, 0.9089] | 0.8320–0.9260 |
| test_to_validation_same_class | F8 | 0.9043 | 0.8956 | 0.9120 [0.8741, 0.9148] | 0.8382–0.9239 |
| test_to_development_same_class | Normal | 0.9990 | 0.9986 | 0.9990 [0.9989, 0.9997] | 0.9984–1.0000 |
| test_to_validation_same_class | Normal | 0.9990 | 0.9984 | 0.9989 [0.9989, 0.9994] | 0.9983–0.9996 |
| margin | F1 | 0.0790 | 0.0751 | 0.0767 [0.0767, 0.0767] | 0.0767–0.0767 |
| margin | F10 | 0.0119 | 0.0163 | 0.0114 [0.0114, 0.0114] | 0.0114–0.0114 |
| margin | F13 | 0.0330 | 0.0450 | 0.0437 [0.0437, 0.0437] | 0.0437–0.0437 |
| margin | F8 | 0.0515 | 0.0436 | 0.0143 [0.0143, 0.0143] | 0.0143–0.0143 |
| margin | Normal | 0.0210 | 0.0212 | 0.0201 [0.0201, 0.0201] | 0.0201–0.0201 |

## Test temporal evidence

Tables report frozen structured counts without assigning mechanisms.

### F1

#### Batch 8 (`test_case_01`)

| Feature | Active | Fraction | Initial | Late | Dominant top-4 |
|---|---:|---:|---:|---:|---|
| level | 8/8 | 1.000 | 2 | 2 | XMEAS-1, XMEAS-4, XMEAS-18, XMEAS-34 |
| trend | 6/8 | 0.750 | 2 | 0 | XMEAS-11, XMEAS-1, XMEAS-18, XMEAS-20 |
| residual | 4/8 | 0.500 | 2 | 0 | XMEAS-20, XMEAS-31, XMEAS-11, XMEAS-18 |
| diff | 2/8 | 0.250 | 2 | 0 | XMEAS-10, XMEAS-31, XMEAS-39 |
| rapid | 1/8 | 0.125 | 1 | 0 | XMEAS-10, XMEAS-31 |

#### Batch 9 (`test_case_02`)

| Feature | Active | Fraction | Initial | Late | Dominant top-4 |
|---|---:|---:|---:|---:|---|
| level | 8/8 | 1.000 | 2 | 2 | XMEAS-1, XMEAS-4, XMEAS-18, XMEAS-34 |
| trend | 6/8 | 0.750 | 2 | 0 | XMEAS-1, XMEAS-11, XMEAS-10, XMEAS-34 |
| residual | 5/8 | 0.625 | 2 | 1 | XMEAS-20, XMEAS-31, XMEAS-11, XMEAS-18 |
| diff | 1/8 | 0.125 | 1 | 0 | XMEAS-10 |
| rapid | 1/8 | 0.125 | 1 | 0 | XMEAS-10 |

#### Batch 10 (`test_case_03`)

| Feature | Active | Fraction | Initial | Late | Dominant top-4 |
|---|---:|---:|---:|---:|---|
| level | 8/8 | 1.000 | 2 | 2 | XMEAS-1, XMEAS-4, XMEAS-18, XMEAS-34 |
| trend | 5/8 | 0.625 | 2 | 0 | XMEAS-1, XMEAS-11, XMEAS-10, XMEAS-21 |
| residual | 4/8 | 0.500 | 2 | 0 | XMEAS-20, XMEAS-11, XMEAS-18, XMEAS-22 |
| diff | 1/8 | 0.125 | 1 | 0 | XMEAS-10, XMEAS-38, XMEAS-1 |
| rapid | 1/8 | 0.125 | 1 | 0 | XMEAS-10, XMEAS-1, XMEAS-38 |

### F8

#### Batch 8 (`test_case_04`)

| Feature | Active | Fraction | Initial | Late | Dominant top-4 |
|---|---:|---:|---:|---:|---|
| level | 8/8 | 1.000 | 2 | 2 | XMEAS-1, XMEAS-34, XMEAS-28, XMEAS-31 |
| trend | 8/8 | 1.000 | 2 | 2 | XMEAS-22, XMEAS-10, XMEAS-1, XMEAS-20 |
| residual | 8/8 | 1.000 | 2 | 2 | XMEAS-1, XMEAS-20, XMEAS-10, XMEAS-16 |
| diff | 6/8 | 0.750 | 2 | 1 | XMEAS-10, XMEAS-1, XMEAS-29, XMEAS-31 |
| rapid | 6/8 | 0.750 | 2 | 1 | XMEAS-10, XMEAS-1, XMEAS-29, XMEAS-31 |

#### Batch 9 (`test_case_05`)

| Feature | Active | Fraction | Initial | Late | Dominant top-4 |
|---|---:|---:|---:|---:|---|
| level | 8/8 | 1.000 | 2 | 2 | XMEAS-1, XMEAS-20, XMEAS-30, XMEAS-18 |
| trend | 8/8 | 1.000 | 2 | 2 | XMEAS-1, XMEAS-20, XMEAS-31, XMEAS-11 |
| residual | 8/8 | 1.000 | 2 | 2 | XMEAS-20, XMEAS-1, XMEAS-10, XMEAS-21 |
| diff | 7/8 | 0.875 | 1 | 2 | XMEAS-10, XMEAS-31, XMEAS-29, XMEAS-1 |
| rapid | 6/8 | 0.750 | 1 | 2 | XMEAS-10, XMEAS-31, XMEAS-1, XMEAS-29 |

#### Batch 10 (`test_case_06`)

| Feature | Active | Fraction | Initial | Late | Dominant top-4 |
|---|---:|---:|---:|---:|---|
| level | 8/8 | 1.000 | 2 | 2 | XMEAS-1, XMEAS-30, XMEAS-24, XMEAS-34 |
| trend | 8/8 | 1.000 | 2 | 2 | XMEAS-34, XMEAS-28, XMEAS-24, XMEAS-20 |
| residual | 8/8 | 1.000 | 2 | 2 | XMEAS-7, XMEAS-16, XMEAS-13, XMEAS-1 |
| diff | 8/8 | 1.000 | 2 | 2 | XMEAS-10, XMEAS-29, XMEAS-1, XMEAS-31 |
| rapid | 8/8 | 1.000 | 2 | 2 | XMEAS-10, XMEAS-29, XMEAS-1, XMEAS-31 |

### F10

#### Batch 8 (`test_case_07`)

| Feature | Active | Fraction | Initial | Late | Dominant top-4 |
|---|---:|---:|---:|---:|---|
| level | 7/8 | 0.875 | 2 | 2 | XMEAS-18 |
| trend | 6/8 | 0.750 | 2 | 1 | XMEAS-18 |
| residual | 8/8 | 1.000 | 2 | 2 | XMEAS-18, XMEAS-38, XMEAS-39 |
| diff | 8/8 | 1.000 | 2 | 2 | XMEAS-18, XMEAS-39 |
| rapid | 8/8 | 1.000 | 2 | 2 | XMEAS-18, XMEAS-39 |

#### Batch 9 (`test_case_08`)

| Feature | Active | Fraction | Initial | Late | Dominant top-4 |
|---|---:|---:|---:|---:|---|
| level | 6/8 | 0.750 | 1 | 2 | XMEAS-18 |
| trend | 8/8 | 1.000 | 2 | 2 | XMEAS-18, XMEAS-38 |
| residual | 8/8 | 1.000 | 2 | 2 | XMEAS-18, XMEAS-38, XMEAS-11, XMEAS-7 |
| diff | 8/8 | 1.000 | 2 | 2 | XMEAS-18, XMEAS-37, XMEAS-40, XMEAS-41 |
| rapid | 8/8 | 1.000 | 2 | 2 | XMEAS-18 |

#### Batch 10 (`test_case_09`)

| Feature | Active | Fraction | Initial | Late | Dominant top-4 |
|---|---:|---:|---:|---:|---|
| level | 6/8 | 0.750 | 2 | 1 | XMEAS-18 |
| trend | 7/8 | 0.875 | 2 | 2 | XMEAS-18, XMEAS-1, XMEAS-15 |
| residual | 8/8 | 1.000 | 2 | 2 | XMEAS-18, XMEAS-38 |
| diff | 8/8 | 1.000 | 2 | 2 | XMEAS-18, XMEAS-37, XMEAS-34 |
| rapid | 7/8 | 0.875 | 2 | 1 | XMEAS-18 |

### F13

#### Batch 8 (`test_case_10`)

| Feature | Active | Fraction | Initial | Late | Dominant top-4 |
|---|---:|---:|---:|---:|---|
| level | 8/8 | 1.000 | 2 | 2 | XMEAS-7, XMEAS-13, XMEAS-16, XMEAS-30 |
| trend | 8/8 | 1.000 | 2 | 2 | XMEAS-11, XMEAS-20, XMEAS-1, XMEAS-31 |
| residual | 8/8 | 1.000 | 2 | 2 | XMEAS-16, XMEAS-7, XMEAS-13, XMEAS-21 |
| diff | 6/8 | 0.750 | 1 | 1 | XMEAS-16, XMEAS-7, XMEAS-13, XMEAS-10 |
| rapid | 5/8 | 0.625 | 1 | 1 | XMEAS-16, XMEAS-7, XMEAS-13, XMEAS-10 |

#### Batch 9 (`test_case_11`)

| Feature | Active | Fraction | Initial | Late | Dominant top-4 |
|---|---:|---:|---:|---:|---|
| level | 8/8 | 1.000 | 2 | 2 | XMEAS-7, XMEAS-16, XMEAS-13, XMEAS-20 |
| trend | 8/8 | 1.000 | 2 | 2 | XMEAS-15, XMEAS-7, XMEAS-16, XMEAS-13 |
| residual | 8/8 | 1.000 | 2 | 2 | XMEAS-7, XMEAS-16, XMEAS-13, XMEAS-10 |
| diff | 8/8 | 1.000 | 2 | 2 | XMEAS-10, XMEAS-16, XMEAS-7, XMEAS-13 |
| rapid | 8/8 | 1.000 | 2 | 2 | XMEAS-10, XMEAS-7, XMEAS-16, XMEAS-13 |

#### Batch 10 (`test_case_12`)

| Feature | Active | Fraction | Initial | Late | Dominant top-4 |
|---|---:|---:|---:|---:|---|
| level | 8/8 | 1.000 | 2 | 2 | XMEAS-34, XMEAS-20, XMEAS-30, XMEAS-18 |
| trend | 8/8 | 1.000 | 2 | 2 | XMEAS-34, XMEAS-28, XMEAS-7, XMEAS-13 |
| residual | 8/8 | 1.000 | 2 | 2 | XMEAS-7, XMEAS-16, XMEAS-13, XMEAS-10 |
| diff | 5/8 | 0.625 | 0 | 2 | XMEAS-10, XMEAS-16, XMEAS-7, XMEAS-13 |
| rapid | 5/8 | 0.625 | 0 | 2 | XMEAS-10, XMEAS-7, XMEAS-16, XMEAS-13 |

## Top-4 Jaccard across splits

| Class | Feature | Development median | Validation | Test median [range] |
|---|---|---:|---:|---:|
| F1 | level | 0.6000 | 1.0000 | 1.0000 [1.0000, 1.0000] |
| F1 | trend | 0.6000 | 0.3333 | 0.3333 [0.3333, 0.6000] |
| F1 | residual | 0.6000 | 0.6000 | 0.6000 [0.6000, 1.0000] |
| F1 | diff | 0.5000 | 0.2500 | 0.3333 [0.2000, 0.3333] |
| F1 | rapid | 0.5000 | 0.3333 | 0.3333 [0.2500, 0.5000] |
| F10 | level | 1.0000 | 1.0000 | 1.0000 [1.0000, 1.0000] |
| F10 | trend | 0.5000 | 0.6667 | 0.3333 [0.2500, 0.5000] |
| F10 | residual | 0.3667 | 0.6667 | 0.5000 [0.4000, 0.6667] |
| F10 | diff | 0.5000 | 0.2500 | 0.2500 [0.2000, 0.4000] |
| F10 | rapid | 0.5000 | 0.3333 | 0.5000 [0.5000, 1.0000] |
| F13 | level | 0.1429 | 0.3333 | 0.1429 [0.1429, 0.6000] |
| F13 | trend | 0.1429 | 0.3333 | 0.0000 [0.0000, 0.3333] |
| F13 | residual | 1.0000 | 0.6000 | 0.6000 [0.6000, 1.0000] |
| F13 | diff | 1.0000 | 1.0000 | 1.0000 [1.0000, 1.0000] |
| F13 | rapid | 1.0000 | 1.0000 | 1.0000 [1.0000, 1.0000] |
| F8 | level | 0.2381 | 0.6000 | 0.3333 [0.1429, 0.3333] |
| F8 | trend | 0.1429 | 0.3333 | 0.1429 [0.1429, 0.3333] |
| F8 | residual | 0.4667 | 0.6000 | 0.3333 [0.1429, 0.6000] |
| F8 | diff | 1.0000 | 0.6000 | 1.0000 [1.0000, 1.0000] |
| F8 | rapid | 1.0000 | 0.6000 | 1.0000 [1.0000, 1.0000] |
| Normal | level | 0.0000 | undefined | undefined [undefined, undefined] |
| Normal | trend | 0.0000 | 0.0000 | undefined [undefined, undefined] |
| Normal | residual | 0.0000 | 0.0000 | undefined [undefined, undefined] |
| Normal | diff | 0.0000 | 0.0000 | 0.0000 [0.0000, 0.0000] |
| Normal | rapid | undefined | 0.0000 | undefined [undefined, undefined] |

## Dominant-variable recurrence

Full counts are stored in `test_variable_recurrence.csv`. Variables present in all three test top-4 sets:

- F1 / diff: XMEAS-10 (validation 2/2; development 5/5)
- F1 / level: XMEAS-1 (validation 2/2; development 5/5), XMEAS-18 (validation 2/2; development 5/5), XMEAS-34 (validation 2/2; development 3/5), XMEAS-4 (validation 2/2; development 5/5)
- F1 / rapid: XMEAS-10 (validation 2/2; development 5/5)
- F1 / residual: XMEAS-11 (validation 1/2; development 4/5), XMEAS-18 (validation 2/2; development 1/5), XMEAS-20 (validation 2/2; development 5/5)
- F1 / trend: XMEAS-1 (validation 2/2; development 5/5), XMEAS-11 (validation 2/2; development 5/5)
- F10 / diff: XMEAS-18 (validation 2/2; development 5/5)
- F10 / level: XMEAS-18 (validation 2/2; development 5/5)
- F10 / rapid: XMEAS-18 (validation 2/2; development 5/5)
- F10 / residual: XMEAS-18 (validation 2/2; development 5/5), XMEAS-38 (validation 2/2; development 3/5)
- F10 / trend: XMEAS-18 (validation 2/2; development 5/5)
- F13 / diff: XMEAS-10 (validation 2/2; development 5/5), XMEAS-13 (validation 2/2; development 4/5), XMEAS-16 (validation 2/2; development 5/5), XMEAS-7 (validation 2/2; development 5/5)
- F13 / rapid: XMEAS-10 (validation 2/2; development 5/5), XMEAS-13 (validation 2/2; development 4/5), XMEAS-16 (validation 2/2; development 5/5), XMEAS-7 (validation 2/2; development 5/5)
- F13 / residual: XMEAS-13 (validation 2/2; development 5/5), XMEAS-16 (validation 2/2; development 5/5), XMEAS-7 (validation 2/2; development 5/5)
- F8 / diff: XMEAS-1 (validation 2/2; development 5/5), XMEAS-10 (validation 2/2; development 5/5), XMEAS-29 (validation 1/2; development 4/5), XMEAS-31 (validation 2/2; development 5/5)
- F8 / level: XMEAS-1 (validation 2/2; development 3/5)
- F8 / rapid: XMEAS-1 (validation 2/2; development 5/5), XMEAS-10 (validation 2/2; development 5/5), XMEAS-29 (validation 1/2; development 4/5), XMEAS-31 (validation 2/2; development 5/5)
- F8 / residual: XMEAS-1 (validation 2/2; development 4/5)
- F8 / trend: XMEAS-20 (validation 2/2; development 3/5)

## Development–validation–test comparison

| Class | Metric | Development | Validation | Test |
|---|---|---:|---:|---:|
| F1 | intra_similarity | 0.9905 | 0.9892 | 0.9906 |
| F1 | same_class_similarity_to_development | 0.9905 | 0.9889 | 0.9898 |
| F1 | margin | 0.0790 | 0.0751 | 0.0767 |
| F1 | top4_jaccard_level | 0.6000 | 1.0000 | 1.0000 |
| F1 | top4_jaccard_trend | 0.6000 | 0.3333 | 0.3333 |
| F1 | top4_jaccard_residual | 0.6000 | 0.6000 | 0.6000 |
| F1 | top4_jaccard_diff | 0.5000 | 0.2500 | 0.3333 |
| F1 | top4_jaccard_rapid | 0.5000 | 0.3333 | 0.3333 |
| F1 | system_active_fraction_level | 1.0000 | 1.0000 | 1.0000 |
| F1 | system_active_fraction_trend | 0.7500 | 0.7500 | 0.7500 |
| F1 | system_active_fraction_residual | 0.5000 | 0.5000 | 0.5000 |
| F1 | system_active_fraction_diff | 0.1250 | 0.1875 | 0.1250 |
| F1 | system_active_fraction_rapid | 0.1250 | 0.1250 | 0.1250 |
| F10 | intra_similarity | 0.9898 | 0.9935 | 0.9907 |
| F10 | same_class_similarity_to_development | 0.9898 | 0.9922 | 0.9919 |
| F10 | margin | 0.0119 | 0.0163 | 0.0114 |
| F10 | top4_jaccard_level | 1.0000 | 1.0000 | 1.0000 |
| F10 | top4_jaccard_trend | 0.5000 | 0.6667 | 0.3333 |
| F10 | top4_jaccard_residual | 0.3667 | 0.6667 | 0.5000 |
| F10 | top4_jaccard_diff | 0.5000 | 0.2500 | 0.2500 |
| F10 | top4_jaccard_rapid | 0.5000 | 0.3333 | 0.5000 |
| F10 | system_active_fraction_level | 0.8750 | 0.9375 | 0.7500 |
| F10 | system_active_fraction_trend | 1.0000 | 0.8750 | 0.8750 |
| F10 | system_active_fraction_residual | 1.0000 | 1.0000 | 1.0000 |
| F10 | system_active_fraction_diff | 0.8750 | 0.9375 | 1.0000 |
| F10 | system_active_fraction_rapid | 0.8750 | 0.9375 | 1.0000 |
| F13 | intra_similarity | 0.8858 | 0.8970 | 0.8890 |
| F13 | same_class_similarity_to_development | 0.8858 | 0.8886 | 0.8945 |
| F13 | margin | 0.0330 | 0.0450 | 0.0437 |
| F13 | top4_jaccard_level | 0.1429 | 0.3333 | 0.1429 |
| F13 | top4_jaccard_trend | 0.1429 | 0.3333 | 0.0000 |
| F13 | top4_jaccard_residual | 1.0000 | 0.6000 | 0.6000 |
| F13 | top4_jaccard_diff | 1.0000 | 1.0000 | 1.0000 |
| F13 | top4_jaccard_rapid | 1.0000 | 1.0000 | 1.0000 |
| F13 | system_active_fraction_level | 1.0000 | 1.0000 | 1.0000 |
| F13 | system_active_fraction_trend | 1.0000 | 1.0000 | 1.0000 |
| F13 | system_active_fraction_residual | 1.0000 | 1.0000 | 1.0000 |
| F13 | system_active_fraction_diff | 0.8750 | 0.6875 | 0.7500 |
| F13 | system_active_fraction_rapid | 0.8750 | 0.6250 | 0.6250 |
| F8 | intra_similarity | 0.9043 | 0.8956 | 0.8597 |
| F8 | same_class_similarity_to_development | 0.9043 | 0.8983 | 0.8997 |
| F8 | margin | 0.0515 | 0.0436 | 0.0143 |
| F8 | top4_jaccard_level | 0.2381 | 0.6000 | 0.3333 |
| F8 | top4_jaccard_trend | 0.1429 | 0.3333 | 0.1429 |
| F8 | top4_jaccard_residual | 0.4667 | 0.6000 | 0.3333 |
| F8 | top4_jaccard_diff | 1.0000 | 0.6000 | 1.0000 |
| F8 | top4_jaccard_rapid | 1.0000 | 0.6000 | 1.0000 |
| F8 | system_active_fraction_level | 1.0000 | 0.9375 | 1.0000 |
| F8 | system_active_fraction_trend | 1.0000 | 1.0000 | 1.0000 |
| F8 | system_active_fraction_residual | 1.0000 | 1.0000 | 1.0000 |
| F8 | system_active_fraction_diff | 0.7500 | 0.7500 | 0.8750 |
| F8 | system_active_fraction_rapid | 0.7500 | 0.7500 | 0.7500 |
| Normal | intra_similarity | 0.9990 | 0.9984 | 0.9994 |
| Normal | same_class_similarity_to_development | 0.9990 | 0.9986 | 0.9990 |
| Normal | margin | 0.0210 | 0.0212 | 0.0201 |
| Normal | top4_jaccard_level | 0.0000 | undefined | undefined |
| Normal | top4_jaccard_trend | 0.0000 | 0.0000 | undefined |
| Normal | top4_jaccard_residual | 0.0000 | 0.0000 | undefined |
| Normal | top4_jaccard_diff | 0.0000 | 0.0000 | 0.0000 |
| Normal | top4_jaccard_rapid | undefined | 0.0000 | undefined |
| Normal | system_active_fraction_level | 0.0000 | 0.0000 | 0.0000 |
| Normal | system_active_fraction_trend | 0.0000 | 0.1000 | 0.0000 |
| Normal | system_active_fraction_residual | 0.0000 | 0.0500 | 0.0000 |
| Normal | system_active_fraction_diff | 0.0000 | 0.1000 | 0.0000 |
| Normal | system_active_fraction_rapid | 0.0000 | 0.0500 | 0.0000 |

## Final descriptive verdict

No retrospective threshold is introduced. The categories below summarize the
relationship between the pre-existing development and validation distributions
and the frozen test outputs.

### F1 — stable across splits

- Intra-class similarity is `0.99058` in test, compared with `0.99054` in
  development and `0.98924` in validation. Test-to-development and
  test-to-validation medians are `0.98978` and `0.98942`.
- The margin is `0.07670`, between development (`0.07903`) and validation
  (`0.07505`). The largest relevant test inter-class median is F1–Normal at
  `0.91388`.
- Level top-4 Jaccard remains `1.0`; trend, residual, diff, and rapid medians are
  `0.333`, `0.6`, `0.333`, and `0.333`, consistent with validation and within
  the observed development ranges except rapid, whose test minimum reaches
  `0.25` while its median remains at the validation value.
- All three test batches have level `8/8` and late level activity `2/2`.
  Trend is `6/8`, `6/8`, and `5/8`; residual is `4/8`, `5/8`, and `4/8`;
  diff is `2/8`, `1/8`, and `1/8`; rapid is `1/8` in every batch. Batch 9 has
  one late residual-active window, while development and validation generally
  had none. The rest of the temporal counts and the recurring variables
  XMEAS-1/XMEAS-4/XMEAS-18/XMEAS-34, XMEAS-20, and XMEAS-10 are conserved.

### F10 — stable across splits

- Intra-class similarity is `0.99067`, between development (`0.98982`) and
  validation (`0.99354`). Test-to-development similarity is `0.99193` and
  test-to-validation is `0.99256`.
- F10–Normal median similarity is `0.97929`, slightly above development
  (`0.97794`) and validation (`0.97721`). The margin remains positive at
  `0.01139`, close to the original development margin `0.01188` and below the
  validation value `0.01634`. No adjustment follows from this narrow margin.
- XMEAS-18 occurs in all three test top-4 sets for every feature. Level Jaccard
  stays `1.0`; residual and rapid medians are `0.5`; diff remains `0.25`, as in
  validation; trend is `0.333`, at the development minimum.
- Residual is `8/8` in every test batch. Level is `7/8`, `6/8`, and `6/8`;
  trend `6/8`, `8/8`, and `7/8`; diff `8/8` throughout; rapid `8/8`, `8/8`,
  and `7/8`. These counts stay within the combined development/validation
  behavior and retain late activity.

### F13 — moderate distributional variation

- Intra-class test similarity is `0.88899`, between development (`0.88576`)
  and validation (`0.89697`). Test-to-development similarity is `0.89446` and
  test-to-validation is `0.88518`.
- The margin is positive at `0.04367`, close to validation (`0.04497`) and
  above development (`0.03300`).
- Residual top-4 Jaccard is `0.6`; diff and rapid remain `1.0`. XMEAS-7,
  XMEAS-13, and XMEAS-16 recur in all three residual sets, while
  XMEAS-7/XMEAS-10/XMEAS-13/XMEAS-16 recur in all diff and rapid sets. Level
  and trend remain variable, with test Jaccard medians `0.143` and `0.0`.
- Level, trend, and residual are `8/8` in all three batches. Diff is `6/8`,
  `8/8`, and `5/8`; rapid is `5/8`, `8/8`, and `5/8`. The test therefore spans
  both the stronger development activity (`7–8/8`) and the lower validation
  activity (`4–6/8`) while retaining the same diff/rapid variable core.

### F8 — unstable/generalization issue

- Test intra-class median similarity is `0.85967`, below the development range
  `[0.88424, 0.92055]` and validation value `0.89562`. The three pairwise test
  similarities are `0.92037` for batches 8–9, `0.85967` for batches 8–10, and
  `0.85644` for batches 9–10; the loss of intra-class stability is concentrated
  on batch 10.
- Test-to-development median remains `0.89966`, but per-case medians decline
  from `0.91051` (batch 8) and `0.90190` (batch 9) to `0.88522` (batch 10).
  Test-to-validation medians are respectively `0.91858`, `0.91302`, and
  `0.85007`.
- The margin remains positive but contracts to `0.01435`, from `0.05152` in
  development and `0.04362` in validation. F8–F13 is the closest test class
  pair, with median `0.84532`. For batch 10 specifically, median similarity to
  the three F13 test cases is `0.85007`; this is reported as structural
  proximity, not as a reclassification.
- The diff and rapid top-4 sets are nevertheless identical across all three
  test batches (Jaccard `1.0`): XMEAS-1, XMEAS-10, XMEAS-29, and XMEAS-31.
  Level and trend Jaccards return to their development medians (`0.333` and
  `0.143`), while residual Jaccard is `0.333`. In batch 10 the dominant
  residual set includes XMEAS-7, XMEAS-13, and XMEAS-16, unlike batches 8–9.
- Level, trend, and residual remain `8/8` in every test case. Diff is `6/8`,
  `7/8`, and `8/8`; rapid is `6/8`, `6/8`, and `8/8`. Thus the instability is
  not a loss of primary activity, but a change in the structured distribution
  across variables and temporal/sign components.

## Overall conclusion

F1 and F10 are stable across splits. F13 shows moderate distributional
variation while retaining positive separation and a highly recurrent
residual/diff/rapid variable core. F8 shows a test generalization issue driven
by batch 10: its intra-class distribution falls outside the development range
and its margin contracts, although its diff/rapid top-4 core remains stable.

Normal N8–N10 has `0/30` level, `0/30` trend, `0/30` residual, `2/30` diff,
`0/30` rapid, and `2/30` any-primary positive windows. The `6.7%` any-primary
fraction is retained as an observation; it does not trigger recalibration.
No V2 file is changed and no downstream FoT interpretation is started.
