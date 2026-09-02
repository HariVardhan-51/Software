"""
generate_sample_data.py

This script generates synthetic healthcare data.

Files generated:
    1. patients.csv
    2. providers.csv
    3. appointments.csv
    4. payments.csv

Files are saved inside:
    data/raw/
"""

import random
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
from faker import Faker


# ============================================================
# CONFIGURATION
# ============================================================

# Project root directory
BASE_DIR = Path(__file__).resolve().parent

# Raw data directory
OUTPUT_DIR = BASE_DIR / "data" / "raw"

# Create Faker object
fake = Faker("en_IN")

# Make the generated data reproducible
random.seed(42)
Faker.seed(42)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def random_date(start_date, end_date):
    """
    Generate a random date between start_date and end_date.
    """

    difference = end_date - start_date

    random_days = random.randint(0, difference.days)

    return start_date + timedelta(days=random_days)


# ============================================================
# GENERATE PATIENTS
# ============================================================

def generate_patients(number_of_patients):
    """
    Generate patient records.
    """

    patients = []

    insurance_providers = [
        "HealthCare Plus",
        "MediAssist",
        "Star Health",
        "Care Insurance",
        "Apollo Insurance",
        "Self Pay"
    ]

    genders = [
        "Male",
        "Female",
        "Other"
    ]

    patient_statuses = [
        "Active",
        "Active",
        "Active",
        "Inactive"
    ]

    for i in range(1, number_of_patients + 1):

        patient_id = f"P{i:05d}"

        date_of_birth = random_date(
            datetime(1940, 1, 1).date(),
            datetime(2010, 12, 31).date()
        )

        registration_date = random_date(
            datetime(2024, 1, 1).date(),
            datetime(2026, 8, 31).date()
        )

        insurance_provider = random.choice(
            insurance_providers
        )

        # Self-pay patients don't have an insurance ID
        if insurance_provider == "Self Pay":
            insurance_id = ""
        else:
            insurance_id = f"INS{i:05d}"

        patient = {
            "patient_id": patient_id,
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "date_of_birth": date_of_birth.isoformat(),
            "gender": random.choice(genders),
            "phone": fake.numerify("9#########"),
            "email": fake.email(),
            "city": fake.city(),
            "state": fake.state(),
            "registration_date": registration_date.isoformat(),
            "insurance_provider": insurance_provider,
            "insurance_id": insurance_id,
            "patient_status": random.choice(patient_statuses)
        }

        patients.append(patient)

    return pd.DataFrame(patients)


# ============================================================
# GENERATE PROVIDERS
# ============================================================

def generate_providers(number_of_providers):
    """
    Generate healthcare provider records.
    """

    providers = []

    specialties = [
        ("Cardiology", "Cardiology"),
        ("Neurology", "Neurology"),
        ("Orthopedics", "Orthopedics"),
        ("Dermatology", "Dermatology"),
        ("Pediatrics", "Pediatrics"),
        ("General Medicine", "General Medicine"),
        ("Gynecology", "Gynecology"),
        ("ENT", "ENT"),
        ("Ophthalmology", "Ophthalmology"),
        ("Gastroenterology", "Gastroenterology")
    ]

    provider_statuses = [
        "Active",
        "Active",
        "Active",
        "Inactive"
    ]

    hospitals = [
        "City Care Hospital",
        "Apollo Medical Center",
        "Sunrise Hospital",
        "Metro Health Hospital",
        "Green Valley Hospital"
    ]

    for i in range(1, number_of_providers + 1):

        provider_id = f"PR{i:05d}"

        specialization, department = random.choice(
            specialties
        )

        provider = {
            "provider_id": provider_id,
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "specialization": specialization,
            "department": department,
            "license_number": f"LIC{i:05d}",
            "phone": fake.numerify("9#########"),
            "email": fake.email(),
            "hospital_name": random.choice(hospitals),
            "city": fake.city(),
            "state": fake.state(),
            "years_of_experience": random.randint(1, 30),
            "provider_status": random.choice(provider_statuses)
        }

        providers.append(provider)

    return pd.DataFrame(providers)


