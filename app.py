import streamlit as st
import cv2
import numpy as np
from keras.models import load_model

# Set page configuration
st.set_page_config(
    page_title="Crops Prediction", 
    page_icon=":seedling:", 
    layout="centered",
)

# Load the model
clf = load_model("model_adamax_2_epoch_20.h5")

# Title of the application
st.title('Agriculture crops classification :seedling:')
st.write('Project objective: To build a predictive model to classify crops based on image.')
st.write('Problem Type: Multi-class Classification')
st.write('Algorithm used: Convolutional Neural Network')
st.write("Data Source: [Crop Detection Dataset Roboflow](https://www.google.com/url?q=https%3A%2F%2Funiverse.roboflow.com%2Fjeyajeev%2Fcrop-detection-etbjz)")
st.write('Model Accuracy: 81.91%')
st.write('View [code](https://github.com/hilalrp/crops_classification_CNN)')
st.write("This Project was created by [Hilal Rosyid Putra](https://www.linkedin.com/in/hilal-rosyid-putra-3b403a199/)")
st.write("")
st.write("")
st.write('---Scroll down to test the model---')
# File uploader
uploaded_file = st.file_uploader("Choose a crop image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Convert the file to an opencv image.
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Display the image
    st.image(img_rgb, channels="RGB", caption='Uploaded crop image.', use_column_width=True)

    # Preprocess the image for prediction
    img_resized = cv2.resize(img, (224, 224))
    img_resized = img_resized / 255.0
    img_resized = np.array(img_resized).reshape((1, 224, 224, 3))

    # Add a button to predict
    if st.button('Predict'):
        # Predict the image
        Y_prediction = clf.predict(img_resized)
        y_pred = np.argmax(Y_prediction[0])
        class_labels = ["Corn", "Cotton", "Rice", "Wheat"]
        output_val = "Prediction: {0} with {1:.2f}% confidence".format(class_labels[y_pred], Y_prediction[0, y_pred] * 100)

        # Display the prediction
        st.markdown(f"<div style='text-align: center; font-size: 24px; color: green;'>{output_val}</div>", unsafe_allow_html=True)
