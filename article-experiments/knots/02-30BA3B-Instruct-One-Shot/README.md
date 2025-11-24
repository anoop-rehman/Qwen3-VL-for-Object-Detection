```
Images processed: 3999
Images evaluated: 3999

IoU threshold: 0.50
Ground-truth boxes: 9129
Predicted boxes : 6306
Matches (IoU >= threshold): 3304
Mean IoU (all matches): 0.6834
Mean IoU (label-correct matches): 0.6923
Label accuracy (within matched boxes): 0.4252

Per-class metrics:
Class                     TP    FP    FN     Prec   Recall       F1  Mean IoU
-----------------------------------------------------------------------------
crack                    125   492   388    0.203    0.244    0.221     0.705
dead_knot               1140  3384  1773    0.252    0.391    0.307     0.688
knot_missing               7   215   111    0.032    0.059    0.041     0.675
knot_with_crack            9    60   512    0.130    0.017    0.031     0.711
live_knot                 41    77  4005    0.347    0.010    0.020     0.666
marrow                     0    32   206    0.000    0.000    0.000     0.000
quartzity                  1   466   164    0.002    0.006    0.003     0.617
resin                     82   175   565    0.319    0.127    0.181     0.752

Micro-averaged metrics:
Precision: 0.2228
Recall   : 0.1539
F1       : 0.1821

Label confusions (IoU ok, label mismatch):
Actual live_knot predicted as dead_knot: 1127
Actual knot_with_crack predicted as dead_knot: 214
Actual resin predicted as crack: 67
Actual dead_knot predicted as knot_missing: 56
Actual marrow predicted as resin: 54
Actual marrow predicted as crack: 46
Actual live_knot predicted as knot_missing: 44
Actual dead_knot predicted as crack: 38
Actual resin predicted as dead_knot: 30
Actual live_knot predicted as crack: 28
Actual dead_knot predicted as quartzity: 22
Actual resin predicted as quartzity: 21
Actual live_knot predicted as quartzity: 21
Actual quartzity predicted as crack: 14
Actual marrow predicted as dead_knot: 13
Actual knot_with_crack predicted as live_knot: 12
Actual knot_with_crack predicted as knot_missing: 12
Actual dead_knot predicted as resin: 12
Actual quartzity predicted as resin: 9
Actual live_knot predicted as knot_with_crack: 9
Actual marrow predicted as quartzity: 8
Actual dead_knot predicted as knot_with_crack: 7
Actual dead_knot predicted as live_knot: 7
Actual knot_missing predicted as dead_knot: 6
Actual resin predicted as knot_with_crack: 4
Actual knot_missing predicted as resin: 4
Actual knot_with_crack predicted as crack: 4
Actual quartzity predicted as dead_knot: 3
Actual live_knot predicted as resin: 3
Actual resin predicted as knot_missing: 2
Actual quartzity predicted as knot_missing: 1
Actual knot_with_crack predicted as quartzity: 1
```
