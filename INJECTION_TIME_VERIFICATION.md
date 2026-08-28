# Injection time verification

This document separates source evidence from an empirical consistency check.

## Scope

- Dataset snapshot: `309b944f35ac440ff0c70616947ffe723c766e14`.
- Empirical data: F1/F8/F10/F13 development batches 1–5 only.
- Normal baseline: development blocks N1–N5 only.
- Windows compared: `[0,5 h)`, `[5,10 h)`, and `[10,15 h)`.
- Features and thresholds are the frozen V2 definitions; no value was tuned.
- No claim of statistical identity is made; no hypothesis test is performed.

## Source evidence

At the pinned dataset commit:

1. `simulator/auto_run.m:8-16` creates `dist=zeros(1,28)`, sets `dist(faultNum)=1`, and calls `sim(modelName)`.
2. `simulator/MultiLoop_mode1.mdl:7774-7778` defines SID 3, a Constant named `Disturbances`, with value `dist` and sample time `Inf`.
3. `simulator/MultiLoop_mode1.mdl:7849-7854` defines SID 250 as a `VariableTransportDelay` with two inputs and `MaximumDelay=20`. The maximum is a capacity parameter, not the applied delay.
4. `simulator/MultiLoop_mode1.mdl:7769-7773` defines SID 249 as a Constant with value `10`; lines `8046-8051` connect SID 249 output 1 to SID 250 input 2, proving the applied delay signal is 10.
5. Lines `8063-8067` connect SID 3 output 1 (`dist`) to SID 250 input 1. Lines `8057-8062` connect SID 250 output 1 to plant subsystem SID 31 input 13; the plant `Disturbances` inport is port 13 at lines `4800-4804`.
6. `InitialOutput` is not serialized in this R2024b model. The compatible Simulink default is zero, as recorded in the pre-validation source audit. Together with the explicit delay-input signal, this yields zero disturbance output before 10 simulation-time units.
7. `auto_run.m:18-21,37` identifies elapsed time and the saved `Time (h)` column in hours. The dataset has one-minute sampling and a 50 h stop time, so the delay value corresponds to 10 h.

The documented routing is therefore:

`dist -> VariableTransportDelay data input; Constant(10) -> delay input; delayed output -> plant input 13`.

## Empirical consistency check

Each table entry is the number of development batches whose maximum over 41 XMEAS strictly exceeds the already-frozen feature threshold.

| Fault | Interval | Level | Trend | Residual | Diff | Any primary |
|---|---|---:|---:|---:|---:|---:|
| F1 | 0-5h | 0/5 | 0/5 | 0/5 | 0/5 | 0/5 |
| F1 | 5-10h | 0/5 | 1/5 | 0/5 | 0/5 | 1/5 |
| F1 | 10-15h | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 |
| F8 | 0-5h | 0/5 | 0/5 | 0/5 | 0/5 | 0/5 |
| F8 | 5-10h | 0/5 | 0/5 | 0/5 | 0/5 | 0/5 |
| F8 | 10-15h | 5/5 | 5/5 | 5/5 | 3/5 | 5/5 |
| F10 | 0-5h | 0/5 | 0/5 | 0/5 | 0/5 | 0/5 |
| F10 | 5-10h | 0/5 | 0/5 | 0/5 | 0/5 | 0/5 |
| F10 | 10-15h | 3/5 | 5/5 | 5/5 | 4/5 | 5/5 |
| F13 | 0-5h | 0/5 | 0/5 | 0/5 | 0/5 | 0/5 |
| F13 | 5-10h | 0/5 | 0/5 | 0/5 | 0/5 | 0/5 |
| F13 | 10-15h | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 |

### Score magnitude relative to frozen thresholds

Median and maximum refer to the five batch-level maxima; 1.0 is the frozen activation boundary.

