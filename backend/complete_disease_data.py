"""
Complete disease information for all 38 classes from New Plant Diseases Dataset
This data will be used to seed the database
"""

COMPLETE_DISEASE_INFO = {
    # ========== APPLE (4 classes) ==========
    "Apple___Apple_scab": {
        "name": "Apple Scab",
        "crop": "Apple",
        "description": "Apple scab is a fungal disease caused by Venturia inaequalis. It appears as olive-green to brown lesions on leaves and fruits, causing premature leaf drop and fruit deformation.",
        "symptoms": [
            "Olive-green to brown spots on leaves",
            "Velvety appearance on lesions",
            "Fruit scabs and deformation",
            "Premature leaf drop",
            "Reduced fruit quality"
        ],
        "treatment": "Apply fungicides (captan, myclobutanil) at bud break. Remove fallen leaves. Prune for better air circulation. Use resistant varieties.",
        "prevention": "Plant resistant varieties, ensure good air circulation, remove infected debris, apply preventive fungicides in spring."
    },
    
    "Apple___Black_rot": {
        "name": "Apple Black Rot",
        "crop": "Apple",
        "description": "Black rot is caused by the fungus Botryosphaeria obtusa. It affects leaves, fruits, and bark, causing significant economic losses.",
        "symptoms": [
            "Purple spots on leaves with red borders",
            "Black, circular lesions on fruits",
            "Fruit mummification",
            "Cankers on branches",
            "Premature fruit drop"
        ],
        "treatment": "Remove infected fruits and branches. Apply fungicides (captan, thiophanate-methyl). Prune dead wood. Improve orchard sanitation.",
        "prevention": "Prune regularly, remove mummified fruits, apply fungicides preventively, maintain tree vigor through proper nutrition."
    },
    
    "Apple___Cedar_apple_rust": {
        "name": "Cedar Apple Rust",
        "crop": "Apple",
        "description": "Cedar apple rust is caused by Gymnosporangium juniperi-virginianae. It requires both apple and cedar trees to complete its life cycle.",
        "symptoms": [
            "Bright orange-yellow spots on leaves",
            "Tube-like structures on leaf undersides",
            "Premature defoliation",
            "Reduced fruit quality",
            "Weakened tree vigor"
        ],
        "treatment": "Apply fungicides (myclobutanil, propiconazole) at pink bud stage. Remove nearby cedar trees if possible. Use resistant apple varieties.",
        "prevention": "Plant resistant varieties, remove cedar trees within 2 miles, apply preventive fungicides, ensure good air circulation."
    },
    
    "Apple___healthy": {
        "name": "Healthy Apple",
        "crop": "Apple",
        "description": "Healthy apple tree with no visible disease symptoms. Shows normal growth and fruit development.",
        "symptoms": [
            "Green, vibrant leaves",
            "No spots or lesions",
            "Normal fruit development",
            "Strong tree structure",
            "Good overall vigor"
        ],
        "treatment": "No treatment needed. Continue regular maintenance and monitoring.",
        "prevention": "Maintain good cultural practices, proper pruning, adequate nutrition, and regular pest monitoring."
    },
    
    # ========== BLUEBERRY (1 class) ==========
    "Blueberry___healthy": {
        "name": "Healthy Blueberry",
        "crop": "Blueberry",
        "description": "Healthy blueberry plant with no disease symptoms. Shows normal growth and berry production.",
        "symptoms": [
            "Healthy green foliage",
            "Normal berry development",
            "No leaf spots or discoloration",
            "Good plant vigor",
            "Strong branch structure"
        ],
        "treatment": "No treatment needed. Continue regular care.",
        "prevention": "Maintain proper soil pH (4.5-5.5), adequate watering, mulching, and regular monitoring."
    },
    
    # ========== CHERRY (2 classes) ==========
    "Cherry_(including_sour)___Powdery_mildew": {
        "name": "Cherry Powdery Mildew",
        "crop": "Cherry",
        "description": "Powdery mildew is caused by Podosphaera clandestina. It appears as white powdery growth on leaves and shoots.",
        "symptoms": [
            "White powdery coating on leaves",
            "Leaf curling and distortion",
            "Stunted shoot growth",
            "Premature leaf drop",
            "Reduced fruit quality"
        ],
        "treatment": "Apply sulfur or potassium bicarbonate fungicides. Prune infected shoots. Improve air circulation.",
        "prevention": "Plant resistant varieties, ensure good air circulation, avoid overhead watering, apply preventive fungicides."
    },
    
    "Cherry_(including_sour)___healthy": {
        "name": "Healthy Cherry",
        "crop": "Cherry",
        "description": "Healthy cherry tree with no disease symptoms. Normal growth and fruit production.",
        "symptoms": [
            "Healthy green leaves",
            "Normal fruit development",
            "No powdery growth",
            "Strong tree structure",
            "Good vigor"
        ],
        "treatment": "No treatment needed. Continue regular maintenance.",
        "prevention": "Proper pruning, adequate nutrition, good air circulation, and regular monitoring."
    },
    
    # ========== CORN/MAIZE (4 classes) ==========
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": {
        "name": "Corn Gray Leaf Spot",
        "crop": "Corn (Maize)",
        "description": "Gray leaf spot is caused by Cercospora zeae-maydis. It's a serious disease that can cause significant yield loss.",
        "symptoms": [
            "Rectangular gray-tan lesions",
            "Lesions parallel to leaf veins",
            "Severe leaf blight",
            "Premature plant death",
            "Reduced ear fill"
        ],
        "treatment": "Apply fungicides (azoxystrobin, pyraclostrobin) at early stages. Use resistant hybrids. Practice crop rotation.",
        "prevention": "Plant resistant hybrids, rotate crops, manage crop residue, ensure proper spacing."
    },
    
    "Corn_(maize)___Common_rust_": {
        "name": "Corn Common Rust",
        "crop": "Corn (Maize)",
        "description": "Common rust is caused by Puccinia sorghi. It produces characteristic rust-colored pustules on leaves.",
        "symptoms": [
            "Small circular to elongate brown pustules",
            "Pustules on both leaf surfaces",
            "Yellowing of leaves",
            "Reduced photosynthesis",
            "Premature leaf death"
        ],
        "treatment": "Apply fungicides if severe. Usually not economically damaging. Plant resistant hybrids.",
        "prevention": "Use resistant hybrids, ensure proper plant spacing, monitor weather conditions."
    },
    
    "Corn_(maize)___Northern_Leaf_Blight": {
        "name": "Northern Leaf Blight",
        "crop": "Corn (Maize)",
        "description": "Northern leaf blight is caused by Exserohilum turcicum. It produces long, elliptical lesions on leaves.",
        "symptoms": [
            "Long, elliptical gray-green lesions",
            "Lesions 1-6 inches long",
            "Severe leaf blighting",
            "Reduced grain fill",
            "Premature plant death"
        ],
        "treatment": "Apply fungicides (azoxystrobin, propiconazole). Use resistant hybrids. Practice crop rotation.",
        "prevention": "Plant resistant hybrids, rotate crops, manage residue, apply fungicides preventively."
    },
    
    "Corn_(maize)___healthy": {
        "name": "Healthy Corn",
        "crop": "Corn (Maize)",
        "description": "Healthy corn plant with no disease symptoms. Normal growth and ear development.",
        "symptoms": [
            "Dark green leaves",
            "Strong stalk",
            "Normal ear development",
            "No lesions or spots",
            "Good plant vigor"
        ],
        "treatment": "No treatment needed. Continue regular care.",
        "prevention": "Proper fertilization, adequate watering, pest management, and regular monitoring."
    },
    
    # ========== GRAPE (4 classes) ==========
    "Grape___Black_rot": {
        "name": "Grape Black Rot",
        "crop": "Grape",
        "description": "Black rot is caused by Guignardia bidwellii. It's one of the most destructive grape diseases.",
        "symptoms": [
            "Circular brown spots on leaves",
            "Black, shriveled berries (mummies)",
            "Fruit rot and drop",
            "Leaf lesions with black borders",
            "Severe yield loss"
        ],
        "treatment": "Apply fungicides (mancozeb, captan) from bud break. Remove mummified berries. Prune for air circulation.",
        "prevention": "Remove infected debris, apply preventive fungicides, ensure good air circulation, prune regularly."
    },
    
    "Grape___Esca_(Black_Measles)": {
        "name": "Grape Esca (Black Measles)",
        "crop": "Grape",
        "description": "Esca is a complex disease caused by multiple fungi. It affects the vascular system of grapevines.",
        "symptoms": [
            "Tiger-stripe pattern on leaves",
            "Interveinal chlorosis and necrosis",
            "Berry spotting and shriveling",
            "Sudden vine collapse (apoplexy)",
            "Wood discoloration"
        ],
        "treatment": "No effective chemical control. Remove severely infected vines. Prune carefully to avoid wounds.",
        "prevention": "Avoid pruning wounds, use proper pruning techniques, maintain vine vigor, remove infected wood."
    },
    
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": {
        "name": "Grape Leaf Blight",
        "crop": "Grape",
        "description": "Leaf blight is caused by Isariopsis clavispora (Pseudocercospora vitis). It causes leaf spots and defoliation.",
        "symptoms": [
            "Angular brown spots on leaves",
            "Spots with yellow halos",
            "Premature defoliation",
            "Reduced photosynthesis",
            "Weakened vines"
        ],
        "treatment": "Apply copper-based fungicides. Remove infected leaves. Improve air circulation.",
        "prevention": "Ensure good air circulation, remove debris, apply preventive fungicides, maintain vine vigor."
    },
    
    "Grape___healthy": {
        "name": "Healthy Grape",
        "crop": "Grape",
        "description": "Healthy grapevine with no disease symptoms. Normal growth and fruit production.",
        "symptoms": [
            "Green, healthy leaves",
            "Normal berry development",
            "No spots or discoloration",
            "Strong vine structure",
            "Good vigor"
        ],
        "treatment": "No treatment needed. Continue regular maintenance.",
        "prevention": "Proper pruning, adequate nutrition, good air circulation, regular monitoring."
    },
    
    # ========== ORANGE (1 class) ==========
    "Orange___Haunglongbing_(Citrus_greening)": {
        "name": "Citrus Greening (Huanglongbing)",
        "crop": "Orange",
        "description": "Huanglongbing (HLB) is caused by bacteria spread by Asian citrus psyllid. It's one of the most devastating citrus diseases.",
        "symptoms": [
            "Yellow shoots and blotchy mottling",
            "Lopsided, bitter fruits",
            "Premature fruit drop",
            "Twig dieback",
            "Tree decline and death"
        ],
        "treatment": "No cure available. Remove infected trees. Control psyllid vectors. Use certified disease-free nursery stock.",
        "prevention": "Control psyllid populations, use disease-free plants, remove infected trees promptly, apply systemic insecticides."
    },
    
    # ========== PEACH (2 classes) ==========
    "Peach___Bacterial_spot": {
        "name": "Peach Bacterial Spot",
        "crop": "Peach",
        "description": "Bacterial spot is caused by Xanthomonas arboricola pv. pruni. It affects leaves, fruits, and twigs.",
        "symptoms": [
            "Small, angular leaf spots",
            "Shot-hole appearance on leaves",
            "Fruit lesions and cracking",
            "Twig cankers",
            "Premature defoliation"
        ],
        "treatment": "Apply copper-based bactericides. Prune infected branches. Use resistant varieties.",
        "prevention": "Plant resistant varieties, apply preventive copper sprays, avoid overhead irrigation, prune for air circulation."
    },
    
    "Peach___healthy": {
        "name": "Healthy Peach",
        "crop": "Peach",
        "description": "Healthy peach tree with no disease symptoms. Normal growth and fruit production.",
        "symptoms": [
            "Healthy green leaves",
            "Normal fruit development",
            "No spots or lesions",
            "Strong tree structure",
            "Good vigor"
        ],
        "treatment": "No treatment needed. Continue regular maintenance.",
        "prevention": "Proper pruning, adequate nutrition, good air circulation, regular monitoring."
    },
    
    # ========== PEPPER (2 classes) ==========
    "Pepper,_bell___Bacterial_spot": {
        "name": "Pepper Bacterial Spot",
        "crop": "Bell Pepper",
        "description": "Bacterial spot is caused by Xanthomonas species. It affects leaves, stems, and fruits.",
        "symptoms": [
            "Small, dark brown leaf spots",
            "Raised lesions on fruits",
            "Premature defoliation",
            "Reduced fruit quality",
            "Yield loss"
        ],
        "treatment": "Apply copper-based bactericides. Remove infected plants. Use disease-free seeds.",
        "prevention": "Use certified disease-free seeds, rotate crops, avoid overhead watering, apply preventive copper sprays."
    },
    
    "Pepper,_bell___healthy": {
        "name": "Healthy Bell Pepper",
        "crop": "Bell Pepper",
        "description": "Healthy pepper plant with no disease symptoms. Normal growth and fruit production.",
        "symptoms": [
            "Green, healthy leaves",
            "Normal fruit development",
            "No spots or lesions",
            "Strong plant structure",
            "Good vigor"
        ],
        "treatment": "No treatment needed. Continue regular care.",
        "prevention": "Proper watering, adequate nutrition, crop rotation, regular monitoring."
    },
    
    # ========== POTATO (3 classes) ==========
    "Potato___Early_blight": {
        "name": "Potato Early Blight",
        "crop": "Potato",
        "description": "Early blight is caused by Alternaria solani. It affects foliage and tubers, reducing yield and quality.",
        "symptoms": [
            "Brown spots with target-like rings",
            "Yellowing of lower leaves",
            "Premature defoliation",
            "Dark lesions on tubers",
            "Reduced tuber size"
        ],
        "treatment": "Apply fungicides (chlorothalonil, mancozeb). Remove infected foliage. Ensure proper nutrition.",
        "prevention": "Use certified seed potatoes, rotate crops, maintain soil fertility, apply preventive fungicides."
    },
    
    "Potato___Late_blight": {
        "name": "Potato Late Blight",
        "crop": "Potato",
        "description": "Late blight is caused by Phytophthora infestans. It's the disease that caused the Irish potato famine.",
        "symptoms": [
            "Water-soaked lesions on leaves",
            "White mold on leaf undersides",
            "Blackened stems",
            "Brown rot in tubers",
            "Rapid plant collapse"
        ],
        "treatment": "Apply fungicides (mancozeb, chlorothalonil) preventively. Destroy infected plants. Harvest carefully.",
        "prevention": "Plant resistant varieties, avoid overhead irrigation, monitor weather, apply preventive fungicides, use certified seed."
    },
    
    "Potato___healthy": {
        "name": "Healthy Potato",
        "crop": "Potato",
        "description": "Healthy potato plant with no disease symptoms. Normal growth and tuber development.",
        "symptoms": [
            "Lush green foliage",
            "Strong plant structure",
            "No disease symptoms",
            "Good tuber formation",
            "Normal vigor"
        ],
        "treatment": "No treatment needed. Continue regular maintenance.",
        "prevention": "Proper watering, adequate nutrition, crop rotation, regular monitoring."
    },
    
    # ========== RASPBERRY (1 class) ==========
    "Raspberry___healthy": {
        "name": "Healthy Raspberry",
        "crop": "Raspberry",
        "description": "Healthy raspberry plant with no disease symptoms. Normal growth and berry production.",
        "symptoms": [
            "Healthy green canes",
            "Normal berry development",
            "No spots or lesions",
            "Good plant vigor",
            "Strong cane structure"
        ],
        "treatment": "No treatment needed. Continue regular care.",
        "prevention": "Proper pruning, adequate watering, mulching, regular monitoring."
    },
    
    # ========== SOYBEAN (1 class) ==========
    "Soybean___healthy": {
        "name": "Healthy Soybean",
        "crop": "Soybean",
        "description": "Healthy soybean plant with no disease symptoms. Normal growth and pod development.",
        "symptoms": [
            "Green, healthy leaves",
            "Normal pod development",
            "No spots or discoloration",
            "Good plant vigor",
            "Strong stem structure"
        ],
        "treatment": "No treatment needed. Continue regular care.",
        "prevention": "Crop rotation, proper spacing, adequate nutrition, regular monitoring."
    },
    
    # ========== SQUASH (1 class) ==========
    "Squash___Powdery_mildew": {
        "name": "Squash Powdery Mildew",
        "crop": "Squash",
        "description": "Powdery mildew is caused by Podosphaera xanthii. It appears as white powdery growth on leaves.",
        "symptoms": [
            "White powdery coating on leaves",
            "Leaf yellowing and wilting",
            "Reduced photosynthesis",
            "Premature leaf death",
            "Reduced fruit quality"
        ],
        "treatment": "Apply sulfur or potassium bicarbonate fungicides. Remove heavily infected leaves. Improve air circulation.",
        "prevention": "Plant resistant varieties, ensure good air circulation, avoid overhead watering, apply preventive fungicides."
    },
    
    # ========== STRAWBERRY (2 classes) ==========
    "Strawberry___Leaf_scorch": {
        "name": "Strawberry Leaf Scorch",
        "crop": "Strawberry",
        "description": "Leaf scorch is caused by Diplocarpon earlianum. It causes purple to brown spots on leaves.",
        "symptoms": [
            "Purple to brown spots on leaves",
            "Spots with purple borders",
            "Leaf scorching and drying",
            "Reduced plant vigor",
            "Lower fruit yield"
        ],
        "treatment": "Apply fungicides (captan, myclobutanil). Remove infected leaves. Improve air circulation.",
        "prevention": "Use resistant varieties, ensure good air circulation, remove debris, apply preventive fungicides."
    },
    
    "Strawberry___healthy": {
        "name": "Healthy Strawberry",
        "crop": "Strawberry",
        "description": "Healthy strawberry plant with no disease symptoms. Normal growth and fruit production.",
        "symptoms": [
            "Green, healthy leaves",
            "Normal fruit development",
            "No spots or lesions",
            "Good plant vigor",
            "Strong runner production"
        ],
        "treatment": "No treatment needed. Continue regular care.",
        "prevention": "Proper watering, adequate nutrition, mulching, regular monitoring."
    },
    
    # ========== TOMATO (10 classes) ==========
    "Tomato___Bacterial_spot": {
        "name": "Tomato Bacterial Spot",
        "crop": "Tomato",
        "description": "Bacterial spot is caused by Xanthomonas species. It affects leaves, stems, and fruits.",
        "symptoms": [
            "Small, dark brown leaf spots",
            "Raised lesions on fruits",
            "Premature defoliation",
            "Reduced fruit quality",
            "Yield loss"
        ],
        "treatment": "Apply copper-based bactericides. Remove infected plants. Use disease-free seeds.",
        "prevention": "Use certified seeds, rotate crops, avoid overhead watering, apply preventive copper sprays."
    },
    
    "Tomato___Early_blight": {
        "name": "Tomato Early Blight",
        "crop": "Tomato",
        "description": "Early blight is caused by Alternaria solani. It causes characteristic target-spot lesions on leaves.",
        "symptoms": [
            "Dark brown spots with concentric rings",
            "Yellowing around spots",
            "Premature defoliation",
            "Stem lesions",
            "Fruit spots"
        ],
        "treatment": "Apply fungicides (chlorothalonil, mancozeb). Remove infected leaves. Improve air circulation.",
        "prevention": "Use resistant varieties, rotate crops, mulch, avoid overhead watering, apply preventive fungicides."
    },
    
    "Tomato___Late_blight": {
        "name": "Tomato Late Blight",
        "crop": "Tomato",
        "description": "Late blight is caused by Phytophthora infestans. It can destroy entire crops rapidly.",
        "symptoms": [
            "Water-soaked spots on leaves",
            "White fuzzy growth on undersides",
            "Brown lesions on stems",
            "Firm brown spots on fruits",
            "Rapid plant collapse"
        ],
        "treatment": "Apply fungicides (mancozeb, chlorothalonil) preventively. Remove infected plants immediately.",
        "prevention": "Plant resistant varieties, ensure drainage, avoid overhead irrigation, monitor weather, apply preventive fungicides."
    },
    
    "Tomato___Leaf_Mold": {
        "name": "Tomato Leaf Mold",
        "crop": "Tomato",
        "description": "Leaf mold is caused by Passalora fulva (Cladosporium fulvum). It thrives in high humidity.",
        "symptoms": [
            "Pale green to yellow spots on upper leaf surface",
            "Olive-green to brown fuzzy growth on undersides",
            "Leaf curling and wilting",
            "Premature defoliation",
            "Reduced yield"
        ],
        "treatment": "Improve ventilation. Apply fungicides (chlorothalonil, mancozeb). Remove infected leaves.",
        "prevention": "Ensure good air circulation, reduce humidity, use resistant varieties, avoid overhead watering."
    },
    
    "Tomato___Septoria_leaf_spot": {
        "name": "Tomato Septoria Leaf Spot",
        "crop": "Tomato",
        "description": "Septoria leaf spot is caused by Septoria lycopersici. It causes numerous small spots on leaves.",
        "symptoms": [
            "Numerous small circular spots",
            "Gray centers with dark borders",
            "Black specks in spot centers",
            "Premature defoliation",
            "Reduced fruit quality"
        ],
        "treatment": "Apply fungicides (chlorothalonil, mancozeb). Remove infected leaves. Improve air circulation.",
        "prevention": "Rotate crops, mulch, avoid overhead watering, remove debris, apply preventive fungicides."
    },
    
    "Tomato___Spider_mites Two-spotted_spider_mite": {
        "name": "Tomato Spider Mites",
        "crop": "Tomato",
        "description": "Two-spotted spider mites (Tetranychus urticae) are tiny pests that suck plant sap, causing stippling and webbing.",
        "symptoms": [
            "Yellow stippling on leaves",
            "Fine webbing on plants",
            "Leaf bronzing and drying",
            "Reduced plant vigor",
            "Premature leaf drop"
        ],
        "treatment": "Apply miticides or insecticidal soap. Spray with water to dislodge mites. Use predatory mites.",
        "prevention": "Maintain adequate moisture, avoid water stress, use resistant varieties, encourage beneficial insects."
    },
    
    "Tomato___Target_Spot": {
        "name": "Tomato Target Spot",
        "crop": "Tomato",
        "description": "Target spot is caused by Corynespora cassiicola. It produces concentric ring patterns on leaves.",
        "symptoms": [
            "Brown spots with concentric rings",
            "Target-like lesions",
            "Premature defoliation",
            "Fruit lesions",
            "Reduced yield"
        ],
        "treatment": "Apply fungicides (chlorothalonil, azoxystrobin). Remove infected leaves. Improve air circulation.",
        "prevention": "Use resistant varieties, rotate crops, ensure good drainage, apply preventive fungicides."
    },
    
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
        "name": "Tomato Yellow Leaf Curl Virus",
        "crop": "Tomato",
        "description": "TYLCV is transmitted by whiteflies. It causes severe stunting and yield loss.",
        "symptoms": [
            "Upward leaf curling",
            "Yellowing of leaf margins",
            "Severe stunting",
            "Reduced fruit set",
            "Small, deformed fruits"
        ],
        "treatment": "No cure. Remove infected plants. Control whitefly vectors. Use resistant varieties.",
        "prevention": "Use resistant varieties, control whiteflies, use reflective mulches, remove infected plants promptly."
    },
    
    "Tomato___Tomato_mosaic_virus": {
        "name": "Tomato Mosaic Virus",
        "crop": "Tomato",
        "description": "Tomato mosaic virus (ToMV) causes mottling and distortion of leaves. It's highly contagious.",
        "symptoms": [
            "Mottled light and dark green on leaves",
            "Leaf distortion and curling",
            "Stunted growth",
            "Reduced fruit quality",
            "Internal fruit browning"
        ],
        "treatment": "No cure. Remove infected plants. Disinfect tools. Use virus-free seeds.",
        "prevention": "Use resistant varieties, practice good sanitation, disinfect tools, avoid tobacco use near plants."
    },
    
    "Tomato___healthy": {
        "name": "Healthy Tomato",
        "crop": "Tomato",
        "description": "Healthy tomato plant with no disease symptoms. Normal growth and fruit production.",
        "symptoms": [
            "Green, vibrant leaves",
            "Strong stem growth",
            "No spots or discoloration",
            "Normal fruit development",
            "Good plant vigor"
        ],
        "treatment": "No treatment needed. Continue regular care and monitoring.",
        "prevention": "Maintain good cultural practices, proper watering, fertilization, and pest management."
    }
}
