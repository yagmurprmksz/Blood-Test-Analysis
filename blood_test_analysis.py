import streamlit as st
import pdfplumber
st.markdown(
    """
    <h1 style="text-align: center; font-size: 50px; font-weight: bold; color: darkblue;">
        Blood Test Analysis🩸📊
    </h1>
    """,
    unsafe_allow_html=True
)
st.image(r"C:\Users\yagmu\PycharmProjects\pythonProject\testing-blood-1024x683.jpg", use_container_width=True)

# Custom CSS for better styling
st.markdown(
    """
    <style>
        .main-title {
            font-size: 32px;
            font-weight: bold;
            text-align: center;
            color: #4CAF50;
        }
        .sub-title {
            font-size: 24px;
            font-weight: bold;
            color: #2E86C1;
        }
        .upload-box {
            border: 2px dashed #4CAF50;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            background-color: #E8F5E9;
        }
        .result-box {
            margin-top: 10px;
            padding: 10px;
            border-radius: 5px;
        }
        .normal {
            background-color: #D4EDDA;
            color: #155724;
        }
        .low {
            background-color: #F8D7DA;
            color: #721C24;
        }
        .high {
            background-color: #FFF3CD;
            color: #856404;
        }
    </style>
    """,
    unsafe_allow_html=True
)
# Test information dictionary
test_info = {
    'WBC': {
        'info': ' White Blood Cells (WBC) fight infections and are part of the immune system.',
        'low_comment': 'May indicate viral infections, bone marrow issues, or autoimmune diseases.',
        'high_comment': 'May suggest infection, inflammation, or leukemia.',
        'diet': 'Consume foods rich in vitamin C and zinc like citrus fruits and nuts.',
        'clinic': 'Consult hematology or internal medicine.'
    },
    'RBC': {
        'info': 'Red Blood Cells (RBC) carry oxygen from your lungs to the rest of your body.',
        'low_comment': 'May indicate anemia, blood loss, or bone marrow disorders.',
        'high_comment': 'Could suggest dehydration, lung diseases, or heart problems.',
        'diet': 'Increase iron-rich foods such as spinach, red meat, and beans.',
        'clinic': 'Consult hematology or internal medicine.'
    },
    'HGB': {
        'info': 'Hemoglobin (HGB) is the protein in RBCs that carries oxygen.',
        'low_comment': 'May suggest anemia, iron deficiency, or blood loss.',
        'high_comment': 'May indicate dehydration or high altitude adaptation.',
        'diet': 'Eat iron-rich foods like liver, lentils, and fortified cereals.',
        'clinic': 'Consult hematology or internal medicine.'
    },
    'HCT': {
        'info': 'Hematocrit (HCT) measures the percentage of blood volume that is RBCs.',
        'low_comment': 'May indicate anemia, overhydration, or nutritional deficiencies.',
        'high_comment': 'May indicate dehydration, polycythemia vera, or lung disease.',
        'diet': 'Consume iron-rich foods like spinach, red meat, and eggs.',
        'clinic': 'Consult hematology or nephrology.'
    },
    'MCV': {
        'info': 'Mean Corpuscular Volume (MCV) measures the average size of RBCs.',
        'low_comment': 'May indicate microcytic anemia due to iron deficiency.',
        'high_comment': 'May suggest macrocytic anemia caused by vitamin B12 or folate deficiency.',
        'diet': 'Eat iron and folate-rich foods like leafy greens and citrus fruits.',
        'clinic': 'Consult hematology.'
    },
    'MCH': {
        'info': 'Mean Corpuscular Hemoglobin (MCH) measures the average amount of hemoglobin in RBCs.',
        'low_comment': 'May indicate hypochromic anemia, such as iron deficiency anemia.',
        'high_comment': 'May suggest macrocytic anemia due to vitamin B12 or folate deficiency.',
        'diet': 'Consume foods rich in iron and vitamins like red meat and leafy greens.',
        'clinic': 'Consult hematology.'
    },
    'MCHC': {
        'info': 'MCHC measures hemoglobin concentration in RBCs.',
        'low_comment': 'May indicate hypochromic anemia, often due to iron deficiency.',
        'high_comment': 'Could suggest spherocytosis or RBC disorders.',
        'diet': 'Increase iron-rich foods such as spinach and red meat.',
        'clinic': 'Consult hematology.'
    },
    'PLT': {
        'info': 'Platelets (PLT) help with blood clotting.',
        'low_comment': 'May indicate thrombocytopenia, infections, or medications.',
        'high_comment': 'May suggest thrombocytosis due to inflammation.',
        'diet': 'Consume foods high in folate and vitamin B12.',
        'clinic': 'Consult hematology.'
    },
    'RDW-CV': {
        'info': 'Red Cell Distribution Width (RDW-CV) measures variation in red blood cell size.',
        'low_comment': 'May indicate uniform red blood cell size.',
        'high_comment': 'May suggest a mix of red blood cell sizes, often seen in anemia.',
        'diet': 'Consume iron and folate-rich foods.',
        'clinic': 'Consult hematology.'
    },
    'RDW-SD': {
        'info': 'Red Cell Distribution Width - Standard Deviation (RDW-SD) measures variation in RBC sizes.',
        'low_comment': 'May indicate uniform RBC size.',
        'high_comment': 'May suggest anemia or blood disorders.',
        'diet': 'Consume foods rich in iron and folate.',
        'clinic': 'Consult hematology.'
    },
    'LY%': {
        'info': 'Lymphocyte Percentage (LY%) measures the proportion of lymphocytes in WBCs.',
        'low_comment': 'May suggest stress, infections, or immune deficiencies.',
        'high_comment': 'May indicate viral infections or chronic inflammation.',
        'diet': 'Eat foods rich in antioxidants and vitamins.',
        'clinic': 'Consult immunology or internal medicine.'
    },
    'NE%': {
        'info': 'Neutrophil Percentage (NE%) measures the proportion of neutrophils in WBCs.',
        'low_comment': 'May indicate bone marrow disorders or severe infections.',
        'high_comment': 'May suggest bacterial infections or inflammation.',
        'diet': 'Include zinc and vitamin C-rich foods.',
        'clinic': 'Consult hematology or internal medicine.'
    },
    'MO%': {
        'info': 'Monocyte Percentage (MO%) measures the proportion of monocytes in WBCs.',
        'low_comment': 'May suggest immune suppression or bone marrow disorders.',
        'high_comment': 'May indicate chronic infections or inflammation.',
        'diet': 'Include omega-3 rich foods and antioxidants.',
        'clinic': 'Consult hematology or internal medicine.'
    },
    'EO%': {
        'info': 'Eosinophil Percentage (EO%) measures the proportion of eosinophils in WBCs.',
        'low_comment': 'May indicate acute stress or infections.',
        'high_comment': 'May suggest allergies or parasitic infections.',
        'diet': 'Eat anti-inflammatory foods like turmeric and ginger.',
        'clinic': 'Consult allergy or immunology specialists.'
    },
    'BA%': {
        'info': 'Basophil Percentage (BA%) measures the proportion of basophils in WBCs.',
        'low_comment': 'May indicate low allergic or inflammatory activity.',
        'high_comment': 'May suggest allergies or chronic inflammation.',
        'diet': 'Focus on anti-inflammatory foods.',
        'clinic': 'Consult allergy or immunology specialists.'
    },
    'IG#': {
        'info': 'Immature Granulocytes Count (IG#) measures immature white blood cells.',
        'low_comment': 'May indicate bone marrow suppression or immune deficiencies.',
        'high_comment': 'May suggest infection, inflammation, or bone marrow disorders.',
        'diet': 'Consume foods rich in protein, vitamins, and antioxidants.',
        'clinic': 'Consult hematology.'
    },
    'IG%': {
        'info': 'Immature Granulocytes Percentage (IG%) measures percentage of immature WBCs.',
        'low_comment': 'May indicate low immune system activity.',
        'high_comment': 'May suggest infection, inflammation, or stress response.',
        'diet': 'Eat foods rich in antioxidants and vitamins.',
        'clinic': 'Consult hematology.'
    },
    'NRBC#': {
        'info': 'Nucleated Red Blood Cell Count (NRBC#) measures immature RBCs.',
        'low_comment': 'Usually absent in healthy individuals.',
        'high_comment': 'May indicate severe anemia, bone marrow stress, or hypoxia.',
        'diet': 'Focus on iron, folate, and vitamin B12-rich foods.',
        'clinic': 'Consult hematology.'
    },
    'NRBC%': {
        'info': 'Nucleated Red Blood Cell Percentage (NRBC%) measures proportion of immature RBCs.',
        'low_comment': 'Usually absent in healthy individuals.',
        'high_comment': 'May suggest anemia, hypoxia, or bone marrow disorders.',
        'diet': 'Increase iron-rich foods and vitamins.',
        'clinic': 'Consult hematology.'
        }
    }