| Fault | Interval | Feature | Median score/threshold | Maximum score/threshold |
|---|---|---|---:|---:|
| F1 | 0-5h | level | 0.274 | 0.425 |
| F1 | 0-5h | trend | 0.401 | 0.730 |
| F1 | 0-5h | residual | 0.849 | 0.894 |
| F1 | 0-5h | diff | 0.895 | 0.914 |
| F1 | 5-10h | level | 0.318 | 0.676 |
| F1 | 5-10h | trend | 0.478 | 1.208 |
| F1 | 5-10h | residual | 0.859 | 0.874 |
| F1 | 5-10h | diff | 0.863 | 0.897 |
| F1 | 10-15h | level | 38.766 | 38.975 |
| F1 | 10-15h | trend | 41.794 | 41.881 |
| F1 | 10-15h | residual | 10.022 | 10.096 |
| F1 | 10-15h | diff | 1.315 | 1.363 |
| F8 | 0-5h | level | 0.328 | 0.393 |
| F8 | 0-5h | trend | 0.526 | 0.734 |
| F8 | 0-5h | residual | 0.817 | 0.850 |
| F8 | 0-5h | diff | 0.838 | 0.970 |
| F8 | 5-10h | level | 0.370 | 0.559 |
| F8 | 5-10h | trend | 0.527 | 0.630 |
| F8 | 5-10h | residual | 0.861 | 0.885 |
| F8 | 5-10h | diff | 0.853 | 0.944 |
| F8 | 10-15h | level | 12.031 | 14.690 |
| F8 | 10-15h | trend | 11.416 | 17.049 |
| F8 | 10-15h | residual | 5.889 | 14.995 |
| F8 | 10-15h | diff | 1.119 | 1.450 |
| F10 | 0-5h | level | 0.290 | 0.439 |
| F10 | 0-5h | trend | 0.573 | 0.816 |
| F10 | 0-5h | residual | 0.873 | 0.907 |
| F10 | 0-5h | diff | 0.951 | 0.987 |
| F10 | 5-10h | level | 0.321 | 0.481 |
| F10 | 5-10h | trend | 0.452 | 0.782 |
| F10 | 5-10h | residual | 0.813 | 0.866 |
| F10 | 5-10h | diff | 0.854 | 0.920 |
| F10 | 10-15h | level | 3.088 | 5.496 |
| F10 | 10-15h | trend | 3.190 | 5.966 |
| F10 | 10-15h | residual | 8.904 | 13.882 |
| F10 | 10-15h | diff | 1.166 | 1.984 |
| F13 | 0-5h | level | 0.273 | 0.352 |
| F13 | 0-5h | trend | 0.357 | 0.466 |
| F13 | 0-5h | residual | 0.809 | 0.973 |
| F13 | 0-5h | diff | 0.834 | 0.918 |
| F13 | 5-10h | level | 0.388 | 0.710 |
| F13 | 5-10h | trend | 0.523 | 0.660 |
| F13 | 5-10h | residual | 0.871 | 0.976 |
| F13 | 5-10h | diff | 0.885 | 0.984 |
| F13 | 10-15h | level | 4.489 | 5.820 |
| F13 | 10-15h | trend | 9.072 | 18.431 |
| F13 | 10-15h | residual | 9.955 | 27.169 |
| F13 | 10-15h | diff | 1.561 | 2.765 |

### Variables active in at least four of five batches

