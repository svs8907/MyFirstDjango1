from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.shortcuts import redirect
from django.urls import reverse
import matplotlib.pyplot as plt
import csv
from django.shortcuts import render
from django.conf import settings
import pandas as pd
import os
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control

def home(request):
    return render(request, 'home.html', {'name': 'User'})

def add(request):
    val1 = str(request.POST['sym1'])
    val2 = str(request.POST['sym2'])
    val3 = str(request.POST['sym3'])
    predicted_disease, medications = predict_disease([val1, val2, val3])
    return render(request, 'result.html', {'result': predicted_disease, 'medications': medications})

def dashboard(request):
    return render(request, 'dashboard.html')

def features(request):
    return render(request, 'features.html')

# Create your views here.

diseases_db = {
    "Common Cold": {
        "symptoms": {"Runny nose", "Sore throat", "Cough"},
        "medications": ["Antihistamines", "Decongestants", "Acetaminophen"]
    },
    "Influenza (Flu)": {
        "symptoms": {"Fever", "Body aches", "Fatigue"},
        "medications": ["Antivirals (e.g., Oseltamivir)", "Ibuprofen", "Acetaminophen"]
    },
    "Hypertension": {
        "symptoms": {"Headache", "Dizziness", "Shortness of breath"},
        "medications": ["ACE inhibitors", "Beta-blockers", "Diuretics"]
    },
    "Diabetes Mellitus": {
        "symptoms": {"Increased thirst", "Frequent urination", "Fatigue"},
        "medications": ["Insulin", "Metformin", "Sulfonylureas"]
    },
    "Asthma": {
        "symptoms": {"Wheezing", "Shortness of breath", "Coughing"},
        "medications": ["Inhaled corticosteroids", "Bronchodilators", "Leukotriene modifiers"]
    },
    "COVID-19": {
        "symptoms": {"Fever", "Cough", "Loss of taste or smell"},
        "medications": ["Antivirals (e.g., Remdesivir)", "Steroids", "Oxygen therapy"]
    },
    "Tuberculosis (TB)": {
        "symptoms": {"Persistent cough", "Night sweats", "Weight loss"},
        "medications": ["Isoniazid", "Rifampin", "Ethambutol"]
    },
    "Malaria": {
        "symptoms": {"Fever", "Chills", "Headache"},
        "medications": ["Chloroquine", "Artemisinin-based combination therapy (ACT)"]
    },
    "Pneumonia": {
        "symptoms": {"Chest pain", "Cough with phlegm", "Shortness of breath"},
        "medications": ["Antibiotics (e.g., Amoxicillin)", "Antivirals", "Pain relievers"]
    },
    "HIV/AIDS": {
        "symptoms": {"Fever", "Fatigue", "Swollen lymph nodes"},
        "medications": ["Antiretroviral therapy (ART)", "Protease inhibitors", "NRTIs"]
    },
}

def predict_disease(symptoms):
    symptoms_set = set(symptoms)
    for disease, info in diseases_db.items():
        if symptoms_set.issubset(info["symptoms"]):
            return disease, info["medications"]
    return "No matching disease found", []

def find_disease(val1, val2, val3):
    predicted_disease, medications = predict_disease([val1, val2, val3])
    return predicted_disease, medications   

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse('home')) 
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')

def home_view(request):
    return render(request, 'home.html')

def rep_page(request):
    return render(request, 'rep.html')

def rep(request, disease):
    # Load the disease data from the CSV file
    data = pd.read_csv('graph1_data.csv')

    # Filter the data based on the selected disease
    filtered_data = data[data['Disease'] == predict_disease]

    # Group the data by year and calculate the sum of deaths
    deaths_per_year = filtered_data.groupby('Year')['Deaths'].sum()


def rep_view(request):
    disease_name = request.GET.get('disease')
    disease_data = None

    # Path to the CSV file
    csv_path = os.path.join(settings.BASE_DIR, 'disease.csv')

    # Read the CSV file
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Disease'] == disease_name:
                disease_data = row
                break

    context = {'disease': disease_name, 'disease_data': disease_data}
    return render(request, 'rep.html', context)


def result(request):
    return render(request,'result.html')

def find_hospitals(request):
    return render(request, 'find_hospitals.html')

def find_doctors(request):
    return render(request, 'find_doctors.html')

def best_countries(request):
    return render(request, 'best_countries.html')

def registerPage(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            messages.error(request, "Password does not meet the requirements. Please try again.")
    context = {'form': form}
    return render(request, 'register.html', context)

def registerPage(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            messages.error(request, "Password does not meet the requirements. Please try again.")
    context = {'form': form}
    return render(request, 'register.html', context)

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            phone_n=form.cleaned_data.get('phone_number')
            user = authenticate(username=username, password=raw_password,number=phone_n)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logoutPage(request):
    logout(request)
    return redirect('login')

def appointments(request):
    return render(request, 'appointments.html')

def result_view(request):
    # Example: Assuming you're getting a selected disease's name from a form in result.html
    disease = request.POST.get('disease')
    
    # Load your CSV data into a dictionary
    disease_data = {
        "COVID-19": {
            "mortality": [("2013", 10), ("2014", 12), ...],  # Replace with actual data
            "immunization": [("2013", 50), ("2014", 60), ...],
            "age_group": {"0-18": 10, "19-35": 30, "36-50": 25, "51+": 35}
        },
        # Add more diseases and their respective data...
    }

    # Pass the disease data to the template
    return render(request, 'rep.html', {
        'disease': disease,
        'mortality_data': disease_data[disease]['mortality'],
        'immunization_data': disease_data[disease]['immunization'],
        'age_group_data': disease_data[disease]['age_group'],
    })

def dashboard_view(request):
    user = request.user
    context = {
        'exercise_progress': 70,  # This could be dynamic
        'water_progress': 50,     # This could be dynamic
        'exercise_minutes': 30,   # Exercise minutes for the day
        'water_count': 2.5,       # Liters of water consumed
        'profile_picture_url': user.profile.picture.url,  # Assuming you have a profile picture
    }
    return render(request, 'dashboard.html', context)

def rep_view(request, disease_name):
    # Load your CSV data
    df = pd.read_csv('path/to/your/disease.csv')

    # Filter data for the selected disease
    disease_data = df[df['Disease'] == disease_name]

    # Convert the filtered data to a dictionary format
    data_dict = disease_data.to_dict('list')
    
    context = {
        'disease_name': disease_name,
        'data': data_dict
    }
    return render(request, 'rep.html', context)
