import pandas as pd
import numpy as np


def get_disease_p(data_disease):
    diseases = data_disease['Болезнь']
    patients_count = data_disease['Количество пациентов']
    summary_patients_count = patients_count[len(patients_count) - 1]
    p_diseases = []
    for i in range(0, len(diseases)):
        p_diseases.append(patients_count[i] / summary_patients_count)
    print("Вероятности болезней ", p_diseases)
    return p_diseases


def get_p(disease, symptom, our_symptoms, disease_p):
    our_p = [1] * (len(disease) - 1)
    print("our p-s before = ", our_p)
    for i in range(len(disease) - 1):
        our_p[i] *= disease_p[i]
        for j in range(len(symptom) - 1):
            if our_symptoms[j] == 1:
                val = symptom.iloc[j][i + 1].replace(',', '.')
                our_p[i] *= float(val)
    print("our p-s after = ", our_p)
    return our_p


def get_max_idx(array):
    max_idx = 0
    max_v = array[max_idx]
    for i in range(0, len(array)):
        if max_v < array[i]:
            max_v = array[i]
            max_idx = i
    print("max idx = ", max_idx)
    return max_idx


def bayes(data_disease, data_symptom, our_symptoms):
    disease_val = data_disease['Болезнь']
    disease_p = get_disease_p(data_disease)
    our_p = get_p(disease_val, data_symptom, our_symptoms, disease_p)
    return disease_val[get_max_idx(our_p)]


data_symptom = pd.read_csv('../data/symptom.csv', delimiter=';')
data_disease = pd.read_csv('../data/disease.csv', delimiter=';')

our_symptoms = [np.random.randint(0, 2) for i in range(len(data_symptom) - 1)]
print("Тестовые симптомы ", our_symptoms)
final_disease = bayes(data_disease, data_symptom, our_symptoms)
print("Диагноз ", final_disease)
