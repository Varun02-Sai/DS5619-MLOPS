# NOTES.md — Week 10: Fairness and Robustness Audit

**Student ID used with `generate_for_student.py`:**
142301040


## Which classes got flagged?

Two-wheeler (78.6%), Bicycle (82.4%), and Sedan (89.5%) fell below the 90% recall bar.

Two-wheelers and bicycles were expected to fail because the generator draws them with smaller box sizes (0.45 and 0.35 multipliers), so they have fewer red pixels and get missed more easily. Sedan (17/19 detected) is just sampling noise—missing two boxes in a small sample dropped it to 89.5%, which isn't a structural issue like the smaller vehicles.


## If the grouping variable were a protected attribute

With vehicle classes, a lower recall just means we miscount some bikes in traffic. But if the groups were protected demographic attributes like race or gender, disparities directly affect people's lives and carry legal consequences. As an engineer, you can't just log the gap and move on—you're obligated to actively fix it (like rebalancing data or tuning group thresholds) before deploying.


## Which attack could corrupt this audit?

Data poisoning during data collection or labeling. An attacker could shift ground-truth boxes or mislabel test images to make certain classes look artificially good or bad, hiding real disparities. A control from lecture is dataset versioning and file hashing (like DVC) so any changes to the test data are caught immediately.


## Would SHAP or LIME explain a missed detection?

No. SHAP and LIME are built for classification models that output a single probability for a fixed input. Object detection outputs variable bounding boxes across an image. When the detector misses an object completely, there is no output score to perturb or explain. In this detector, the bike was missed because it had fewer than 20 contiguous red pixels or didn't meet the 0.3 IoU overlap, which feature attribution tools can't tell you.


## What did your attack show?

As eps increased from 0 to 40, recall dropped across the board. By eps=20, Bicycle dropped by 29.4% (82.4% to 52.9%), Tempo-traveller dropped by 26.7% (100% to 73.3%), and SUV dropped by 22.2% (100% to 77.8%). Bicycle was the most fragile and was already flagged in the clean audit.

The biggest drop ranking (Bicycle, Tempo-traveller, SUV) doesn't match the lowest recall ranking (Bicycle, Two-wheeler, Tempo-traveller). Lowest recall is the better measure of real harm because it shows who is actually being missed the most. Two-wheeler didn't have the biggest drop only because it was already low at baseline (78.6%), showing that already weak classes suffer the worst final performance.

For this detector, input validation could check for abnormal color shifts (like unusually low red or high green/blue) before running inference. Adversarial training would mean including color-shifted images when tuning detection thresholds. This rule breaks easily because of hardcoded color cutoffs (r > 120, r - g > 40), so a tiny shift pushes pixels out. A CNN is less brittle to simple color shifts because it learns textures and spatial shapes across many layers, though it can still be tricked by other adversarial patterns.
