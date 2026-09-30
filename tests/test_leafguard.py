import unittest
import numpy as np
from leafguard import analyze_leaf, get_advice
from leafguard.advice import ADVICE, LANGS

BG, GREEN, BROWN, ORANGE = (242, 242, 242), (63, 163, 77), (59, 35, 19), (217, 120, 30)


def make_leaf(spots=(), colour=BROWN, outside=()):
    img = np.full((400, 400, 3), BG, dtype=np.uint8)
    yy, xx = np.ogrid[:400, :400]
    img[((xx - 200) / 110.0) ** 2 + ((yy - 200) / 165.0) ** 2 <= 1] = GREEN
    for cx, cy, r in spots:
        img[(xx - cx) ** 2 + (yy - cy) ** 2 <= r * r] = colour
    for cx, cy, r in outside:
        img[(xx - cx) ** 2 + (yy - cy) ** 2 <= r * r] = BROWN
    return img


class TestAnalysis(unittest.TestCase):
    def test_healthy_leaf(self):
        res = analyze_leaf(make_leaf())
        self.assertFalse(res["noleaf"])
        self.assertEqual(res["label"], "healthy")
        self.assertLess(res["coverage_pct"], 2)

    def test_dark_spots_detected_as_blight(self):
        res = analyze_leaf(make_leaf([(170, 150, 22), (230, 230, 26), (190, 260, 18)]))
        self.assertEqual(res["label"], "blight")
        self.assertGreater(res["coverage_pct"], 2)

    def test_orange_spots_detected_as_rust(self):
        res = analyze_leaf(make_leaf([(170, 150, 20), (230, 230, 22)], colour=ORANGE))
        self.assertEqual(res["label"], "rust")

    def test_no_leaf_in_plain_background(self):
        res = analyze_leaf(np.full((400, 400, 3), BG, dtype=np.uint8))
        self.assertTrue(res["noleaf"])

    def test_spots_outside_leaf_are_ignored(self):
        res = analyze_leaf(make_leaf(outside=[(40, 40, 25), (360, 360, 25)]))
        self.assertEqual(res["label"], "healthy")
        self.assertFalse(res["spot_mask"][40, 40])

    def test_more_spots_means_more_coverage(self):
        few = analyze_leaf(make_leaf([(200, 200, 15)]))["coverage_pct"]
        many = analyze_leaf(make_leaf([(200, 200, 15), (160, 130, 25), (240, 280, 25)]))["coverage_pct"]
        self.assertGreater(many, few)


class TestAdvice(unittest.TestCase):
    def test_all_languages_present(self):
        for label in ADVICE:
            for lang in LANGS:
                name, text = get_advice(label, lang)
                self.assertTrue(name and text)

    def test_bad_inputs_raise(self):
        with self.assertRaises(KeyError):
            get_advice("unknown")
        with self.assertRaises(ValueError):
            get_advice("blight", "xx")


if __name__ == "__main__":
    unittest.main()
