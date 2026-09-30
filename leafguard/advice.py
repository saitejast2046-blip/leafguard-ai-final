"""Treatment advice in English, Telugu and Hindi."""
NAMES = {
    "healthy": {"en": "Healthy leaf", "te": "ఆరోగ్యంగా ఉంది", "hi": "स्वस्थ पत्ती"},
    "blight": {"en": "Late Blight", "te": "లేట్ బ్లైట్ (ఆలస్య తెగులు)", "hi": "लेट ब्लाइट"},
    "rust": {"en": "Rust / yellowing", "te": "తుప్పు తెగులు / పసుపు మచ్చలు", "hi": "रस्ट / पीले धब्बे"},
}
ADVICE = {
    "healthy": {
        "en": "Leaf looks healthy. Keep monitoring weekly and maintain balanced watering.",
        "te": "ఆకు ఆరోగ్యంగా ఉంది. వారానికి ఒకసారి పరిశీలించండి, సమతుల్యంగా నీరు పెట్టండి.",
        "hi": "पत्ती स्वस्थ दिख रही है। हर हफ्ते निगरानी करें और संतुलित सिंचाई रखें।",
    },
    "blight": {
        "en": "Remove and destroy infected leaves. Avoid overhead watering. Spray a copper-based fungicide as per the label and consult your local agriculture officer.",
        "te": "సోకిన ఆకులను తొలగించి నాశనం చేయండి. పై నుండి నీరు పోయకండి. లేబుల్ ప్రకారం కాపర్ ఆధారిత శిలీంద్ర నాశనిని పిచికారీ చేయండి; స్థానిక వ్యవసాయ అధికారిని సంప్రదించండి.",
        "hi": "संक्रमित पत्तियाँ हटाकर नष्ट करें। ऊपर से सिंचाई न करें। लेबल के अनुसार कॉपर-आधारित फफूंदनाशक का छिड़काव करें और स्थानीय कृषि अधिकारी से सलाह लें।",
    },
    "rust": {
        "en": "Remove affected leaves, improve air flow between plants and apply a suitable fungicide. Check nutrient levels (nitrogen, iron).",
        "te": "ప్రభావిత ఆకులను తొలగించండి, మొక్కల మధ్య గాలి ప్రసరణ పెంచండి, తగిన శిలీంద్ర నాశనిని వాడండి. నత్రజని, ఇనుము పోషకాల స్థాయిని పరిశీలించండి.",
        "hi": "प्रभावित पत्तियाँ हटाएँ, पौधों के बीच हवा का प्रवाह बढ़ाएँ और उपयुक्त फफूंदनाशक लगाएँ। नाइट्रोजन और आयरन की जाँच करें।",
    },
}
LANGS = ("en", "te", "hi")


def get_advice(label, lang="en"):
    """Return (disease name, advice) for a label in the requested language."""
    if label not in ADVICE:
        raise KeyError(f"unknown label: {label}")
    if lang not in LANGS:
        raise ValueError(f"unsupported language: {lang}")
    return NAMES[label][lang], ADVICE[label][lang]