reference_ranges = {
    'WBC': (4, 10),
    'RBC': (3.50, 5.50),
    'HGB': (11, 15),
    'HCT': (37, 47),
    'MCV': (80, 100),
    'MCH': (27, 34),
    'MCHC': (32, 36),
    'PLT': (100, 400),
    'RDW-CV': (11, 16),
    'RDW-SD': (35, 56),
    'LY%': (20, 40),
    'NE%': (50, 70),
    'MO%': (3, 12),
    'EO%': (0.5, 5),
    'BA%': (0, 1),
    'IG#': (0.01, 0.04),
    'IG%': (0.16, 0.62),
    'NRBC#': (0.000, 0.015),
    'NRBC%': (0.000, 0.030)
}
# Session state için tüm testleri varsayılan olarak başlat
for test_name in reference_ranges.keys():
    if f"show_{test_name}" not in st.session_state:
        st.session_state[f"show_{test_name}"] = False

uploaded_file = st.file_uploader("Upload your blood test PDF file", type=["pdf"])

if uploaded_file:
    blood_test_results = {}
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            for line in text.split("\n"):
                parts = line.split()
                if len(parts) > 2:
                    test_name = parts[1]
                    try:
                        test_value = float(parts[2])
                        blood_test_results[test_name] = test_value
                    except ValueError:
                        continue

    for test_name, value in blood_test_results.items():
        if test_name in reference_ranges:
            lower, upper = reference_ranges[test_name]
            if lower <= value <= upper:
                css_class = 'normal'
                status = '✅Normal'
            elif value < lower:
                css_class = 'low'
                status = '⬇️LOW'
            else:
                css_class = 'high'
                status = '⬆️ HIGH'

            st.markdown(f"<div class='result-box {css_class}'>{test_name}: {status} ({value})</div>",
                        unsafe_allow_html=True)
            if st.button(f"ℹ️ Details for {test_name}"):
                st.session_state[f"show_{test_name}"] = not st.session_state[f"show_{test_name}"]

            if st.session_state[f"show_{test_name}"]:
                info = test_info.get(test_name, {})
                st.info(f"**ℹ️ Info:** {info.get('info', 'No information available.')}")
                st.info(f"**⚠️ Low Value Comment:** {info.get('low_comment', 'No comment available.')}")
                st.info(f"**🔴 High Value Comment:** {info.get('high_comment', 'No comment available.')}")
                st.info(f"**🥗 Diet Suggestion:** {info.get('diet', 'No suggestions available.')}")
                st.info(f"**🏥 Clinic Suggestion:** {info.get('clinic', 'No clinic recommendation available.')}")
