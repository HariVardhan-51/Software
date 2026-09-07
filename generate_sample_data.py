"""
generate_sample_data.py

Generates synthetic healthcare data for the clinic database project.

Files generated:
    1. patients.csv
    2. providers.csv
    3. appointments.csv
    4. payments.csv

Files are saved to:
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

BASE_DIR = Path(__file__).resolve().parent

OUTPUT_DIR = BASE_DIR / "data" / "raw"

fake = Faker("en_IN")

# Make data reproducible
random.seed(42)
Faker.seed(42)


# ============================================================
# RECORD COUNTS
# ============================================================

NUMBER_OF_PATIENTS = 1000

NUMBER_OF_PROVIDERS = 100

NUMBER_OF_APPOINTMENTS = 5000


# ============================================================
# MASTER DATA
# ============================================================

INSURANCE_PAYERS = [
    {
        "code": "HCP",
        "name": "HealthCare Plus",
        "type": "Commercial"
    },
    {
        "code": "MED",
        "name": "MediAssist",
        "type": "Commercial"
    },
    {
        "code": "STAR",
        "name": "Star Health",
        "type": "Commercial"
    },
    {
        "code": "CARE",
        "name": "Care Insurance",
        "type": "Commercial"
    },
    {
        "code": "APOLLO",
        "name": "Apollo Insurance",
        "type": "Commercial"
    },
    {
        "code": "SELF",
        "name": "Self Pay",
        "type": "Self Pay"
    }
]


PROCEDURES = [
    {
        "code": "CONS001",
        "name": "General Consultation",
        "category": "Consultation",
        "duration": 30,
        "charge": 1000.00
    },
    {
        "code": "CARD001",
        "name": "Cardiology Consultation",
        "category": "Consultation",
        "duration": 45,
        "charge": 1800.00
    },
    {
        "code": "NEUR001",
        "name": "Neurology Consultation",
        "category": "Consultation",
        "duration": 45,
        "charge": 2000.00
    },
    {
        "code": "ORTH001",
        "name": "Orthopedic Consultation",
        "category": "Consultation",
        "duration": 45,
        "charge": 1600.00
    },
    {
        "code": "DERM001",
        "name": "Dermatology Consultation",
        "category": "Consultation",
        "duration": 30,
        "charge": 1200.00
    },
    {
        "code": "PED001",
        "name": "Pediatric Consultation",
        "category": "Consultation",
        "duration": 30,
        "charge": 1000.00
    },
    {
        "code": "FOLLOW001",
        "name": "Follow-up Visit",
        "category": "Follow-up",
        "duration": 20,
        "charge": 700.00
    },
    {
        "code": "CHECK001",
        "name": "Routine Health Checkup",
        "category": "Preventive",
        "duration": 60,
        "charge": 2500.00
    },
    {
        "code": "DIAG001",
        "name": "Diagnostic Consultation",
        "category": "Diagnostic",
        "duration": 45,
        "charge": 1500.00
    },
    {
        "code": "EMER001",
        "name": "Emergency Consultation",
        "category": "Emergency",
        "duration": 60,
        "charge": 3000.00
    }
]


SPECIALTIES = [
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


HOSPITALS = [
    {
        "code": "LOC001",
        "name": "City Care Hospital",
        "city": "Hyderabad",
        "state": "Telangana",
        "zip": "500001",
        "phone": "04040010001"
    },
    {
        "code": "LOC002",
        "name": "Apollo Medical Center",
        "city": "Bengaluru",
        "state": "Karnataka",
        "zip": "560001",
        "phone": "08040010002"
    },
    {
        "code": "LOC003",
        "name": "Sunrise Hospital",
        "city": "Chennai",
        "state": "Tamil Nadu",
        "zip": "600001",
        "phone": "04440010003"
    },
    {
        "code": "LOC004",
        "name": "Metro Health Hospital",
        "city": "Mumbai",
        "state": "Maharashtra",
        "zip": "400001",
        "phone": "02240010004"
    },
    {
        "code": "LOC005",
        "name": "Green Valley Hospital",
        "city": "Delhi",
        "state": "Delhi",
        "zip": "110001",
        "phone": "01140010005"
    }
]


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def random_date(start_date, end_date):
    """Generate a random date between two dates."""

    difference = end_date - start_date

    random_days = random.randint(
        0,
        difference.days
    )

    return start_date + timedelta(
        days=random_days
    )


def random_time():
    """Generate an appointment time."""

    hour = random.randint(9, 17)

    minute = random.choice(
        [0, 15, 30, 45]
    )

    return hour, minute


# ============================================================
# GENERATE PATIENTS
# ============================================================

def generate_patients(number_of_patients):

    patients = []

    for i in range(
        1,
        number_of_patients + 1
    ):

        patient_id = f"P{i:05d}"

        patient_number = f"PAT{i:06d}"

        date_of_birth = random_date(
            datetime(1940, 1, 1).date(),
            datetime(2010, 12, 31).date()
        )

        registration_date = random_date(
            datetime(2024, 1, 1).date(),
            datetime(2026, 8, 31).date()
        )

        payer = random.choice(
            INSURANCE_PAYERS
        )

        if payer["code"] == "SELF":

            insurance_id = ""

        else:

            insurance_id = f"INS{i:06d}"

        created_at = datetime.combine(
            registration_date,
            datetime.min.time()
        ) + timedelta(
            hours=random.randint(8, 17),
            minutes=random.randint(0, 59)
        )

        updated_at = created_at + timedelta(
            days=random.randint(0, 30)
        )

        patient = {

            "patient_id": patient_id,

            "patient_number": patient_number,

            "first_name": fake.first_name(),

            "last_name": fake.last_name(),

            "date_of_birth":
                date_of_birth.isoformat(),

            "gender": random.choice([
                "Male",
                "Female",
                "Other"
            ]),

            "phone":
                fake.numerify("9#########"),

            "email":
                fake.email(),

            "city":
                fake.city(),

            "state":
                fake.state(),

            "zip_code":
                fake.postcode(),

            "registration_date":
                registration_date.isoformat(),

            "insurance_provider":
                payer["name"],

            "insurance_id":
                insurance_id,

            "primary_insurance_code":
                payer["code"],

            "patient_status":
                random.choice([
                    "Active",
                    "Active",
                    "Active",
                    "Inactive"
                ]),

            "created_at":
                created_at.strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),

            "updated_at":
                updated_at.strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
        }

        patients.append(patient)

    return pd.DataFrame(patients)


# ============================================================
# GENERATE PROVIDERS
# ============================================================

def generate_providers(number_of_providers):

    providers = []

    for i in range(
        1,
        number_of_providers + 1
    ):

        provider_id = f"PR{i:05d}"

        provider_code = f"PRV{i:06d}"

        specialization, department = random.choice(
            SPECIALTIES
        )

        location = random.choice(
            HOSPITALS
        )

        hire_date = random_date(
            datetime(2010, 1, 1).date(),
            datetime(2025, 12, 31).date()
        )

        created_at = datetime.combine(
            hire_date,
            datetime.min.time()
        ) + timedelta(
            hours=random.randint(8, 17)
        )

        updated_at = created_at + timedelta(
            days=random.randint(0, 100)
        )

        provider = {

            "provider_id":
                provider_id,

            "provider_code":
                provider_code,

            "first_name":
                fake.first_name(),

            "last_name":
                fake.last_name(),

            "specialization":
                specialization,

            "department":
                department,

            "license_number":
                f"LIC{i:06d}",

            "phone":
                fake.numerify("9#########"),

            "email":
                fake.email(),

            "hospital_name":
                location["name"],

            "city":
                location["city"],

            "state":
                location["state"],

            "zip_code":
                location["zip"],

            "location_code":
                location["code"],

            "hire_date":
                hire_date.isoformat(),

            "years_of_experience":
                random.randint(1, 30),

            "provider_status":
                random.choice([
                    "Active",
                    "Active",
                    "Active",
                    "Inactive"
                ]),

            "created_at":
                created_at.strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),

            "updated_at":
                updated_at.strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
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

    appointments = []

    patient_ids = patients_df[
        "patient_id"
    ].tolist()

    provider_ids = providers_df[
        "provider_id"
    ].tolist()

    provider_locations = dict(
        zip(
            providers_df["provider_id"],
            providers_df["location_code"]
        )
    )

    location_details = {
        location["code"]: location
        for location in HOSPITALS
    }

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

    for i in range(
        1,
        number_of_appointments + 1
    ):

        appointment_id = f"A{i:06d}"

        appointment_number = (
            f"APT{i:07d}"
        )

        patient_id = random.choice(
            patient_ids
        )

        provider_id = random.choice(
            provider_ids
        )

        location_code = provider_locations[
            provider_id
        ]

        location = location_details[
            location_code
        ]

        procedure = random.choice(
            PROCEDURES
        )

        appointment_date = random_date(
            datetime(2025, 1, 1).date(),
            datetime(2026, 8, 31).date()
        )

        hour, minute = random_time()

        scheduled_start = datetime(
            appointment_date.year,
            appointment_date.month,
            appointment_date.day,
            hour,
            minute
        )

        scheduled_end = (
            scheduled_start
            + timedelta(
                minutes=procedure["duration"]
            )
        )

        appointment_status = random.choice(
            appointment_statuses
        )

        # Default values
        check_in_time = ""

        completed_time = ""

        cancelled_at = ""

        cancellation_reason = ""

        diagnosis = ""

        notes = ""

        if appointment_status == "Completed":

            check_in_time = (
                scheduled_start
                + timedelta(
                    minutes=random.randint(
                        -10,
                        15
                    )
                )
            ).strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            completed_time = (
                scheduled_end
                + timedelta(
                    minutes=random.randint(
                        0,
                        30
                    )
                )
            ).strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            diagnosis = random.choice(
                diagnoses
            )

            notes = random.choice([
                "Follow-up required",
                "Medication prescribed",
                "Patient advised to rest",
                "Routine monitoring recommended",
                "No further action required"
            ])

        elif appointment_status == "Cancelled":

            cancelled_at = (
                scheduled_start
                - timedelta(
                    days=random.randint(
                        1,
                        7
                    )
                )
            ).strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            cancellation_reason = random.choice([
                "Patient requested cancellation",
                "Provider unavailable",
                "Scheduling conflict",
                "Emergency situation"
            ])

        elif appointment_status == "No Show":

            notes = "Patient did not attend appointment"

        created_at = (
            scheduled_start
            - timedelta(
                days=random.randint(
                    1,
                    30
                )
            )
        )

        updated_at = (
            created_at
            + timedelta(
                days=random.randint(
                    0,
                    10
                )
            )
        )

        appointment = {

            "appointment_id":
                appointment_id,

            "appointment_number":
                appointment_number,

            "patient_id":
                patient_id,

            "provider_id":
                provider_id,

            "hospital_name":
                location["name"],

            "city":
                location["city"],

            "state":
                location["state"],

            "zip_code":
                location["zip"],

            "location_code":
                location["code"],

            "procedure_code":
                procedure["code"],

            "procedure_name":
                procedure["name"],

            "procedure_category":
                procedure["category"],

            "standard_duration_minutes":
                procedure["duration"],

            "standard_charge":
                procedure["charge"],

            "appointment_date":
                appointment_date.isoformat(),

            "appointment_time":
                f"{hour:02d}:{minute:02d}:00",

            "appointment_status":
                appointment_status,

            "check_in_time":
                check_in_time,

            "completed_time":
                completed_time,

            "cancelled_at":
                cancelled_at,

            "cancellation_reason":
                cancellation_reason,

            "reason":
                random.choice(reasons),

            "diagnosis":
                diagnosis,

            "notes":
                notes,

            "created_at":
                created_at.strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),

            "updated_at":
                updated_at.strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
        }

        appointments.append(
            appointment
        )

    return pd.DataFrame(appointments)


# ============================================================
# GENERATE PAYMENTS / CLAIMS SOURCE DATA
# ============================================================

def generate_payments(
    appointments_df,
    patients_df
):

    payments = []

    patient_payers = dict(
        zip(
            patients_df["patient_id"],
            patients_df["primary_insurance_code"]
        )
    )

    payer_details = {
        payer["code"]: payer
        for payer in INSURANCE_PAYERS
    }

    for i, appointment in enumerate(
        appointments_df.itertuples(
            index=False
        ),
        start=1
    ):

        payment_id = f"PAY{i:06d}"

        payment_number = (
            f"PMT{i:07d}"
        )

        appointment_id = (
            appointment.appointment_id
        )

        patient_id = (
            appointment.patient_id
        )

        payer_code = patient_payers[
            patient_id
        ]

        payer = payer_details[
            payer_code
        ]

        # ----------------------------------------------------
        # BILLED AMOUNT
        # ----------------------------------------------------

        billed_amount = round(
            float(
                appointment.standard_charge
            ),
            2
        )

        # ----------------------------------------------------
        # CLAIM VALUES
        # ----------------------------------------------------

        if payer_code == "SELF":

            allowed_amount = billed_amount

            insurance_amount = 0.00

            patient_responsibility = (
                billed_amount
            )

        else:

            # Insurance payer allows between
            # 80% and 100% of billed amount
            allowed_amount = round(
                billed_amount
                * random.uniform(
                    0.80,
                    1.00
                ),
                2
            )

            # Insurance pays between
            # 70% and 100% of allowed amount
            insurance_amount = round(
                allowed_amount
                * random.uniform(
                    0.70,
                    1.00
                ),
                2
            )

            patient_responsibility = round(
                allowed_amount
                - insurance_amount,
                2
            )

        # ----------------------------------------------------
        # CLAIM STATUS
        # ----------------------------------------------------

        if appointment.appointment_status == "Completed":

            claim_status = random.choice([
                "Submitted",
                "Processed",
                "Paid",
                "Paid"
            ])

        elif appointment.appointment_status == "Cancelled":

            claim_status = "Not Applicable"

        else:

            claim_status = "Pending"

        # ----------------------------------------------------
        # CLAIM DATES
        # ----------------------------------------------------

        appointment_datetime = datetime.strptime(
            f"{appointment.appointment_date} "
            f"{appointment.appointment_time}",
            "%Y-%m-%d %H:%M:%S"
        )

        submitted_at = ""

        processed_at = ""

        if claim_status != "Not Applicable":

            submitted_datetime = (
                appointment_datetime
                + timedelta(
                    days=random.randint(
                        1,
                        3
                    )
                )
            )

            submitted_at = (
                submitted_datetime.strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            )

            if claim_status in [
                "Processed",
                "Paid"
            ]:

                processed_datetime = (
                    submitted_datetime
                    + timedelta(
                        days=random.randint(
                            1,
                            10
                        )
                    )
                )

                processed_at = (
                    processed_datetime.strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                )

        # ----------------------------------------------------
        # PAYMENT
        # ----------------------------------------------------

        if claim_status == "Paid":

            payment_status = "Paid"

            payment_amount = (
                patient_responsibility
            )

            payment_method = (
                "Insurance"
                if payer_code != "SELF"
                else random.choice([
                    "Credit Card",
                    "Debit Card",
                    "Cash",
                    "UPI"
                ])
            )

        elif appointment.appointment_status == "Cancelled":

            payment_status = "Failed"

            payment_amount = 0.00

            payment_method = "UPI"

        else:

            payment_status = "Pending"

            payment_amount = 0.00

            payment_method = (
                "Insurance"
                if payer_code != "SELF"
                else "UPI"
            )

        # ----------------------------------------------------
        # PAYMENT TYPE
        # ----------------------------------------------------

        if payer_code == "SELF":

            payment_type = "Patient Payment"

        else:

            payment_type = "Insurance Payment"

        payment_date = (
            appointment.appointment_date
        )

        created_at = datetime.strptime(
            payment_date,
            "%Y-%m-%d"
        )

        updated_at = (
            created_at
            + timedelta(
                days=random.randint(
                    0,
                    10
                )
            )
        )

        payment = {

            "payment_id":
                payment_id,

            "payment_number":
                payment_number,

            "appointment_id":
                appointment_id,

            "patient_id":
                patient_id,

            "claim_number":
                f"CLM{i:07d}",

            "amount":
                billed_amount,

            "allowed_amount":
                allowed_amount,

            "insurance_amount":
                insurance_amount,

            "patient_amount":
                patient_responsibility,

            "payment_method":
                payment_method,

            "payment_type":
                payment_type,

            "payment_date":
                payment_date,

            "payment_status":
                payment_status,

            "claim_status":
                claim_status,

            "submitted_at":
                submitted_at,

            "processed_at":
                processed_at,

            "transaction_id":
                f"TXN{i:08d}",

            "currency":
                "INR",

            "created_at":
                created_at.strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),

            "updated_at":
                updated_at.strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
        }

        payments.append(payment)

    return pd.DataFrame(payments)


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("=" * 70)
    print("GENERATING HEALTHCARE SAMPLE DATA")
    print("=" * 70)

    # Create data/raw if it doesn't exist
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # --------------------------------------------------------
    # Patients
    # --------------------------------------------------------

    print()
    print("Generating patients...")

    patients_df = generate_patients(
        NUMBER_OF_PATIENTS
    )

    # --------------------------------------------------------
    # Providers
    # --------------------------------------------------------

    print("Generating providers...")

    providers_df = generate_providers(
        NUMBER_OF_PROVIDERS
    )

    # --------------------------------------------------------
    # Appointments
    # --------------------------------------------------------

    print("Generating appointments...")

    appointments_df = generate_appointments(
        NUMBER_OF_APPOINTMENTS,
        patients_df,
        providers_df
    )

    # --------------------------------------------------------
    # Payments / Claims source data
    # --------------------------------------------------------

    print("Generating payments...")

    payments_df = generate_payments(
        appointments_df,
        patients_df
    )

    # --------------------------------------------------------
    # Save files
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
    # Summary
    # --------------------------------------------------------

    print()
    print("=" * 70)
    print("DATA GENERATION COMPLETED")
    print("=" * 70)

    print(
        f"Patients       : {len(patients_df)}"
    )

    print(
        f"Providers      : {len(providers_df)}"
    )

    print(
        f"Appointments   : {len(appointments_df)}"
    )

    print(
        f"Payments       : {len(payments_df)}"
    )

    print()
    print(
        f"Files saved to: {OUTPUT_DIR}"
    )

    print("=" * 70)


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()