```
Images processed: 3999
Images evaluated: 3999

IoU threshold: 0.50
Ground-truth boxes: 9129
Predicted boxes : 8209
Matches (IoU >= threshold): 3560
Mean IoU (all matches): 0.6685
Mean IoU (label-correct matches): 0.6719
Label accuracy (within matched boxes): 0.5601

Per-class metrics:
Class                     TP    FP    FN     Prec   Recall       F1  Mean IoU
-----------------------------------------------------------------------------
crack                    158   970   355    0.140    0.308    0.193     0.688
dead_knot               1102  2911  1811    0.275    0.378    0.318     0.666
knot_missing              13   117   105    0.100    0.110    0.105     0.746
knot_with_crack           89   350   432    0.203    0.171    0.185     0.716
live_knot                457  1368  3589    0.250    0.113    0.156     0.656
marrow                     0    71   206    0.000    0.000    0.000     0.000
quartzity                  0    16   165    0.000    0.000    0.000     0.000
resin                    175   412   472    0.298    0.270    0.284     0.709

Micro-averaged metrics:
Precision: 0.2429
Recall   : 0.2184
F1       : 0.2300

Label confusions (IoU ok, label mismatch):
Actual live_knot predicted as dead_knot: 718
Actual dead_knot predicted as live_knot: 175
Actual resin predicted as crack: 105
Actual marrow predicted as crack: 80
Actual knot_with_crack predicted as live_knot: 77
Actual knot_with_crack predicted as dead_knot: 67
Actual resin predicted as dead_knot: 50
Actual live_knot predicted as knot_with_crack: 49
Actual marrow predicted as resin: 37
Actual live_knot predicted as crack: 33
Actual dead_knot predicted as knot_missing: 25
Actual dead_knot predicted as crack: 23
Actual quartzity predicted as crack: 20
Actual knot_missing predicted as dead_knot: 16
Actual live_knot predicted as knot_missing: 15
Actual dead_knot predicted as resin: 15
Actual dead_knot predicted as knot_with_crack: 11
Actual quartzity predicted as resin: 8
Actual marrow predicted as dead_knot: 8
Actual live_knot predicted as resin: 7
Actual knot_missing predicted as resin: 7
Actual knot_missing predicted as crack: 5
Actual resin predicted as live_knot: 3
Actual resin predicted as knot_missing: 2
Actual knot_with_crack predicted as crack: 2
Actual crack predicted as knot_with_crack: 1
Actual live_knot predicted as marrow: 1
Actual resin predicted as marrow: 1
Actual marrow predicted as knot_with_crack: 1
Actual quartzity predicted as dead_knot: 1
Actual dead_knot predicted as marrow: 1
Actual knot_with_crack predicted as knot_missing: 1
Actual crack predicted as live_knot: 1
```
