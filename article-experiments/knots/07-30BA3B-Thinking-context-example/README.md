```
Images processed: 3911
Images evaluated: 3911

IoU threshold: 0.50
Ground-truth boxes: 8926
Predicted boxes : 6180
Matches (IoU >= threshold): 2739
Mean IoU (all matches): 0.6694
Mean IoU (label-correct matches): 0.6762
Label accuracy (within matched boxes): 0.4790

Per-class metrics:
Class                     TP    FP    FN     Prec   Recall       F1  Mean IoU
-----------------------------------------------------------------------------
crack                    126  1228   381    0.093    0.249    0.135     0.697
dead_knot                932  2149  1925    0.302    0.326    0.314     0.668
knot_missing               1    97   117    0.010    0.008    0.009     0.731
knot_with_crack           93   935   412    0.090    0.184    0.121     0.683
live_knot                 57   127  3878    0.310    0.014    0.028     0.674
marrow                     0    12   203    0.000    0.000    0.000     0.000
quartzity                  0    86   164    0.000    0.000    0.000     0.000
resin                    103   234   534    0.306    0.162    0.211     0.721

Micro-averaged metrics:
Precision: 0.2123
Recall   : 0.1470
F1       : 0.1737

Label confusions (IoU ok, label mismatch):
Actual live_knot predicted as dead_knot: 635
Actual live_knot predicted as knot_with_crack: 138
Actual dead_knot predicted as knot_with_crack: 108
Actual marrow predicted as resin: 87
Actual resin predicted as crack: 87
Actual knot_with_crack predicted as dead_knot: 62
Actual dead_knot predicted as crack: 59
Actual live_knot predicted as crack: 44
Actual dead_knot predicted as live_knot: 29
Actual dead_knot predicted as knot_missing: 27
Actual resin predicted as dead_knot: 25
Actual marrow predicted as crack: 16
Actual knot_missing predicted as dead_knot: 15
Actual quartzity predicted as resin: 13
Actual live_knot predicted as knot_missing: 12
Actual knot_with_crack predicted as live_knot: 12
Actual resin predicted as quartzity: 10
Actual marrow predicted as dead_knot: 8
Actual quartzity predicted as crack: 7
Actual knot_missing predicted as crack: 5
Actual dead_knot predicted as quartzity: 5
Actual resin predicted as knot_with_crack: 3
Actual live_knot predicted as quartzity: 3
Actual dead_knot predicted as resin: 3
Actual quartzity predicted as dead_knot: 2
Actual knot_with_crack predicted as crack: 2
Actual knot_with_crack predicted as quartzity: 1
Actual crack predicted as live_knot: 1
Actual resin predicted as live_knot: 1
Actual crack predicted as resin: 1
Actual knot_missing predicted as live_knot: 1
Actual knot_missing predicted as knot_with_crack: 1
Actual marrow predicted as knot_with_crack: 1
Actual quartzity predicted as marrow: 1
Actual crack predicted as dead_knot: 1
Actual knot_missing predicted as resin: 1
```
