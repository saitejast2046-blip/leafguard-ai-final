"""Leaf-first analysis: find the leaf, then measure uneven (non-green) spots on the leaf only."""
import numpy as np
from scipy import ndimage as ndi


def rgb_to_hsv(img):
    """Convert a uint8 HxWx3 RGB image to (hue 0-360, saturation 0-1, value 0-1) arrays."""
    x = img.astype(np.float32) / 255.0
    r, g, b = x[..., 0], x[..., 1], x[..., 2]
    mx, mn = x.max(-1), x.min(-1)
    d = mx - mn
    h = np.zeros_like(mx)
    nz = d > 0
    is_r = nz & (mx == r)
    is_g = nz & (mx == g) & ~is_r
    is_b = nz & ~is_r & ~is_g
    h[is_r] = ((g - b)[is_r] / d[is_r]) % 6
    h[is_g] = (b - r)[is_g] / d[is_g] + 2
    h[is_b] = (r - g)[is_b] / d[is_b] + 4
    h *= 60.0
    s = np.where(mx > 0, d / np.where(mx > 0, mx, 1), 0)
    return h, s, mx


def find_leaf_mask(hsv, close_radius=8):
    """Largest green object, closed and hole-filled so spots inside the leaf stay part of it."""
    h, s, v = hsv
    seed = (h >= 70) & (h <= 165) & (s > 0.25) & (v > 0.2)
    labels, count = ndi.label(seed)
    if count == 0:
        return np.zeros_like(seed)
    sizes = ndi.sum(seed, labels, index=range(1, count + 1))
    leaf = labels == (int(np.argmax(sizes)) + 1)
    leaf = ndi.binary_dilation(leaf, iterations=close_radius)
    leaf = ndi.binary_erosion(leaf, iterations=close_radius, border_value=1)
    return ndi.binary_fill_holes(leaf)


def find_spots(hsv, leaf_mask, edge_margin=4):
    """Non-green pixels inside the leaf (edge ignored, tiny specks removed)."""
    h, s, v = hsv
    core = ndi.binary_erosion(leaf_mask, iterations=edge_margin, border_value=1)
    healthy = (h >= 60) & (h <= 170) & (s > 0.12) & (v > 0.15)
    raw = core & ~healthy
    kernel = np.ones((3, 3), dtype=int)
    kernel[1, 1] = 0
    neighbours = ndi.convolve(raw.astype(int), kernel, mode="constant")
    return raw & (neighbours >= 3), core


def severity_label(pct, label):
    if label == "healthy":
        return "None"
    return "Low" if pct < 10 else "Moderate" if pct < 25 else "High"


def analyze_leaf(img, min_leaf_fraction=0.02):
    """Analyse an RGB uint8 image. Returns a dict with coverage, label and masks."""
    hsv = rgb_to_hsv(np.asarray(img, dtype=np.uint8))
    leaf = find_leaf_mask(hsv)
    if leaf.mean() < min_leaf_fraction:
        return {"noleaf": True, "coverage_pct": 0.0, "label": None, "severity": None,
                "leaf_mask": leaf, "spot_mask": np.zeros_like(leaf)}
    spots, core = find_spots(hsv, leaf)
    n_leaf, n_spot = int(core.sum()), int(spots.sum())
    pct = 100.0 * n_spot / n_leaf if n_leaf else 0.0
    dark = int((spots & (hsv[2] < 0.55)).sum())
    light = n_spot - dark
    # Rule-based stand-in until the trained MobileNetV3 classifier replaces it (see train.py)
    label = "healthy" if pct < 2 else ("blight" if dark >= light else "rust")
    return {"noleaf": False, "coverage_pct": pct, "label": label,
            "severity": severity_label(pct, label), "leaf_mask": leaf, "spot_mask": spots}
