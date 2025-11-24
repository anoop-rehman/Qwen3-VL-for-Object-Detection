```
Images processed: 3997
Images evaluated: 3997

IoU threshold: 0.50
Ground-truth boxes: 9132
Predicted boxes : 8900
Matches (IoU >= threshold): 3443
Mean IoU (all matches): 0.6720
Mean IoU (label-correct matches): 0.6605
Label accuracy (within matched boxes): 0.4415

Per-class metrics:
Class                     TP    FP    FN     Prec   Recall       F1  Mean IoU
-----------------------------------------------------------------------------
crack                    158  1251   355    0.112    0.308    0.164     0.708
dead_knot                600  1916  2313    0.238    0.206    0.221     0.657
knot_missing               1    13   117    0.071    0.008    0.015     0.626
knot_with_crack           74  1083   450    0.064    0.141    0.088     0.700
live_knot                649  2766  3396    0.190    0.160    0.174     0.645
marrow                     0     7   206    0.000    0.000    0.000     0.000
quartzity                  0     9   165    0.000    0.000    0.000     0.000
resin                     38   335   610    0.102    0.059    0.074     0.717

Micro-averaged metrics:
Precision: 0.1708
Recall   : 0.1664
F1       : 0.1686

Label confusions (IoU ok, label mismatch):
Actual dead_knot predicted as live_knot: 692
Actual live_knot predicted as dead_knot: 406
Actual resin predicted as crack: 120
Actual resin predicted as dead_knot: 88
Actual knot_with_crack predicted as live_knot: 87
Actual live_knot predicted as knot_with_crack: 85
Actual dead_knot predicted as knot_with_crack: 84
Actual marrow predicted as crack: 51
Actual marrow predicted as dead_knot: 38
Actual knot_with_crack predicted as dead_knot: 37
Actual dead_knot predicted as crack: 35
Actual live_knot predicted as crack: 32
Actual resin predicted as live_knot: 24
Actual knot_missing predicted as dead_knot: 20
Actual marrow predicted as knot_with_crack: 17
Actual resin predicted as knot_with_crack: 16
Actual marrow predicted as live_knot: 13
Actual quartzity predicted as live_knot: 12
Actual quartzity predicted as crack: 9
Actual knot_missing predicted as crack: 8
Actual quartzity predicted as knot_with_crack: 7
Actual knot_with_crack predicted as crack: 7
Actual knot_missing predicted as knot_with_crack: 6
Actual crack predicted as knot_with_crack: 6
Actual dead_knot predicted as resin: 4
Actual quartzity predicted as dead_knot: 3
Actual knot_missing predicted as live_knot: 3
Actual dead_knot predicted as knot_missing: 3
Actual live_knot predicted as knot_missing: 3
Actual marrow predicted as resin: 3
Actual live_knot predicted as resin: 2
Actual dead_knot predicted as marrow: 1
Actual crack predicted as live_knot: 1
```
