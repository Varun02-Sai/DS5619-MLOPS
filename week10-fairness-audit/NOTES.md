# NOTES.md — Week 10: Fairness and Robustness Audit

**Student ID used with `generate_for_student.py`:**
142301040


## Which classes got flagged?

The clean audit flagged Two-wheeler (78.6%), Bicycle (82.4%), and Sedan (89.5%) below the 90% threshold.

Two-wheeler and Bicycle falling short was expected because `generate_for_student.py` uses small box size multipliers (0.45 and 0.35) for them. Smaller drawn boxes produce fewer red pixels, making it harder for them to reach the detector's 20-pixel connected component threshold, especially in low light. Sedan at 89.5% (17 out of 19 detected) is just sampling noise. Missing only two boxes in a small test set drops the score under 90%, unlike the small vehicles which have a clear structural disadvantage.


## If the grouping variable were a protected attribute

If the grouping variable were a protected demographic attribute (like gender, race, or disability) rather than vehicle categories, the stakes become ethical and legal rather than just tracking accuracy. In vehicle detection, missing a bike means inaccurate traffic counts; in demographic applications, performance disparities can lead to wrongful arrests, denied loans, or biased medical care. As an engineer, you have legal compliance obligations and an ethical duty to mitigate disparities (e.g., rebalancing datasets, tuning thresholds per group, or rejecting deployment) before shipping the model to production.


## Which attack could corrupt this audit?

A data poisoning attack during the data collection or annotation lifecycle stage could silently corrupt the audit. An adversary with access to the test dataset could subtly shift bounding boxes or flip category labels on specific classes, making the model look fairer or artificially underperforming. A practical control from the lecture is cryptographic dataset hashing, version control (such as DVC), and data validation checks to ensure test set integrity cannot be modified without detection.


## Would SHAP or LIME explain a missed detection?

If an auditor asked why a specific Bicycle box was missed, SHAP and LIME would not work well. Both tools assume a fixed set of input features mapping to a fixed scalar output probability (like a classifier predicting P(y=class)). In object detection, the output is a variable list of boxes and coordinates across the image. When an object is completely missed (a false negative), there is no detection or score output to compute gradients or perturbations against. For our detector, the actual reason for the miss was that the bicycle's red pixel count fell below 20 or IoU didn't reach 0.3, which SHAP and LIME cannot surface.


## What did your attack show?

Looking at `fairness_report.json`:
- Flagged classes dropped progressively as eps increased:
  - Two-wheeler dropped from 78.6% (eps=0) to 71.4% (eps=10, 20), 42.9% (eps=30), and 21.4% (eps=40).
  - Bicycle dropped from 82.4% (eps=0) to 76.5% (eps=10), 52.9% (eps=20), 35.3% (eps=30), and 5.9% (eps=40).
  - Sedan dropped from 89.5% (eps=0) to 84.2% (eps=10), 73.7% (eps=20), 68.4% (eps=30), and 52.6% (eps=40).

At eps=20, the most fragile classes by recall drop were Bicycle (-29.4%), Tempo-traveller (-26.7%), and SUV (-22.2%). Bicycle was also flagged in the clean audit, but Tempo-traveller and SUV started at 100% recall.

The drop ranking and the lowest recall ranking do not completely agree:
- Drop ranking: Bicycle (-29.4%), Tempo-traveller (-26.7%), SUV (-22.2%).
- Lowest recall ranking: Bicycle (52.9%), Two-wheeler (71.4%), Tempo-traveller (73.3%).

Lowest recall is the better measure of real-world harm because it reflects actual missed vehicles on the road. Two-wheeler only dropped 7.1% simply because its clean baseline was already low (78.6%), but it remains one of the most dangerous to miss. Vulnerable groups that start with poor performance end up with the worst outcomes under attack.

For this detector, input validation would check pixel color distributions or check for abnormal global channel shifts (like lowered red and boosted green/blue) before inference. Adversarial training would involve adding color-perturbed images during development or lowering the detector's strict color thresholds. The hand-crafted rule breaks so easily because it relies on hard cutoffs (`r > 120`, `r - g > 40`), where a small shift pushes pixels across the threshold. A CNN is less brittle to a simple global color shift because it uses many learned texture features across multiple channels, though CNNs still have their own adversarial vulnerabilities.
