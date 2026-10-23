# NOTES.md — Week 11: Model Compression Benchmark

**Student ID used with `generate_for_student.py`:**
142301040


## pruned_dense_fp32 vs. pruned_sparse_coo

Both models have the exact same weights and accuracy (98.67%), but `pruned_dense_fp32` is 1024 bytes (1.0x baseline size) while `pruned_sparse_coo` is 616 bytes (1.66x compression).

This shows the lecture's pruning pitfall: setting weights to zero in a regular dense array saves no space because each zero still takes up 4 bytes. To actually shrink the model, you have to use a sparse format like COO that stores only non-zero weights. But sparse storage has an overhead: each surviving weight pays for both its value (4 bytes) and its index (4 bytes), so 8 bytes total per non-zero weight. At 70% sparsity, 77 non-zero weights remain, which gives 77 * 8 = 616 bytes. Pruning only saves space when sparsity is high enough (over 50%) to make up for storing indices.


## The 0.95-sparsity experiment

When setting PRUNE_SPARSITY to 0.95, accuracy drops from 98.67% down to 79.00%.

This happens because 95% sparsity zeroes out 243 of the 256 weights (leaving only 13 non-zero weights). Out of 256 weights, 216 are noise and 40 are informative. At 70% sparsity, zeroing 179 weights only pruned noise, leaving all 40 informative weights untouched. But at 95% sparsity, after zeroing all 216 noise weights, 27 informative weights also get zeroed out. Losing over half of the informative weights destroys the model's ability to classify properly, causing accuracy to drop off a cliff.
