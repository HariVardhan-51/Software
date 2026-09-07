# Source-to-Target Data Mapping

## 1. Document Purpose

This document defines the mapping between the raw source data and the
final core tables in the `clinic_db` PostgreSQL database.

The purpose of this document is to provide a clear understanding of:

- Source files
- Raw PostgreSQL tables
- Target core tables
- Source-to-target column mappings
- Transformations
- Lookup logic
- Primary key generation
- Foreign key relationships

---

# 2. Data Flow

The overall data flow is:

CSV Files
    |
    v
PostgreSQL RAW Layer
    |
    v
Data Validation
    |
    v
Transformation
    |
    v
PostgreSQL CORE Layer


Source files:

    patients.csv
    providers.csv
    appointments.csv
    payments.csv


RAW tables:

    raw.patients_file
    raw.providers_file
    raw.appointments_file
    raw.payments_file


CORE tables:

    core.locations
    core.patients
    core.providers
    core.procedure_types
    core.appointments
    core.insurance_payers
    core.claims
    core.payments


# 3. High-Level Source-to-Target Mapping

| Source File | Raw Table | Target Core Tables |
|-------------|-----------|--------------------|
| patients.csv | raw.patients_file | core.patients, core.insurance_payers |
| providers.csv | raw.providers_file | core.providers, core.locations |
| appointments.csv | raw.appointments_file | core.appointments, core.procedure_types, core.locations |
| payments.csv | raw.payments_file | core.claims, core.payments |

Additional relationships are used between raw datasets during
transformation.

For example:

    raw.appointments_file.patient_id
        -> raw.patients_file.patient_id
        -> patient insurance information
        -> core.insurance_payers

Therefore, the mapping is not always a direct one-file-to-one-table
relationship.


# 4. Source File: patients.csv

## Source

    data/raw/patients.csv

## Raw Table

    raw.patients_file

## Target Tables

    core.patients
    core.insurance_payers


## 4.1 patients.csv -> core.patients

| Source Column | Target Column | Transformation |
|---------------|---------------|----------------|
| patient_id | patient_id | Generate new BIGINT identity key in target |
| patient_number | patient_number | Direct mapping |
| first_name | first_name | Direct mapping |
| last_name | last_name | Direct mapping |
| date_of_birth | date_of_birth | Convert TEXT to DATE |
| gender | gender | Direct mapping |
| zip_code | zip_code | Direct mapping |
| registration_date | registration_date | Convert TEXT to DATE |
| patient_status | patient_status | Direct mapping |
| primary_insurance_code | primary_insurance_code | Direct mapping |
| created_at | created_at | Convert TEXT to TIMESTAMP |
| updated_at | updated_at | Convert TEXT to TIMESTAMP |


### Columns not loaded into core.patients

The following raw columns are retained in the raw layer but are not
part of the required core.patients table:

    phone
    email
    city
    state
    insurance_provider
    insurance_id

The raw layer preserves the original source information.


## 4.2 patients.csv -> core.insurance_payers

Insurance payer information is extracted from the patient source data.

| Source Column | Target Column | Transformation |
|---------------|---------------|----------------|
| primary_insurance_code | payer_code | Direct mapping |
| insurance_provider | payer_name | Direct mapping |
| - | payer_type | Derived from insurance provider |
| - | is_active | Default TRUE |
| created_at | created_at | Convert TEXT to TIMESTAMP |
| updated_at | updated_at | Convert TEXT to TIMESTAMP |

### Deduplication

Multiple patients may use the same insurance payer.

For example:

    P00001 -> HCP
    P00002 -> HCP
    P00003 -> HCP

Only one payer record should be created:

    HCP -> HealthCare Plus

Therefore:

    DISTINCT primary_insurance_code


# 5. Source File: providers.csv

## Source

    data/raw/providers.csv

## Raw Table

    raw.providers_file

## Target Tables

    core.providers
    core.locations


# 5.1 providers.csv -> core.locations

Provider location information is used to create location records.

| Source Column | Target Column | Transformation |
|---------------|---------------|----------------|
| location_code | location_code | Direct mapping |
| hospital_name | location_name | Direct mapping |
| city | address_city | Direct mapping |
| state | address_state | Direct mapping |
| zip_code | zip_code | Direct mapping |
| phone | phone | Direct mapping |
| - | is_active | Default TRUE |
| created_at | created_at | Convert TEXT to TIMESTAMP |
| updated_at | updated_at | Convert TEXT to TIMESTAMP |

### Location deduplication

