# NOTES.md — Week 8: Drift and Observability Monitoring

**Student ID used with `generate_for_student.py`:**
142301040


## Drift level vs. expectation

The pipeline gave moderate drift with a PSI of 0.1381. This makes sense since camera_A is daylight and camera_B is low light. On camera_A all detections had a 0.98 confidence score, but on camera_B scores dropped as low as 0.817, which shifted the distribution.


## What confidence-score-only monitoring misses

Confidence scores only show if predictions shifted, not whether they are actually right. The model could give high confidence on false positives or miss cars entirely. If ground truth labels are available later, I would track mAP, precision, and recall to monitor actual detection accuracy.
