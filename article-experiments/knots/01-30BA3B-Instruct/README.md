```
Images processed: 4000
Images evaluated: 4000

IoU threshold: 0.50
Ground-truth boxes: 9134
Predicted boxes : 13975
Matches (IoU >= threshold): 4535
Mean IoU (all matches): 0.6794
Mean IoU (label-correct matches): 0.6805
Label accuracy (within matched boxes): 0.4088

Per-class metrics:
Class                     TP    FP    FN     Prec   Recall       F1  Mean IoU
-----------------------------------------------------------------------------
crack                    206  2081   307    0.090    0.402    0.147     0.725
dead_knot               1293  4306  1620    0.231    0.444    0.304     0.675
knot_missing               4   873   114    0.005    0.034    0.008     0.717
knot_with_crack           37  1084   487    0.033    0.071    0.045     0.689
live_knot                285  1795  3762    0.137    0.070    0.093     0.662
marrow                     1   417   205    0.002    0.005    0.003     0.645
quartzity                  0   901   165    0.000    0.000    0.000     0.000
resin                     28   664   620    0.040    0.043    0.042     0.777

Micro-averaged metrics:
Precision: 0.1327
Recall   : 0.2030
F1       : 0.1605

Label confusions (IoU ok, label mismatch):
Actual live_knot predicted as dead_knot: 1135
Actual dead_knot predicted as live_knot: 229
Actual knot_with_crack predicted as dead_knot: 185
Actual resin predicted as crack: 181
Actual live_knot predicted as knot_missing: 90
Actual marrow predicted as crack: 84
Actual dead_knot predicted as knot_with_crack: 84
Actual resin predicted as dead_knot: 81
Actual live_knot predicted as knot_with_crack: 81
Actual dead_knot predicted as crack: 80
Actual dead_knot predicted as knot_missing: 74
Actual live_knot predicted as crack: 71
Actual knot_with_crack predicted as live_knot: 47
Actual marrow predicted as dead_knot: 30
Actual resin predicted as live_knot: 29
Actual quartzity predicted as crack: 21
Actual resin predicted as knot_missing: 19
Actual resin predicted as knot_with_crack: 19
Actual knot_missing predicted as dead_knot: 19
Actual quartzity predicted as dead_knot: 13
Actual knot_missing predicted as crack: 13
Actual dead_knot predicted as quartzity: 13
Actual knot_with_crack predicted as knot_missing: 10
Actual marrow predicted as knot_missing: 9
Actual marrow predicted as live_knot: 7
Actual resin predicted as quartzity: 6
Actual live_knot predicted as quartzity: 6
Actual marrow predicted as resin: 6
Actual knot_missing predicted as live_knot: 5
Actual dead_knot predicted as resin: 5
Actual crack predicted as knot_with_crack: 5
Actual marrow predicted as knot_with_crack: 5
Actual knot_with_crack predicted as crack: 5
Actual live_knot predicted as resin: 4
Actual knot_missing predicted as resin: 2
Actual live_knot predicted as marrow: 2
Actual quartzity predicted as knot_missing: 2
Actual knot_with_crack predicted as marrow: 1
Actual knot_with_crack predicted as quartzity: 1
Actual quartzity predicted as live_knot: 1
Actual knot_missing predicted as knot_with_crack: 1
```