The same location can have multiple providers.

Example:

    PRV000001 -> LOC001
    PRV000002 -> LOC001
    PRV000003 -> LOC001

Only one location record should be created:

    LOC001 -> City Care Hospital

The unique business key is:

    location_code


# 5.2 providers.csv -> core.providers

| Source Column | Target Column | Transformation |
|---------------|---------------|----------------|
| provider_id | provider_id | Generate new BIGINT identity key |
| provider_code | provider_code | Direct mapping |
| first_name | first_name | Direct mapping |
| last_name | last_name | Direct mapping |
| specialization | specialty | Rename column |
| location_code | primary_location_id | Lookup core.locations.location_id |
| hire_date | hire_date | Convert TEXT to DATE |
| provider_status | provider_status | Direct mapping |
| created_at | created_at | Convert TEXT to TIMESTAMP |
| updated_at | updated_at | Convert TEXT to TIMESTAMP |

### Location lookup

The raw provider contains:

    location_code = LOC001

The transformation looks up:

    core.locations.location_code = LOC001

and obtains:

    core.locations.location_id = 1

Then:

    core.providers.primary_location_id = 1


# 6. Source File: appointments.csv

## Source

    data/raw/appointments.csv

## Raw Table

    raw.appointments_file

## Target Tables

    core.appointments
    core.procedure_types
    core.locations

Appointments also participate in relationships with:

    core.patients
    core.providers
    core.insurance_payers
    core.claims


# 6.1 appointments.csv -> core.procedure_types

| Source Column | Target Column | Transformation |
|---------------|---------------|----------------|
| procedure_code | procedure_code | Direct mapping |
| procedure_name | procedure_name | Direct mapping |
| procedure_category | procedure_category | Direct mapping |
| standard_duration_minutes | standard_duration_minutes | Convert TEXT to INTEGER |
| standard_charge | standard_charge | Convert TEXT to NUMERIC |
| - | is_active | Default TRUE |
| created_at | created_at | Convert TEXT to TIMESTAMP |
| updated_at | updated_at | Convert TEXT to TIMESTAMP |

### Deduplication

The same procedure can occur in thousands of appointments.

Example:

    A000001 -> CONS001
    A000002 -> CONS001
    A000003 -> CONS001

Only one procedure record should exist:

    CONS001 -> General Consultation

The business key is:

    procedure_code


# 6.2 appointments.csv -> core.locations

Appointment location information is also available in the appointment
source.

| Source Column | Target Column | Transformation |
|---------------|---------------|----------------|
| location_code | location_code | Direct mapping |
| hospital_name | location_name | Direct mapping |
| city | address_city | Direct mapping |
| state | address_state | Direct mapping |
| zip_code | zip_code | Direct mapping |
| - | phone | NULL if unavailable |
| - | is_active | Default TRUE |
| created_at | created_at | Convert TEXT to TIMESTAMP |
| updated_at | updated_at | Convert TEXT to TIMESTAMP |

### Important

Locations may already have been created from providers.csv.

Therefore, the transformation must use:

    location_code

to identify an existing location before inserting a new one.

This prevents duplicate locations.


# 6.3 appointments.csv -> core.appointments

| Source Column | Target Column | Transformation |
|---------------|---------------|----------------|
| appointment_id | appointment_id | Generate new BIGINT identity key |
| appointment_number | appointment_number | Direct mapping |
| patient_id | patient_id | Lookup core.patients |
| provider_id | provider_id | Lookup core.providers |
| location_code | location_id | Lookup core.locations |
| procedure_code | procedure_type_id | Lookup core.procedure_types |
| appointment_date + appointment_time | scheduled_start | Combine and convert to TIMESTAMP |
| standard_duration_minutes | scheduled_end | scheduled_start + duration |
| appointment_status | appointment_status | Direct mapping |
| check_in_time | check_in_time | Convert TEXT to TIMESTAMP |
| completed_time | completed_time | Convert TEXT to TIMESTAMP |
| cancelled_at | cancelled_at | Convert TEXT to TIMESTAMP |
| cancellation_reason | cancellation_reason | Direct mapping |
| created_at | created_at | Convert TEXT to TIMESTAMP |
| updated_at | updated_at | Convert TEXT to TIMESTAMP |


## Appointment patient lookup

Source:

    raw.appointments_file.patient_id

Lookup:

    core.patients.patient_number

The transformation must maintain a mapping between the raw patient
identifier and the generated core patient identifier.

Example:

    Raw patient:
        P00001

    Core patient:
        patient_id = 1
        patient_number = PAT000001

