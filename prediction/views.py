import os
from django.conf import settings
from django.shortcuts import render, redirect
from .models import Prediction
import joblib
from PIL import Image
import numpy as np

# Load SVM model
model_path = os.path.join(settings.BASE_DIR, 'prediction', 'svm_model.pkl')
clf = joblib.load(model_path)


def predict_image(request):
    if request.method == 'POST':
        uploaded_image = request.FILES.get('image')
        if uploaded_image:
            # Save image to the database
            prediction = Prediction.objects.create(uploaded_image=uploaded_image)
            
            # Process the image
            img_path = prediction.uploaded_image.path
            img = Image.open(img_path).convert('L').resize((32, 32))
            img_array = np.array(img).flatten().reshape(1, -1)
            
            # Predict using the model
            result = clf.predict(img_array)
            
            # Map prediction to Malignant or Benign
            prediction.result = 'Malignant' if result[0] == 1 else 'Benign'
            prediction.save()
            
            # Redirect user to the result page
            return redirect('prediction:result', prediction_id=prediction.id)
    
    return render(request, 'predict.html')


def result(request, prediction_id):
    
    try:
        # Fetch the prediction instance from the database
        prediction = Prediction.objects.get(id=prediction_id)
        if prediction.result == 'Malignant':
            prediction_message = "Please consult with your doctor for further evaluation and treatment options."
        else:
            prediction_message = "No immediate concern, but recommended regular monitoring for any changes."
            
    except Prediction.DoesNotExist:
        return render(request, 'result.html', {'prediction': None, 'message': "No prediction found."})
        
    return render(request, 'result.html', {'prediction': prediction, 'message': prediction_message})

def dashboard(request):
    return render(request, 'dashboard.html')
