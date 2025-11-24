```
Images processed: 3999
Images evaluated: 3999

IoU threshold: 0.50
Ground-truth boxes: 9129
Predicted boxes : 8026
Matches (IoU >= threshold): 3566
Mean IoU (all matches): 0.6735
Mean IoU (label-correct matches): 0.6679
Label accuracy (within matched boxes): 0.5373

Per-class metrics:
Class                     TP    FP    FN     Prec   Recall       F1  Mean IoU
-----------------------------------------------------------------------------
crack                    175  1137   338    0.133    0.341    0.192     0.711
dead_knot                712  1277  2201    0.358    0.244    0.290     0.660
knot_missing               0     6   118    0.000    0.000    0.000     0.000
knot_with_crack           59   432   462    0.120    0.113    0.117     0.695
live_knot                787  2335  3259    0.252    0.195    0.220     0.653
marrow                     0    28   206    0.000    0.000    0.000     0.000
quartzity                  0    16   165    0.000    0.000    0.000     0.000
resin                    183   879   464    0.172    0.283    0.214     0.711

Micro-averaged metrics:
Precision: 0.2387
Recall   : 0.2099
F1       : 0.2234

Label confusions (IoU ok, label mismatch):
Actual dead_knot predicted as live_knot: 549
Actual live_knot predicted as dead_knot: 373
Actual knot_with_crack predicted as live_knot: 139
Actual resin predicted as crack: 91
Actual dead_knot predicted as crack: 59
Actual marrow predicted as resin: 57
Actual marrow predicted as crack: 49
Actual live_knot predicted as knot_with_crack: 48
Actual dead_knot predicted as resin: 48
Actual knot_with_crack predicted as dead_knot: 37
Actual live_knot predicted as crack: 32
Actual dead_knot predicted as knot_with_crack: 28
Actual live_knot predicted as resin: 24
Actual resin predicted as dead_knot: 22
Actual knot_missing predicted as dead_knot: 21
Actual quartzity predicted as crack: 17
Actual quartzity predicted as resin: 8
Actual knot_missing predicted as crack: 6
Actual marrow predicted as live_knot: 6
Actual marrow predicted as knot_with_crack: 5
Actual resin predicted as knot_with_crack: 4
Actual resin predicted as live_knot: 4
Actual marrow predicted as dead_knot: 4
Actual quartzity predicted as knot_with_crack: 3
Actual knot_missing predicted as resin: 3
Actual resin predicted as quartzity: 2
Actual quartzity predicted as dead_knot: 2
Actual quartzity predicted as live_knot: 2
Actual knot_with_crack predicted as crack: 2
Actual dead_knot predicted as marrow: 1
Actual crack predicted as live_knot: 1
Actual crack predicted as resin: 1
Actual crack predicted as knot_with_crack: 1
Actual crack predicted as dead_knot: 1
```