Appointment:

    raw patient_id = P00001

becomes:

    core appointment.patient_id = 1


## Appointment provider lookup

Source:

    raw.appointments_file.provider_id

Lookup:

    core.providers.provider_code

Example:

    Raw provider:
        PR00001

    Core provider:
        provider_id = 1
        provider_code = PRV000001

The appointment stores:

    provider_id = 1


## Appointment location lookup

Source:

    location_code

Lookup:

    core.locations.location_code

Example:

    LOC001 -> location_id 1

Therefore:

    core.appointments.location_id = 1


## Appointment procedure lookup

Source:

    procedure_code

Lookup:

    core.procedure_types.procedure_code

Example:

    CONS001 -> procedure_type_id 1

Therefore:

    core.appointments.procedure_type_id = 1


# 7. Source File: payments.csv

## Source

    data/raw/payments.csv

## Raw Table

    raw.payments_file

## Target Tables

    core.claims
    core.payments


# 7.1 payments.csv -> core.claims

| Source Column | Target Column | Transformation |
|---------------|---------------|----------------|
| claim_number | claim_number | Direct mapping |
| appointment_id | appointment_id | Lookup core.appointments |
| patient_id | patient_id | Lookup core.patients |
| claim payer information | payer_id | Lookup core.insurance_payers |
| amount | billed_amount | Convert TEXT to NUMERIC |
| allowed_amount | allowed_amount | Convert TEXT to NUMERIC |
| insurance_amount | insurance_paid_amount | Rename + convert to NUMERIC |
| patient_amount | patient_responsibility | Rename + convert to NUMERIC |
| claim_status | claim_status | Direct mapping |
| submitted_at | submitted_at | Convert TEXT to TIMESTAMP |
| processed_at | processed_at | Convert TEXT to TIMESTAMP |
| created_at | created_at | Convert TEXT to TIMESTAMP |
| updated_at | updated_at | Convert TEXT to TIMESTAMP |


## Claim payer lookup

The payment source itself does not contain a direct payer_code column.

The payer is obtained through the patient.

Relationship:

    payments.patient_id
            |
            v
    patients.primary_insurance_code
            |
            v
    insurance_payers.payer_code
            |
            v
    insurance_payers.payer_id


Example:

    payment.patient_id = P00001

    P00001 ->
        primary_insurance_code = HCP

    HCP ->
        payer_id = 1

Therefore:

    claim.payer_id = 1


# 7.2 payments.csv -> core.payments

| Source Column | Target Column | Transformation |
|---------------|---------------|----------------|
| payment_id | payment_id | Generate new BIGINT identity key |
| payment_number | payment_number | Direct mapping |
| patient_id | patient_id | Lookup core.patients |
| appointment_id | appointment_id | Lookup core.appointments |
| claim_number | claim_id | Lookup core.claims |
| payment_type | payment_type | Direct mapping |
| patient_amount | payment_amount | Rename + convert to NUMERIC |
| payment_date | payment_date | Convert TEXT to DATE |
| payment_status | payment_status | Direct mapping |
| created_at | created_at | Convert TEXT to TIMESTAMP |
| updated_at | updated_at | Convert TEXT to TIMESTAMP |


## Claim lookup

The payment contains:

    claim_number

The transformation looks up:

    core.claims.claim_number

and obtains:

    core.claims.claim_id

Example:

    CLM0000001 -> claim_id 1

Therefore:

    core.payments.claim_id = 1


# 8. Complete Core Table Mapping

## core.locations

Primary source:

    providers.csv

Secondary source:

    appointments.csv

Business key:

    location_code


Mapping:

    location_code
        -> location_code

    hospital_name
        -> location_name

    city
        -> address_city

    state
        -> address_state

    zip_code
        -> zip_code


# core.patients

Source:

    patients.csv

Business key:

    patient_number


Mapping:

    patient_number
    first_name
    last_name
    date_of_birth
    gender
    zip_code
    registration_date
    patient_status
    primary_insurance_code


# core.providers

Source:

    providers.csv

Business key:

    provider_code


Mapping:

    provider_code
    first_name
    last_name
    specialization -> specialty
    location_code -> primary_location_id
    hire_date
    provider_status


# core.procedure_types

Source:

    appointments.csv

Business key:

    procedure_code


Mapping:

    procedure_code
    procedure_name
    procedure_category
    standard_duration_minutes
    standard_charge


# core.appointments

Source:

    appointments.csv

Business key:

    appointment_number


