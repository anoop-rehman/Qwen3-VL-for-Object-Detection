```
Images processed: 3935
Images evaluated: 3935

IoU threshold: 0.50
Ground-truth boxes: 9006
Predicted boxes : 8203
Matches (IoU >= threshold): 3672
Mean IoU (all matches): 0.6834
Mean IoU (label-correct matches): 0.6791
Label accuracy (within matched boxes): 0.5158

Per-class metrics:
Class                     TP    FP    FN     Prec   Recall       F1  Mean IoU
-----------------------------------------------------------------------------
crack                    147   627   364    0.190    0.288    0.229     0.733
dead_knot                867  2161  1999    0.286    0.303    0.294     0.681
knot_missing               5    74   111    0.063    0.043    0.051     0.710
knot_with_crack           54   288   466    0.158    0.104    0.125     0.730
live_knot                766  2759  3222    0.217    0.192    0.204     0.659
marrow                     3    56   200    0.051    0.015    0.023     0.811
quartzity                  0    12   164    0.000    0.000    0.000     0.000
resin                     52   332   586    0.135    0.082    0.102     0.734

Micro-averaged metrics:
Precision: 0.2309
Recall   : 0.2103
F1       : 0.2201

Label confusions (IoU ok, label mismatch):
Actual dead_knot predicted as live_knot: 546
Actual live_knot predicted as dead_knot: 518
Actual resin predicted as dead_knot: 136
Actual resin predicted as crack: 104
Actual knot_with_crack predicted as live_knot: 100
Actual marrow predicted as crack: 76
Actual knot_with_crack predicted as dead_knot: 42
Actual live_knot predicted as knot_with_crack: 39
Actual knot_missing predicted as dead_knot: 26
Actual dead_knot predicted as knot_missing: 24
Actual dead_knot predicted as crack: 23
Actual dead_knot predicted as knot_with_crack: 22
Actual marrow predicted as dead_knot: 20
Actual live_knot predicted as crack: 18
Actual quartzity predicted as crack: 17
Actual resin predicted as live_knot: 12
Actual live_knot predicted as knot_missing: 12
Actual quartzity predicted as dead_knot: 6
Actual dead_knot predicted as resin: 6
Actual marrow predicted as resin: 6
Actual knot_missing predicted as live_knot: 5
Actual resin predicted as knot_with_crack: 3
Actual knot_with_crack predicted as crack: 3
Actual live_knot predicted as marrow: 3
Actual quartzity predicted as resin: 2
Actual resin predicted as marrow: 2
Actual knot_missing predicted as crack: 2
Actual knot_missing predicted as resin: 1
Actual dead_knot predicted as marrow: 1
Actual live_knot predicted as resin: 1
Actual quartzity predicted as live_knot: 1
Actual crack predicted as dead_knot: 1
```
