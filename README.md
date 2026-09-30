# LeafGuard AI

Offline, phone-friendly crop leaf disease screening with advice in English, Telugu and Hindi.
Built for OptiForge'26 (AI & Machine Learning theme).

## Problem
Small farmers often spot leaf diseases too late, have limited access to experts, and may use the wrong pesticide.
LeafGuard AI checks a leaf photo, shows how much of the leaf is affected, and gives treatment advice in the farmer's language.

## How it works
1. **Find the leaf:** the largest green object is separated from the background (holes are filled so spots stay inside the leaf).
2. **Measure spots on the leaf only:** non-green regions inside the leaf are marked; the blurry leaf edge and tiny specks are ignored.
3. **Report:** affected-area percentage, severity, disease label and advice in English / Telugu / Hindi.
4. **Classifier:** `train.py` fine-tunes MobileNetV3 on PlantVillage and exports TensorFlow Lite for on-device use.
   Until that model is plugged in, the disease label comes from a rule-based stand-in (dark vs yellow/orange spots).

## Project layout
- `index.html` - live web demo (runs fully in the browser, no server, no internet needed for analysis)
- `leafguard/` - Python implementation of leaf and spot detection (`segmentation.py`) and multilingual advice (`advice.py`)
- `tests/` - unit tests
- `train.py` - MobileNetV3 training, evaluation and TFLite export

## Run
```bash
pip install -r requirements.txt
python -m unittest discover -s tests -v
```
Open `index.html` in a browser for the demo. To train: `pip install -r requirements-train.txt && python train.py` (GPU recommended).

## Results
Rule-based leaf and spot detection is covered by unit tests on synthetic leaves.
MobileNetV3 accuracy / F1 on the PlantVillage test split: _to be added after training (see `train.py` output)_.

## Limitations
- PlantVillage images are clean lab photos; accuracy on real field photos will be lower and needs field data (cotton, rice, chilli).
- Best results with one leaf on a plain background in good light.
- Decision support only; consult a local agriculture officer.

## Future work
Field data collection, pest detection, Telugu voice assistant, weather-based outbreak alerts.
