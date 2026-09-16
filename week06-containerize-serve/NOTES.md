# NOTES.md — Week 6: Containerize and Serve a Detector

**Student ID used with `generate_for_student.py`:**
142301040


## Built image size

168MB


## Swapping in a real checkpoint

I would separate the PyTorch installation and the model weights from the application code layer. PyTorch with CUDA is several gigabytes, so if it's installed in the same step or if weights are copied directly into the image, every small code change in `src/` would force Docker to rebuild and re-download gigabytes of dependencies. Using a prebuilt PyTorch base image (or caching torch in an early layer) and mounting the model weights from external storage at runtime keeps the build fast and prevents the image size from blowing up.