Mapping:

    appointment_number
    patient_id
    provider_id
    location_id
    procedure_type_id
    scheduled_start
    scheduled_end
    appointment_status
    check_in_time
    completed_time
    cancelled_at
    cancellation_reason


# core.insurance_payers

Source:

    patients.csv

Business key:

    primary_insurance_code


Mapping:

    primary_insurance_code -> payer_code
    insurance_provider -> payer_name


# core.claims

Source:

    payments.csv

Business key:

    claim_number


Mapping:

    claim_number
    appointment_id
    patient_id
    payer_id
    amount -> billed_amount
    allowed_amount
    insurance_amount -> insurance_paid_amount
    patient_amount -> patient_responsibility
    claim_status
    submitted_at
    processed_at


# core.payments

Source:

    payments.csv

Business key:

    payment_number


Mapping:

    payment_number
    patient_id
    appointment_id
    claim_id
    payment_type
    patient_amount -> payment_amount
    payment_date
    payment_status


# 9. Transformation Rules

## 9.1 Data Type Conversion

Raw tables store source values primarily as TEXT.

The core layer converts them to appropriate PostgreSQL data types.

| Raw Data | Core Data Type |
|----------|----------------|
| Date strings | DATE |
| Timestamp strings | TIMESTAMP |
| Numeric strings | NUMERIC |
| Duration strings | INTEGER |
| Active status | BOOLEAN |
| Business identifiers | VARCHAR |
| Descriptions | VARCHAR / TEXT |


## 9.2 Primary Key Generation

Raw source IDs are treated as source/business identifiers.

Core tables use generated BIGINT primary keys.

Example:

    raw:
        patient_id = P00001

    core:
        patient_id = 1
        patient_number = PAT000001


This separates the internal database key from the source identifier.


## 9.3 Foreign Key Lookup

Foreign keys are populated using business keys.

Examples:

    location_code
        -> core.locations.location_id

    provider_code
        -> core.providers.provider_id

    procedure_code
        -> core.procedure_types.procedure_type_id

    patient_number
        -> core.patients.patient_id

    claim_number
        -> core.claims.claim_id


## 9.4 Deduplication

Reference/master tables must be deduplicated before insertion.

Tables requiring deduplication include:

    core.locations
    core.procedure_types
    core.insurance_payers


Business keys:

    locations:
        location_code

    procedure_types:
        procedure_code

    insurance_payers:
        payer_code


# 10. Load Order

Because the core tables contain foreign keys, they should be populated
in dependency order.

Recommended load order:

    1. core.locations

    2. core.patients

    3. core.providers

    4. core.procedure_types

    5. core.insurance_payers

    6. core.appointments

    7. core.claims

    8. core.payments


# 11. Relationship Diagram

The final core model is:

                         core.locations
                              |
                              |
                    +---------+---------+
                    |                   |
                    v                   v
             core.providers      core.appointments
                                      |
                    +-----------------+----------------+
                    |                 |                |
                    v                 v                v
             core.patients    core.procedure_types   core.claims
                                                        |
                                                        |
                                                        v
                                             core.insurance_payers


core.appointments
        |
        |
        v
core.payments


# 12. End-to-End Data Flow

patients.csv
    |
    +--------------------> core.patients
    |
    +--------------------> core.insurance_payers


providers.csv
    |
    +--------------------> core.providers
    |
    +--------------------> core.locations


appointments.csv
    |
    +--------------------> core.appointments
    |
    +--------------------> core.procedure_types
    |
    +--------------------> core.locations


payments.csv
    |
    +--------------------> core.claims
    |
    +--------------------> core.payments


# 13. Data Quality Checks Before Core Load

The following validations should be completed before loading data
into the core layer:

    - Required columns exist
    - Primary keys are not null
    - Primary keys are not duplicated
    - Appointment statuses are valid
    - Payment amounts are not negative
    - Appointment patient IDs exist
    - Payment appointment IDs exist
    - Dates are valid
    - Financial amounts are consistent


# 14. Expected Result

After successful transformation, the database should contain:

    clinic_db
    |
    +-- raw
    |   +-- patients_file
    |   +-- providers_file
    |   +-- appointments_file
    |   +-- payments_file
    |
    +-- core
        +-- locations
        +-- patients
        +-- providers
        +-- procedure_types
        +-- appointments
        +-- insurance_payers
        +-- claims
        +-- payments


The raw layer preserves the source data.

The core layer contains cleaned, typed, normalized and relational data
that is ready for downstream analytics and reporting.