# ============================================================
# GENERATE APPOINTMENTS
# ============================================================

def generate_appointments(
    number_of_appointments,
    patients_df,
    providers_df
):
    """
    Generate appointment records.

    patient_id comes from patients.csv.
    provider_id comes from providers.csv.
    """

    appointments = []

    patient_ids = patients_df["patient_id"].tolist()

    provider_ids = providers_df["provider_id"].tolist()

    appointment_types = [
        "Consultation",
        "Follow-up",
        "Routine Checkup",
        "Emergency",
        "Diagnostic"
    ]

    appointment_statuses = [
        "Completed",
        "Completed",
        "Completed",
        "Scheduled",
        "Cancelled",
        "No Show"
    ]

    reasons = [
        "Routine checkup",
        "Chest pain",
        "Fever",
        "Headache",
        "Back pain",
        "Skin problem",
        "Stomach pain",
        "Follow-up visit",
        "Blood pressure check",
        "Diabetes consultation"
    ]

    diagnoses = [
        "Hypertension",
        "Diabetes",
        "Viral infection",
        "Migraine",
        "Back pain",
        "Dermatitis",
        "Gastritis",
        "Routine examination",
        "No diagnosis"
    ]

    notes = [
        "Follow-up required",
        "Medication prescribed",
        "Patient advised to rest",
        "Routine monitoring recommended",
        "No further action required"
    ]

    for i in range(1, number_of_appointments + 1):

        appointment_id = f"A{i:06d}"

        appointment_date = random_date(
            datetime(2025, 1, 1).date(),
            datetime(2026, 8, 31).date()
        )

        # Generate appointment time
        hour = random.randint(9, 17)

        minute = random.choice([
            0,
            15,
            30,
            45
        ])

        appointment_status = random.choice(
            appointment_statuses
        )

        # Diagnosis only for completed appointments
        if appointment_status == "Completed":
            diagnosis = random.choice(diagnoses)
            appointment_notes = random.choice(notes)
        else:
            diagnosis = ""
            appointment_notes = ""

        appointment = {
            "appointment_id": appointment_id,

            # Foreign key to patients.csv
            "patient_id": random.choice(patient_ids),

            # Foreign key to providers.csv
            "provider_id": random.choice(provider_ids),

            "appointment_date": appointment_date.isoformat(),

            "appointment_time": (
                f"{hour:02d}:{minute:02d}:00"
            ),

            "appointment_type": random.choice(
                appointment_types
            ),

            "appointment_status": appointment_status,

            "reason": random.choice(reasons),

            "diagnosis": diagnosis,

            "notes": appointment_notes,

            "created_at": (
                appointment_date - timedelta(
                    days=random.randint(1, 30)
                )
            ).strftime("%Y-%m-%d %H:%M:%S")
        }

        appointments.append(appointment)

    return pd.DataFrame(appointments)


# ============================================================
# GENERATE PAYMENTS
# ============================================================