- F1, 10-15h, diff: XMEAS-10 (5/5)
- F1, 10-15h, level: XMEAS-1 (5/5), XMEAS-10 (5/5), XMEAS-11 (5/5), XMEAS-13 (5/5), XMEAS-15 (5/5), XMEAS-16 (5/5), XMEAS-18 (5/5), XMEAS-20 (5/5), XMEAS-21 (5/5), XMEAS-22 (5/5), XMEAS-23 (5/5), XMEAS-24 (5/5), XMEAS-25 (5/5), XMEAS-26 (5/5), XMEAS-27 (5/5), XMEAS-28 (5/5), XMEAS-29 (5/5), XMEAS-30 (5/5), XMEAS-31 (5/5), XMEAS-33 (5/5), XMEAS-34 (5/5), XMEAS-35 (5/5), XMEAS-36 (5/5), XMEAS-38 (5/5), XMEAS-4 (5/5), XMEAS-5 (5/5), XMEAS-6 (5/5), XMEAS-7 (5/5)
- F1, 10-15h, residual: XMEAS-1 (5/5), XMEAS-10 (5/5), XMEAS-11 (5/5), XMEAS-12 (5/5), XMEAS-13 (5/5), XMEAS-14 (5/5), XMEAS-15 (5/5), XMEAS-16 (5/5), XMEAS-18 (5/5), XMEAS-20 (5/5), XMEAS-21 (5/5), XMEAS-22 (5/5), XMEAS-23 (5/5), XMEAS-24 (5/5), XMEAS-25 (5/5), XMEAS-28 (5/5), XMEAS-29 (5/5), XMEAS-30 (5/5), XMEAS-31 (5/5), XMEAS-33 (5/5), XMEAS-34 (5/5), XMEAS-38 (5/5), XMEAS-4 (5/5), XMEAS-5 (5/5), XMEAS-6 (5/5), XMEAS-7 (5/5), XMEAS-26 (4/5), XMEAS-35 (4/5)
- F1, 10-15h, trend: XMEAS-1 (5/5), XMEAS-10 (5/5), XMEAS-11 (5/5), XMEAS-12 (5/5), XMEAS-13 (5/5), XMEAS-14 (5/5), XMEAS-15 (5/5), XMEAS-16 (5/5), XMEAS-18 (5/5), XMEAS-20 (5/5), XMEAS-21 (5/5), XMEAS-22 (5/5), XMEAS-24 (5/5), XMEAS-25 (5/5), XMEAS-27 (5/5), XMEAS-28 (5/5), XMEAS-29 (5/5), XMEAS-3 (5/5), XMEAS-30 (5/5), XMEAS-31 (5/5), XMEAS-33 (5/5), XMEAS-34 (5/5), XMEAS-35 (5/5), XMEAS-36 (5/5), XMEAS-38 (5/5), XMEAS-4 (5/5), XMEAS-7 (5/5)
- F8, 10-15h, level: XMEAS-1 (5/5), XMEAS-11 (4/5), XMEAS-18 (4/5), XMEAS-20 (4/5)
- F8, 10-15h, residual: XMEAS-1 (5/5), XMEAS-10 (5/5), XMEAS-11 (5/5), XMEAS-13 (5/5), XMEAS-16 (5/5), XMEAS-18 (5/5), XMEAS-20 (5/5), XMEAS-21 (5/5), XMEAS-22 (5/5), XMEAS-23 (5/5), XMEAS-25 (5/5), XMEAS-29 (5/5), XMEAS-31 (5/5), XMEAS-5 (5/5), XMEAS-6 (5/5), XMEAS-7 (5/5), XMEAS-28 (4/5), XMEAS-34 (4/5)
- F8, 10-15h, trend: XMEAS-10 (5/5), XMEAS-20 (5/5), XMEAS-25 (5/5), XMEAS-29 (5/5), XMEAS-31 (5/5), XMEAS-1 (4/5), XMEAS-11 (4/5), XMEAS-18 (4/5), XMEAS-21 (4/5), XMEAS-22 (4/5), XMEAS-23 (4/5), XMEAS-38 (4/5)
- F10, 10-15h, diff: XMEAS-18 (4/5)
- F10, 10-15h, residual: XMEAS-18 (5/5)
- F10, 10-15h, trend: XMEAS-18 (5/5)
- F13, 10-15h, diff: XMEAS-10 (5/5)
- F13, 10-15h, level: XMEAS-30 (5/5), XMEAS-34 (5/5), XMEAS-10 (4/5), XMEAS-13 (4/5), XMEAS-16 (4/5), XMEAS-24 (4/5), XMEAS-28 (4/5), XMEAS-7 (4/5)
- F13, 10-15h, residual: XMEAS-10 (5/5), XMEAS-11 (5/5), XMEAS-13 (5/5), XMEAS-15 (5/5), XMEAS-16 (5/5), XMEAS-18 (5/5), XMEAS-21 (5/5), XMEAS-22 (5/5), XMEAS-24 (5/5), XMEAS-28 (5/5), XMEAS-30 (5/5), XMEAS-34 (5/5), XMEAS-7 (5/5), XMEAS-12 (4/5), XMEAS-20 (4/5)
- F13, 10-15h, trend: XMEAS-10 (5/5), XMEAS-13 (5/5), XMEAS-16 (5/5), XMEAS-24 (5/5), XMEAS-28 (5/5), XMEAS-30 (5/5), XMEAS-34 (5/5), XMEAS-7 (5/5), XMEAS-1 (4/5), XMEAS-11 (4/5), XMEAS-15 (4/5), XMEAS-18 (4/5), XMEAS-20 (4/5), XMEAS-33 (4/5)

## Conclusion

Across the frozen feature thresholds, no feature produces a recurring five-of-five fault response in either pre-10 h window, whereas every fault has an any-primary response in five of five batches in `[10,15 h)`.

No systematic fault signature is detectable before 10 h, while the expected disturbance response appears after 10 h, consistent with the 10 h transport-delay path documented in the simulator.

This empirical result is a consistency check, not the primary proof of injection time.