def generate_payments(
    appointments_df,
    patients_df
):
    """
    Generate payment records.

    Each payment is connected to an appointment
    and a patient.
    """

    payments = []

    # Create mapping:
    #
    # patient_id -> insurance_provider
    #
    patient_insurance = dict(
        zip(
            patients_df["patient_id"],
            patients_df["insurance_provider"]
        )
    )

    for i, appointment in enumerate(
        appointments_df.itertuples(index=False),
        start=1
    ):

        payment_id = f"PAY{i:06d}"

        transaction_id = f"TXN{i:08d}"

        # Generate appointment amount
        amount = round(
            random.uniform(500, 5000),
            2
        )

        patient_id = appointment.patient_id

        appointment_id = appointment.appointment_id

        appointment_status = appointment.appointment_status

        insurance_provider = patient_insurance[
            patient_id
        ]

        # ----------------------------------------------------
        # Cancelled / No Show
        # ----------------------------------------------------

        if appointment_status in [
            "Cancelled",
            "No Show"
        ]:

            payment_status = random.choice([
                "Pending",
                "Failed"
            ])

            insurance_amount = 0.00

            patient_amount = 0.00

            if insurance_provider == "Self Pay":
                payment_method = "UPI"
            else:
                payment_method = "Insurance"

        # ----------------------------------------------------
        # Completed / Scheduled
        # ----------------------------------------------------

        else:

            payment_status = random.choice([
                "Paid",
                "Paid",
                "Paid",
                "Pending"
            ])

            if insurance_provider != "Self Pay":

                insurance_amount = round(
                    amount * random.uniform(0.50, 0.90),
                    2
                )

                patient_amount = round(
                    amount - insurance_amount,
                    2
                )

                payment_method = "Insurance"

            else:

                insurance_amount = 0.00

                patient_amount = amount

                payment_method = random.choice([
                    "Credit Card",
                    "Debit Card",
                    "Cash",
                    "UPI"
                ])

        payment = {
            "payment_id": payment_id,

            # Foreign key to appointments.csv
            "appointment_id": appointment_id,

            # Foreign key to patients.csv
            "patient_id": patient_id,

            "payment_date": appointment.appointment_date,

            "amount": amount,

            "payment_method": payment_method,

            "insurance_amount": insurance_amount,

            "patient_amount": patient_amount,

            "payment_status": payment_status,

            "transaction_id": transaction_id,

            "currency": "INR"
        }

        payments.append(payment)

    return pd.DataFrame(payments)


# ============================================================
# MAIN FUNCTION
# ============================================================

def main():

    # Number of records to generate
    NUMBER_OF_PATIENTS = 1000

    NUMBER_OF_PROVIDERS = 100

    NUMBER_OF_APPOINTMENTS = 5000

    # Make sure data/raw directory exists
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    print("Starting sample data generation...")

    # --------------------------------------------------------
    # Generate Patients
    # --------------------------------------------------------

    print("Generating patients...")

    patients_df = generate_patients(
        NUMBER_OF_PATIENTS
    )

    # --------------------------------------------------------
    # Generate Providers
    # --------------------------------------------------------

    print("Generating providers...")

    providers_df = generate_providers(
        NUMBER_OF_PROVIDERS
    )

    # --------------------------------------------------------
    # Generate Appointments
    # --------------------------------------------------------

    print("Generating appointments...")

    appointments_df = generate_appointments(
        NUMBER_OF_APPOINTMENTS,
        patients_df,
        providers_df
    )

    # --------------------------------------------------------
    # Generate Payments
    # --------------------------------------------------------

    print("Generating payments...")

    payments_df = generate_payments(
        appointments_df,
        patients_df
    )

    # --------------------------------------------------------
    # Save CSV files
    # --------------------------------------------------------

    patients_df.to_csv(
        OUTPUT_DIR / "patients.csv",
        index=False
    )

    providers_df.to_csv(
        OUTPUT_DIR / "providers.csv",
        index=False
    )

    appointments_df.to_csv(
        OUTPUT_DIR / "appointments.csv",
        index=False
    )

    payments_df.to_csv(
        OUTPUT_DIR / "payments.csv",
        index=False
    )

    # --------------------------------------------------------
    # Display summary
    # --------------------------------------------------------

    print()
    print("=" * 50)
    print("Sample data generated successfully!")
    print("=" * 50)

    print(f"Output directory : {OUTPUT_DIR}")

    print(
        f"Patients         : {len(patients_df)} records"
    )

    print(
        f"Providers        : {len(providers_df)} records"
    )

    print(
        f"Appointments     : {len(appointments_df)} records"
    )

    print(
        f"Payments         : {len(payments_df)} records"
    )

    print("=" * 50)


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()