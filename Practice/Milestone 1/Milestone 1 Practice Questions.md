# Milestone 1 Practice Questions

## Category 1: Pandas

### 1.1 Event Ticket Revenue Analysis (Pandas) [Completed]

#### Problem Statement
A ticketing platform receives daily transactional records in `ticket_sales.csv` and master metadata in `events.csv`. Raw transaction exports can contain repeated identifiers, incomplete contact fields, and references that are not present in the master file. Management needs a trustworthy event-category financial report built only from valid, matching records.

#### Business Objective
Compute $\text{tickets} \times \text{ticket\_price} \times (1 - \text{discount\_pct} / 100)$. Report the average and total of the calculated metric, together with the valid record count, for each category.

#### Project Structure & Dependencies
```text
Project/
├── main.py
├── requirements.txt
├── tests.py
└── data/
    ├── ticket_sales.csv
    └── events.csv
```
- **Dependencies:** `pandas`, `pytest`

#### Input Data

##### `ticket_sales.csv`
| sale_id | event_id | buyer_name | buyer_email | tickets | ticket_price | discount_pct | sale_date |
|---|---|---|---|---|---|---|---|
| 5001 | 301 | Asha Rao | asha@example.com | 2 | 1500 | 10 | 2026-10-01 |
| 5002 | 302 | Ravi Sen | ravi@example.com | 1 | 2200 | 0 | 2026-10-02 |
| 5003 | 303 | Mina Das | mina@example.com | 3 | 900 | 5 | 2026-10-03 |
| 5004 | 301 | Kabir Roy | kabir@example.com | 1 | 1500 | 0 | 2026-10-04 |
| 5005 | 302 | Tara Jain | | 2 | 2200 | 10 | 2026-10-05 |
| 5002 | 302 | Ravi Sen | ravi2@example.com | 4 | 2200 | 0 | 2026-10-06 |
| 5006 | 999 | Neel Shah | neel@example.com | 1 | 700 | 0 | 2026-10-07 |

##### `events.csv`
| event_id | event_name | category | venue |
|---|---|---|---|
| 301 | Jazz Evening | Music | Hall A |
| 302 | Tech Summit | Technology | Hall B |
| 303 | Food Carnival | Lifestyle | Open Ground |

#### Required Implementation (`main.py`)
Implement all six functions in `main.py`. Each function must return a DataFrame. Do not print from pipeline functions.

1. **`load_ticket_sales(file_path)`**
   - Read CSV `file_path`.
   - Return exactly: `sale_id`, `event_id`, `buyer_name`, `buyer_email`, `tickets`, `ticket_price`, `discount_pct` in that order (do not return `sale_date`).
2. **`clean_ticket_sales(df)`**
   - Remove records where `buyer_email` is missing (`NaN` / `None`).
   - Remove duplicate `sale_id` records while retaining the earliest row in input order. Preserve all other columns.
3. **`merge_with_events(df, ref_file_path)`**
   - Load `events.csv`; execute an inner join using `event_id`. Discard records without a matching reference.
   - Keep all transaction columns and add reference-only columns in reference-file order (`event_name`, `category`, `venue`).
4. **`add_net_ticket_value(df)`**
   - Create numeric `net_ticket_value` = $\text{tickets} \times \text{ticket\_price} \times (1 - \text{discount\_pct} / 100)$.
   - Round each computed row to two decimal places. Retain all existing columns.
5. **`aggregate_by_category(df)`**
   - Group by `category`.
   - Return `category`, `avg_net_ticket_value` (mean), `total_net_ticket_revenue` (sum), and `valid_sale_count` (number of rows). Use these exact output names. Reset index.
6. **`finalize_summary(df)`**
   - Return only `category`, `avg_net_ticket_value`, `total_net_ticket_revenue`, `valid_sale_count` in that order.
   - Round monetary summaries to 2 decimal places, sort by `category` ascending, and reset index. Preserve this schema even for empty data.

#### Main Block & Constraints
- Under `if __name__ == "__main__":`, execute functions 1–6 in order, passing intermediate DataFrames to the next function. Print only the final summary DataFrame. Read CSV paths from `data/` inside the main block.
- **Constraints:**
  - Function names and parameters must match exactly. Each function must be independently callable and return a DataFrame.
  - Use vectorized Pandas operations (no row-by-row loops); do not hard-code values, use global intermediate variables, or mutate input frames in place.
  - With no matching/valid rows, aggregation and finalization must return an empty DataFrame with the prescribed columns.
  - Deduplicate before joining (e.g. sale 5002 keeps its first row; remove missing-email and unmatched-event records).

#### Expected Output (for sample inputs)
| category | avg_net_ticket_value | total_net_ticket_revenue | valid_sale_count |
|---|---|---|---|
| Lifestyle | 2565.00 | 2565.00 | 1 |
| Music | 2100.00 | 4200.00 | 2 |
| Technology | 2200.00 | 2200.00 | 1 |

---

### 1.2 Vehicle Service Invoice Analysis (Pandas)

#### Problem Statement
A vehicle service network receives transactional records in `service_invoices.csv` and master metadata in `service_centres.csv`. Raw invoice exports can contain repeated invoice identifiers, missing customer contact values, and centre IDs absent from the master file. Operations needs a trustworthy service-type financial report from valid, matching records.

#### Business Objective
Compute $(\text{labour\_hours} \times \text{hourly\_rate} + \text{parts\_charge}) \times (1 - \text{discount\_pct} / 100)$. Report the average and total of the calculated metric, together with the valid record count, for each `service_type`.

#### Project Structure & Dependencies
```text
Project/
├── main.py
├── requirements.txt
├── tests.py
└── data/
    ├── service_invoices.csv
    └── service_centres.csv
```
- **Dependencies:** `pandas`, `pytest`

#### Input Data

##### `service_invoices.csv`
| invoice_id | centre_id | customer_name | customer_email | labour_hours | hourly_rate | parts_charge | discount_pct | invoice_date |
|---|---|---|---|---|---|---|---|---|
| 6101 | 401 | Nora Shah | nora@example.com | 2 | 900 | 500 | 10 | 2026-10-11 |
| 6102 | 402 | Arun Das | arun@example.com | 1 | 1200 | 800 | 0 | 2026-10-12 |
| 6103 | 403 | Leah Roy | leah@example.com | 3 | 750 | 300 | 5 | 2026-10-13 |
| 6104 | 401 | Mohan Sen | mohan@example.com | 1 | 900 | 250 | 0 | 2026-10-14 |
| 6105 | 402 | Ira Jain | | 2 | 1200 | 600 | 10 | 2026-10-15 |
| 6102 | 402 | Arun Das | arun2@example.com | 4 | 1200 | 900 | 0 | 2026-10-16 |
| 6106 | 999 | Zara Rao | zara@example.com | 1 | 500 | 100 | 0 | 2026-10-17 |

##### `service_centres.csv`
| centre_id | service_type | region | centre_name |
|---|---|---|---|
| 401 | General Service | North | North Auto |
| 402 | Engine Repair | South | South Auto |
| 403 | Wheel Alignment | West | West Auto |

#### Required Implementation (`main.py`)
Implement all six functions in `main.py`. Each function must return a DataFrame. Do not print from pipeline functions.

1. **`load_service_invoices(file_path)`**
   - Read CSV `file_path`.
   - Return exactly: `invoice_id`, `centre_id`, `customer_name`, `customer_email`, `labour_hours`, `hourly_rate`, `parts_charge`, `discount_pct` in that order (do not return `invoice_date`).
2. **`clean_service_invoices(df)`**
   - Remove records where `customer_email` is missing (`NaN` / `None`).
   - Remove duplicate `invoice_id` records while retaining the earliest row in input order. Preserve all other columns.
3. **`merge_with_service_centres(df, ref_file_path)`**
   - Load `service_centres.csv`; execute an inner join using `centre_id`. Discard records without a matching reference.
   - Keep all transaction columns and add reference-only columns in reference-file order (`service_type`, `region`, `centre_name`).
4. **`add_net_invoice_value(df)`**
   - Create numeric `net_invoice_value` = $(\text{labour\_hours} \times \text{hourly\_rate} + \text{parts\_charge}) \times (1 - \text{discount\_pct} / 100)$.
   - Round each computed row to two decimal places. Retain all existing columns.
5. **`aggregate_by_service_type(df)`**
   - Group by `service_type`.
   - Return `service_type`, `avg_net_invoice_value` (mean), `total_net_invoice_value` (sum), and `valid_invoice_count` (number of rows). Use these exact output names. Reset index.
6. **`finalize_summary(df)`**
   - Return only `service_type`, `avg_net_invoice_value`, `total_net_invoice_value`, `valid_invoice_count` in that order.
   - Round monetary summaries to 2 decimal places, sort by `service_type` ascending, and reset index. Preserve this schema even for empty data.

#### Main Block & Constraints
- Under `if __name__ == "__main__":`, execute functions 1–6 in order, passing intermediate DataFrames to the next function. Print only the final summary DataFrame. Read CSV paths from `data/` inside the main block.
- **Constraints:**
  - Function names and parameters must match exactly. Each function must be independently callable and return a DataFrame.
  - Use vectorized Pandas operations (no row-by-row loops); do not hard-code values, use global intermediate variables, or mutate input frames in place.
  - With no matching/valid rows, aggregation and finalization must return an empty DataFrame with the prescribed columns.
  - Deduplicate before joining. Use transaction `hourly_rate` and `parts_charge` for invoice calculation.

#### Expected Output (for sample inputs)
| service_type | avg_net_invoice_value | total_net_invoice_value | valid_invoice_count |
|---|---|---|---|
| Engine Repair | 2000.00 | 2000.00 | 1 |
| General Service | 1610.00 | 3220.00 | 2 |
| Wheel Alignment | 2437.50 | 2437.50 | 1 |

---

### 1.3 Training Enquiry Fee Summary Pipeline (Pandas) [Completed]

#### Problem Statement
A training institute needs a report showing the average discounted fee and number of valid enquiries for each course. Raw enquiry data contains missing emails, duplicate enquiry IDs, and a reference ID that may not exist in the course catalogue.

#### Project Structure & Dependencies
```text
Project/
├── main.py
├── requirements.txt
├── tests.py
└── data/
    ├── training_enquiries.csv
    └── training_courses.csv
```
- **Dependencies:** `pandas`, `pytest`

#### Input Data

##### `training_enquiries.csv`
| enquiry_id | course_id | student_name | email | phone | quoted_fee | discount_pct | enquiry_date |
|---|---|---|---|---|---|---|---|
| 3001 | 11 | Aarav Rao | aarav@example.com | 9876501011 | 30000 | 10 | 2026-09-01 |
| 3002 | 12 | Diya Sen | diya@example.com | 9876501012 | 24000 | 5 | 2026-09-02 |
| 3003 | 13 | Kabir Das | kabir@example.com | 9876501013 | 20000 | 0 | 2026-09-03 |
| 3004 | 14 | Meera Nair | | 9876501014 | 18000 | 10 | 2026-09-04 |
| 3005 | 15 | Rohan Patil | rohan@example.com | 9876501015 | 22000 | 5 | 2026-09-05 |
| 3006 | 11 | Sana Ali | sana@example.com | 9876501016 | 32000 | 15 | 2026-09-06 |
| 3007 | 14 | Vikram Roy | vikram@example.com | 9876501017 | 19000 | 0 | 2026-09-07 |
| 3002 | 12 | Diya Sen Duplicate | diya2@example.com | 9876501099 | 25000 | 0 | 2026-09-08 |
| 3008 | 99 | Nisha Paul | nisha@example.com | 9876501018 | 26000 | 10 | 2026-09-09 |

##### `training_courses.csv`
| course_id | course_name | category | duration_months | standard_fee |
|---|---|---|---|---|
| 11 | Data Analytics | Data | 4 | 35000 |
| 12 | Python Full Stack | Software | 6 | 30000 |
| 13 | Cloud Fundamentals | Cloud | 3 | 25000 |
| 14 | Software Testing | Quality | 3 | 22000 |
| 15 | Generative AI Basics | AI | 2 | 28000 |

#### Required Implementation (`main.py`)
Implement all six functions in `main.py`. Each function must return a DataFrame. Do not print from pipeline functions.

1. **`load_student_enquiries(file_path)`**
   - Read `training_enquiries.csv`.
   - Return exactly: `enquiry_id`, `course_id`, `student_name`, `email`, `phone`, `quoted_fee`, `discount_pct` (Exclude `enquiry_date`).
2. **`clean_enquiry_data(df)`**
   - Remove rows with missing `email`.
   - For duplicate `enquiry_id` values, keep the first occurrence in input order.
3. **`merge_with_courses(enquiries_df, ref_file_path)`**
   - Read `training_courses.csv`; inner-join on `course_id`.
   - Remove unmatched records. Keep all enquiry columns plus `course_name`, `category`, `duration_months`, `standard_fee`.
4. **`add_net_quoted_fee(df)`**
   - Add `net_quoted_fee` = $\text{quoted\_fee} \times (1 - \text{discount\_pct} / 100)$, rounded to two decimal places.
5. **`aggregate_by_course(df)`**
   - Return one row per course with `course_name`, `avg_net_quoted_fee` (mean `net_quoted_fee`), and `enquiry_count` (number of valid enquiry rows). Reset the index.
6. **`finalize_summary(df)`**
   - Return columns in this order: `course_name`, `avg_net_quoted_fee`, `enquiry_count`.
   - Round average to two decimals, sort alphabetically by `course_name`, and reset index.

#### Main Block & Constraints
- Under `if __name__ == "__main__":`, call all six functions in order, passing each result to the next step. Print only the final summary DataFrame.
- **Constraints:** Use vectorized Pandas operations (no row-by-row loops), do not modify input DataFrames in place, do not use global variables for intermediate DataFrames, and do not hard-code values.

---

### 1.4 Customer Service Request Summary Pipeline (Pandas) [Completed]

#### Problem Statement
A technology support company wants a summary of quoted service fees after discounts. Its service request data may contain missing customer emails, repeated request IDs, and requests for services absent from the catalogue.

#### Project Structure & Dependencies
```text
Project/
├── main.py
├── requirements.txt
├── tests.py
└── data/
    ├── service_requests.csv
    └── service_catalogue.csv
```
- **Dependencies:** `pandas`, `pytest`

#### Input Data

##### `service_requests.csv`
| request_id | service_id | customer_name | email | phone | quoted_fee | discount_pct | request_date |
|---|---|---|---|---|---|---|---|
| 4101 | 21 | Home Wi-Fi Setup | customer1@example.com | 9000011001 | 1200 | 10 | 2026-09-11 |
| 4102 | 22 | Laptop Repair | | 9000011002 | 2500 | 5 | 2026-09-12 |
| 4103 | 23 | Data Backup | customer3@example.com | 9000011003 | 1800 | 0 | 2026-09-13 |
| 4104 | 24 | Printer Setup | customer4@example.com | 9000011004 | 900 | 10 | 2026-09-14 |
| 4105 | 21 | Home Wi-Fi Setup | customer5@example.com | 9000011005 | 1400 | 15 | 2026-09-15 |
| 4106 | 25 | Cybersecurity Check | customer6@example.com | 9000011006 | 3200 | 5 | 2026-09-16 |
| 4107 | 22 | Laptop Repair | customer7@example.com | 9000011007 | 2300 | 0 | 2026-09-17 |
| 4103 | 23 | Data Backup Duplicate | duplicate@example.com | 9000011099 | 1900 | 0 | 2026-09-18 |
| 4108 | 88 | Unknown Service | customer8@example.com | 9000011008 | 700 | 0 | 2026-09-19 |

##### `service_catalogue.csv`
| service_id | service_name | category | duration_days | standard_fee |
|---|---|---|---|---|
| 21 | Home Wi-Fi Setup | Networking | 1 | 1500 |
| 22 | Laptop Repair | Hardware | 2 | 3000 |
| 23 | Data Backup | Data Services | 1 | 2200 |
| 24 | Printer Setup | Peripherals | 1 | 1200 |
| 25 | Cybersecurity Check | Security | 2 | 4000 |

#### Required Implementation (`main.py`)
Implement all six functions in `main.py`. Each function must return a DataFrame. Do not print from pipeline functions.

1. **`load_service_requests(file_path)`**
   - Read `service_requests.csv`.
   - Return exactly: `request_id`, `service_id`, `customer_name`, `email`, `phone`, `quoted_fee`, `discount_pct` (Exclude `request_date`).
2. **`clean_service_requests(df)`**
   - Remove rows with missing `email`.
   - For duplicate `request_id` values, keep the first occurrence in input order.
3. **`merge_with_services(requests_df, ref_file_path)`**
   - Read `service_catalogue.csv`; inner-join on `service_id`.
   - Remove unmatched records. Keep all request columns plus `service_name`, `category`, `duration_days`, `standard_fee`.
4. **`add_net_quoted_fee(df)`**
   - Add `net_quoted_fee` = $\text{quoted\_fee} \times (1 - \text{discount\_pct} / 100)$, rounded to two decimal places.
5. **`aggregate_by_service(df)`**
   - Return one row per service with `service_name`, `avg_net_quoted_fee` (mean `net_quoted_fee`), and `request_count` (number of valid request rows). Reset the index.
6. **`finalize_summary(df)`**
   - Return columns in this order: `service_name`, `avg_net_quoted_fee`, `request_count`.
   - Round average to two decimals, sort alphabetically by `service_name`, and reset index.

---

## Category 2: FastAPI Applications

### 2.1 Gym and Membership Plans API [Completed]

#### Problem Statement
A fitness organization manages gym branches and membership plans offered at each branch. Staff register branches, add plans, retrieve a branch with its plans, optionally filter by membership duration, sort plans by name or monthly fee, and update plan details without transferring a plan to another branch.

#### Project Structure & Dependencies
```text
Project/
├── database.py
├── models.py
├── schemas.py
├── main.py
├── requirements.txt
└── tests.py
```
- **SQLite Database:** `gym_memberships.db`
- **Dependencies:** `fastapi`, `uvicorn`, `sqlalchemy`, `pydantic`, `pytest`, `httpx`

#### Database Models (`models.py`)
Create two tables with a bidirectional one-to-many relationship:
1. **`gym_branches` (Branch)**
   - `id`: Integer, primary key, auto-generated
   - `name`: Non-empty String
   - `city`: Non-empty String
2. **`membership_plans` (MembershipPlan)**
   - `id`: Integer, primary key, auto-generated
   - `name`: Non-empty String
   - `duration_months`: Integer (minimum $1$)
   - `monthly_fee`: Integer (minimum $300$)
   - `guest_passes`: Integer (minimum $0$)
   - `branch_id`: Integer, Foreign Key referencing `gym_branches.id` (NOT NULL)

#### Pydantic Schemas (`schemas.py`)
- **`BranchCreate`:** `name` (non-empty string), `city` (non-empty string)
- **`BranchOut`:** `id`, `name`, `city`
- **`BranchWithPlans`:** `id`, `name`, `city`, `membership_plans` (list of `MembershipPlanOut`)
- **`MembershipPlanCreate`:** `name` (non-empty string), `duration_months` ($\text{int} \ge 1$), `monthly_fee` ($\text{int} \ge 300$), `guest_passes` ($\text{int} \ge 0$). *(Used for both create and update).*
- **`MembershipPlanOut`:** `id`, `name`, `duration_months`, `monthly_fee`, `guest_passes` *(omit `branch_id` from the flat child response)*

#### Required Endpoints (`main.py`)

| Method & Path | Expected Behavior | Success Status |
|---|---|---|
| `POST /branches` | Create a branch; return its saved record including generated ID. | `201` |
| `POST /branches/{parent_id}/membership_plans` | Create a membership plan under the specified branch. Return `404` if the branch does not exist. | `201` |
| `GET /branches/{parent_id}` | Return branch details with nested `membership_plans`. Optional `duration_months` query filter uses exact match. Optional `sort` accepts `name` or `monthly_fee` and sorts ascending. | `200` |
| `PUT /branches/{parent_id}/membership_plans/{child_id}` | Fully update the plan fields. Do not move it to another branch. Return `404` if the branch is missing, plan is missing, or plan belongs to another branch. | `200` |

#### Validation & Error Rules
- **HTTP 422:** Empty/whitespace required strings, missing required body fields, invalid types (strict integer validation: booleans and numeric strings are rejected), `duration_months` $< 1$, `monthly_fee` $< 300$, or `guest_passes` $< 0$.
- **HTTP 404:**
  - Requested parent branch does not exist.
  - During `PUT`, child plan does not exist or belongs to another branch.
  - Unsupported `sort` query parameter supplied (anything other than `name` or `monthly_fee`).
- **Query Filters & Sorting:**
  - If `duration_months` filter is missing or blank, treat it as no filter.
  - Supported sort fields are ascending, with `id` ascending as tie-breaker. Without sort, plans are ordered by `id` ascending.
  - A branch with zero plans returns an empty list for `membership_plans`.
- **Server Startup:** If run directly, `main.py` starts `uvicorn` on host `0.0.0.0` and port `8080`. Importing `main.py` must not start the server.

#### Example Request Bodies
```json
// Create Branch
{
  "name": "Central Fitness",
  "city": "Bhubaneswar"
}

// Create Membership Plan
{
  "name": "Monthly Flex",
  "duration_months": 1,
  "monthly_fee": 900,
  "guest_passes": 1
}
```

---

### 2.2 Farm and Crop Batches API

#### Problem Statement
An agricultural organization manages farms and crop batches assigned to each farm. Staff register farms, add crop batches, retrieve a farm with its batches, optionally filter by crop type, sort by batch name or expected yield, and update batch details without moving a batch to another farm.

#### Project Structure & Dependencies
```text
Project/
├── database.py
├── models.py
├── schemas.py
├── main.py
├── requirements.txt
└── tests.py
```
- **SQLite Database:** `farm_batches.db`
- **Dependencies:** `fastapi`, `uvicorn`, `sqlalchemy`, `pydantic`, `pytest`, `httpx`

#### Database Models (`models.py`)
Create two tables with a bidirectional one-to-many relationship:
1. **`farms` (Farm)**
   - `id`: Integer, primary key, auto-generated
   - `name`: Non-empty String
   - `region`: Non-empty String
2. **`crop_batches` (CropBatch)**
   - `id`: Integer, primary key, auto-generated
   - `batch_name`: Non-empty String
   - `crop_type`: Non-empty String
   - `expected_yield_kg`: Integer (minimum $0$)
   - `area_hectares`: Integer (minimum $1$)
   - `farm_id`: Integer, Foreign Key referencing `farms.id` (NOT NULL)

#### Pydantic Schemas (`schemas.py`)
- **`FarmCreate`:** `name` (non-empty string), `region` (non-empty string)
- **`FarmOut`:** `id`, `name`, `region`
- **`FarmWithChildren`:** `id`, `name`, `region`, `crop_batches` (list of `CropBatchOut`)
- **`CropBatchCreate`:** `batch_name` (non-empty string), `crop_type` (non-empty string), `expected_yield_kg` ($\text{int} \ge 0$), `area_hectares` ($\text{int} \ge 1$). *(Used for both create and update).*
- **`CropBatchOut`:** `id`, `batch_name`, `crop_type`, `expected_yield_kg`, `area_hectares` *(omit `farm_id` from the flat child response)*

#### Required Endpoints (`main.py`)

| Method & Path | Expected Behavior | Success Status |
|---|---|---|
| `POST /farms` | Create a parent farm; return its saved record including generated ID. | `201` |
| `POST /farms/{parent_id}/crop_batches` | Create a crop batch under the specified farm. Return `404` if parent does not exist. | `201` |
| `GET /farms/{parent_id}` | Return farm details with nested `crop_batches`. Optional `crop_type` query filter uses exact match. Optional `sort` accepts `batch_name` or `expected_yield_kg` and sorts ascending. | `200` |
| `PUT /farms/{parent_id}/crop_batches/{child_id}` | Update the child fields. Do not move it to another parent. Return `404` if parent is missing, child is missing, or child belongs to another parent. | `200` |

#### Validation & Error Rules
- **HTTP 422:** Empty/whitespace required strings, missing required body fields, invalid types (strict integer validation: booleans and numeric strings are rejected), `expected_yield_kg` $< 0$, or `area_hectares` $< 1$.
- **HTTP 404:**
  - Requested parent farm does not exist.
  - During `PUT`, child crop batch does not exist or belongs to another farm.
  - Unsupported `sort` query parameter supplied (anything other than `batch_name` or `expected_yield_kg`).
- **Query Filters & Sorting:**
  - If `crop_type` filter is missing or blank, treat it as no filter.
  - Supported sort fields are ascending, with `id` ascending as tie-breaker. Without sort, child rows are ordered by `id` ascending.
  - A farm with zero batches returns an empty list for `crop_batches`.
- **Server Startup:** If run directly, `main.py` starts `uvicorn` on host `0.0.0.0` and port `8080`. Importing `main.py` must not start the server.

#### Example Request Bodies
```json
// Create Farm
{
  "name": "Green Valley Farm",
  "region": "North"
}

// Create Crop Batch
{
  "batch_name": "Wheat-A",
  "crop_type": "Wheat",
  "expected_yield_kg": 2400,
  "area_hectares": 4
}
```

---

### 2.3 Consultant and Practice Area API [Completed]

#### Problem Statement
A consulting organization manages practice areas and the consultants assigned to them. Administrators create practice areas, add consultants, retrieve a practice area with its consultants, and update a consultant's details. Every consultant belongs to exactly one practice area.

#### Project Structure & Dependencies
```text
Project/
├── database.py
├── models.py
├── schemas.py
├── main.py
├── requirements.txt
└── tests.py
```
- **SQLite Database:** `consulting.db`
- **Dependencies:** `fastapi`, `uvicorn`, `sqlalchemy`, `pydantic`, `pytest`, `httpx`

#### Database Models (`models.py`)
Create two tables with a bidirectional one-to-many relationship:
1. **`practice_areas` (PracticeArea)**
   - `id`: Integer, primary key, auto-generated
   - `name`: String
   - `floor_number`: Integer (minimum $1$)
2. **`consultants` (Consultant)**
   - `id`: Integer, primary key, auto-generated
   - `name`: String
   - `designation`: String
   - `consultation_fee`: Integer (minimum $300$)
   - `experience_years`: Integer (minimum $0$)
   - `practicearea_id`: Integer, Foreign Key referencing `practice_areas.id`

#### Pydantic Schemas (`schemas.py`)
- **`PracticeAreaCreate`:** `name` (non-empty string), `floor_number` ($\text{int} \ge 1$)
- **`PracticeAreaOut`:** `id`, `name`, `floor_number`
- **`PracticeAreaWithConsultants`:** `id`, `name`, `floor_number`, `consultants` (list of `ConsultantOut`)
- **`ConsultantCreate`:** `name` (non-empty string), `designation` (non-empty string), `consultation_fee` ($\text{int} \ge 300$), `experience_years` ($\text{int} \ge 0$). *(Used for both create and update).*
- **`ConsultantOut`:** `id`, `name`, `designation`, `consultation_fee`, `experience_years`

#### Required Endpoints (`main.py`)

| Method & Path | Expected Behavior | Success Status |
|---|---|---|
| `POST /practice-areas` | Create a Practice Area; return its saved record including generated ID. | `201` |
| `POST /practice-areas/{parent_id}/consultants` | Create a Consultant under the specified parent. Return `404` if parent does not exist. | `201` |
| `GET /practice-areas/{parent_id}` | Return parent details with nested consultants. Optional `designation` query filter uses exact match. Optional `sort` query accepts `name` or `consultation_fee` and sorts ascending. | `200` |
| `PUT /practice-areas/{parent_id}/consultants/{child_id}` | Update the child's `name`, `designation`, `consultation_fee`, and `experience_years`. Do not move it to another parent. Return `404` if parent is missing, child is missing, or child belongs to another parent. | `200` |

#### Validation & Error Rules
- **HTTP 422:** Empty required `name`/`designation`, missing required body field, invalid type, `floor_number` $< 1$, `consultation_fee` $< 300$, or `experience_years` $< 0$.
- **HTTP 404:**
  - Requested parent does not exist.
  - During `PUT`, child does not exist or is owned by a different parent.
  - Invalid `sort` parameter supplied (anything other than `name` or `consultation_fee`). Return concise error details; do not silently fall back.
- **Query Filters:** If `designation` filter is missing or blank, treat it as no filter.

#### Example Request Bodies
```json
// Create Practice Area
{
  "name": "Data Engineering",
  "floor_number": 3
}

// Create Consultant
{
  "name": "Alex Morgan",
  "designation": "Senior",
  "consultation_fee": 800,
  "experience_years": 8
}
```

---

### 2.4 Trainer and Skill Group API [Completed]

#### Problem Statement
A learning company manages skill groups and the trainers assigned to them. Administrators create skill groups, add trainers, retrieve a skill group with its trainers, and update trainer details. Every trainer belongs to one skill group.

#### Project Structure & Dependencies
```text
Project/
├── database.py
├── models.py
├── schemas.py
├── main.py
├── requirements.txt
└── tests.py
```
- **SQLite Database:** `learning.db`
- **Dependencies:** `fastapi`, `uvicorn`, `sqlalchemy`, `pydantic`, `pytest`, `httpx`

#### Database Models (`models.py`)
Create two tables with a bidirectional one-to-many relationship:
1. **`skill_groups` (SkillGroup)**
   - `id`: Integer, primary key, auto-generated
   - `name`: String
   - `floor_number`: Integer (minimum $1$)
2. **`trainers` (Trainer)**
   - `id`: Integer, primary key, auto-generated
   - `name`: String
   - `designation`: String
   - `session_fee`: Integer (minimum $300$)
   - `experience_years`: Integer (minimum $0$)
   - `skillgroup_id`: Integer, Foreign Key referencing `skill_groups.id`

#### Pydantic Schemas (`schemas.py`)
- **`SkillGroupCreate`:** `name` (non-empty string), `floor_number` ($\text{int} \ge 1$)
- **`SkillGroupOut`:** `id`, `name`, `floor_number`
- **`SkillGroupWithTrainers`:** `id`, `name`, `floor_number`, `trainers` (list of `TrainerOut`)
- **`TrainerCreate`:** `name` (non-empty string), `designation` (non-empty string), `session_fee` ($\text{int} \ge 300$), `experience_years` ($\text{int} \ge 0$). *(Used for both create and update).*
- **`TrainerOut`:** `id`, `name`, `designation`, `session_fee`, `experience_years`

#### Required Endpoints (`main.py`)

| Method & Path | Expected Behavior | Success Status |
|---|---|---|
| `POST /skill-groups` | Create a Skill Group; return its saved record including generated ID. | `201` |
| `POST /skill-groups/{parent_id}/trainers` | Create a Trainer under the specified parent. Return `404` if parent does not exist. | `201` |
| `GET /skill-groups/{parent_id}` | Return parent details with nested trainers. Optional `designation` query filter uses exact match. Optional `sort` query accepts `name` or `session_fee` and sorts ascending. | `200` |
| `PUT /skill-groups/{parent_id}/trainers/{child_id}` | Update the child's `name`, `designation`, `session_fee`, and `experience_years`. Do not move it to another parent. Return `404` if parent is missing, child is missing, or child belongs to another parent. | `200` |

#### Validation & Error Rules
- **HTTP 422:** Empty required `name`/`designation`, missing required body field, invalid type, `floor_number` $< 1$, `session_fee` $< 300$, or `experience_years` $< 0$.
- **HTTP 404:**
  - Requested parent does not exist.
  - During `PUT`, child does not exist or is owned by a different parent.
  - Invalid `sort` parameter supplied (anything other than `name` or `session_fee`).
- **Server Startup:** Use `if __name__ == "__main__":` to run `uvicorn` on host `0.0.0.0` and port `8080`. Importing `main.py` must not start the server.

#### Example Request Bodies
```json
// Create Skill Group
{
  "name": "Cloud Computing",
  "floor_number": 3
}

// Create Trainer
{
  "name": "Alex Morgan",
  "designation": "Senior",
  "session_fee": 800,
  "experience_years": 8
}
```

---

## Appendix: Setup, Commands & Readiness Checklists

### 1. Setup & Run Commands

#### Pandas Exercises
```bash
python -m pip install pandas pytest
python main.py
pytest -q
```

#### FastAPI Exercises
```bash
python -m pip install fastapi uvicorn sqlalchemy pydantic pytest httpx
python main.py
# Or run via uvicorn CLI:
uvicorn main:app --host 0.0.0.0 --port 8080
pytest -q
```

---

## Old Syllabus

### NumPy

#### 1. E-Commerce Daily Order Analysis (NumPy)

##### Problem Statement
An e-commerce analytics team tracks the number of orders received by an online store each day. Each value in a NumPy array represents the number of orders received on a specific day. Your task is to build NumPy-based functions that can:
- Create an orders array
- Validate the orders array
- Compute order metrics
- Categorize order-volume levels
- Find the longest growth streak
- Format order counts for reports

All functions must use NumPy arrays as input/output wherever applicable.

##### Function Rules & Concepts Tested
- **Rules:** Function-based (do not create a class), implement at module level, use exact function names/parameters, return NumPy arrays where expected, do **not** use Pandas.
- **Concepts:** NumPy array creation, array validation, numeric aggregation, conditional labeling, trend/growth analysis, formatting numeric values.

##### Operations

###### 1. Create Orders Array
Creates a NumPy array from daily e-commerce order counts.

```python
def create_orders_array(orders_data: list) -> np.ndarray:
```

- **Example Input:** `create_orders_array([120, 360, 190, 540, 780])`
- **Expected Output:** `np.array([120, 360, 190, 540, 780])`
- **Implementation Flow:**
  - Convert list to NumPy array with `int64` type.
  - Return the resulting array.

###### 2. Validate Orders Array
Checks whether the orders array contains valid non-negative numeric values.

```python
def validate_orders_array(orders_array: np.ndarray) -> bool:
```

- **Example Input:** `validate_orders_array(np.array([150, 360, -280, 550]))`
- **Expected Output:** `False`
- **Implementation Flow:**
  - Check that the array is not empty.
  - Check that the array data type is numeric.
  - Check that all values are $\ge 0$.
  - Return `True` if all conditions pass, otherwise return `False`.

###### 3. Compute Order Metrics
Returns total orders, average orders, and maximum orders.

```python
def compute_order_metrics(orders_array: np.ndarray) -> tuple:
```

- **Example Input:** `compute_order_metrics(np.array([120, 360, 190, 540, 780]))`
- **Expected Output:** `(1990, 398.0, 780)`
- **Implementation Flow:**
  - Calculate Total, Average, and Maximum for the given input array.
  - Convert total and maximum values to `int`.
  - Round average to 2 decimal places.
  - Return a tuple `(total, average, maximum)`.

###### 4. Categorize Order Volume Levels
Labels each day’s order count as `"Low Volume"`, `"Moderate Volume"`, or `"High Volume"`.

```python
def categorize_order_levels(orders_array: np.ndarray) -> np.ndarray:
```

- **Example Input:** `categorize_order_levels(np.array([120, 360, 190, 540, 780]))`
- **Expected Output:** `np.array(["Low Volume", "Moderate Volume", "Low Volume", "High Volume", "High Volume"])`
- **Implementation Flow:**
  - Orders $< 300 \rightarrow$ `"Low Volume"`
  - Orders $300$ to $499 \rightarrow$ `"Moderate Volume"`
  - Orders $\ge 500 \rightarrow$ `"High Volume"`
  - Return a NumPy array of order-volume labels.

###### 5. Find Longest Growth Streak
Finds the longest sequence of consecutive days where orders increased compared to the previous day.

```python
def longest_order_growth_streak(orders_array: np.ndarray) -> int:
```

- **Example Input:** `longest_order_growth_streak(np.array([150, 120, 280, 290, 320, 120, 560]))`
- **Expected Output:** `3`
- **Implementation Flow:**
  - Declare two variables to track `max_streak` and `current_streak`.
  - Use a `for` loop to iterate over the array. When the current value is greater than the earlier value, increase `current_streak` by 1.
  - If `max_streak` is less than `current_streak`, update `max_streak`.
  - Else set `current_streak` to 1.
  - Return `max_streak`.

###### 6. Format Order Counts
Formats order counts with comma separators for reporting.

```python
def format_order_counts(orders_array: np.ndarray) -> np.ndarray:
```

- **Example Input:** `format_order_counts(np.array([5200, 55000, 3700000]))`
- **Expected Output:** `np.array(["5,200", "55,000", "3,700,000"])`
- **Implementation Flow:**
  - Convert each order count into a formatted string using comma separators.
  - Return the formatted values as a NumPy array.

---

#### 2. Fitness Tracker Analyzer (NumPy)

##### Problem Statement
Develop a Python program named `FitnessTrackerAnalyzer` to analyze fitness readings using the NumPy library. 

##### Requirements & Workflow
1. **Input & Conversion:** Accept a list of fitness readings and convert them into a NumPy array of floating-point numbers.
2. **Validation:** Validate the readings to ensure the array is not empty and all values are positive ($> 0$).
3. **Statistical Analysis:** Calculate the total, average (rounded to 1 decimal place), and maximum fitness reading.
4. **High-Intensity Adjustment:** Identify and adjust high-intensity readings by reducing values $\ge 50.0$ by $10\%$.
5. **Activity Classification:** Classify each reading as `"High"` if it exceeds the average reading, and `"Normal"` otherwise.
6. **Formatting:** Format all readings to two decimal places followed by the unit `"bpm"`.

##### Sample Output (for a given sample input `[72, 85, 120, 145, 90]`)
```text
(512.0, 102.4, 145.0)
[ 72.   85.  108.  130.5  90. ]
['Normal' 'Normal' 'High' 'High' 'Normal']
['72.00 bpm' '85.00 bpm' '120.00 bpm' '145.00 bpm' '90.00 bpm']
```

---

#### 3. Movie Rating Analyzer (NumPy)

##### Problem Statement
A streaming platform tracks movie ratings using NumPy arrays, where each value represents a viewer rating (out of 100). Implement a system that processes this data, validates it, performs aggregations, applies a bonus, and categorizes movies based on their ratings.

##### Class Definition
```python
class MovieRatingAnalyzer:
```

##### Operations

###### 1. Create a Rating Array
Creates a NumPy array from a list of movie rating scores.

```python
def create_rating_array(self, ratings_array: list) -> np.ndarray:
```

- **Example Input:** `create_rating_array([85, 90, 78, 92, 88])`
- **Expected Output:** `np.array([85, 90, 78, 92, 88])`
- **Implementation Flow:** Convert the input list to a NumPy array of integer type and return it.

###### 2. Validate Ratings
Checks if the rating array is valid: numeric and in the range $0\text{--}100$.

```python
def validate_ratings(self, rating_array: np.ndarray) -> bool:
```

- **Example Input:** `validate_ratings(np.array([85, 90, -78, 92, 88]))`
- **Expected Output:** `False`
- **Implementation Flow:**
  - Check for non-empty array; return `False` if empty.
  - Ensure all values are between $0$ and $100$ (inclusive); return `False` if any value is outside the range (`np.any`).
  - Return `True`.

###### 3. Compute Rating Summary
Returns total, average, and highest rating.

```python
def compute_rating_summary(self, rating_array: np.ndarray) -> tuple:
```

- **Example Input:** `compute_rating_summary(np.array([85, 90, 78, 92, 88]))`
- **Expected Output:** `(433, 86.6, 92)`
- **Implementation Flow:**
  - Convert input to a NumPy array of numeric type.
  - Compute Total = sum of all ratings.
  - Compute Average rounded to 1 decimal place.
  - Compute Maximum value.

###### 4. Apply Bonus
Adds a $5\%$ bonus to ratings above $85$, without exceeding $100$.

```python
def apply_bonus(self, rating_array: np.ndarray) -> np.ndarray:
```

- **Example Input:** `apply_bonus(np.array([85, 90, 78, 92, 88]))`
- **Expected Output:** `np.array([85.0, 94.5, 78.0, 96.6, 92.4])`
- **Implementation Flow:**
  - Convert all elements to `float` datatype.
  - Identify ratings $> 85$ and increase them by $5\%$.
  - Clip values to a maximum of $100$.
  - Round results to 1 decimal place and return the updated array.

###### 5. Categorize Movies
Labels movies based on rating thresholds.

```python
def categorize_movies(self, rating_array: np.ndarray) -> np.ndarray:
```

- **Example Input:** `categorize_movies(np.array([85, 90, 78, 92, 88]))`
- **Expected Output:** `np.array(["Good", "Excellent", "Needs Improvement", "Excellent", "Good"])`
- **Implementation Flow:**
  - Thresholds: $\ge 90 \rightarrow$ `"Excellent"`, $80\text{--}89 \rightarrow$ `"Good"`, $< 80 \rightarrow$ `"Needs Improvement"`.
  - Return the categorized result as a string array.

###### 6. Format Ratings with Grade Notation
Returns grades as letters: A/B/C/D based on numeric ratings.

```python
def format_ratings_with_grades(self, rating_array: np.ndarray) -> np.ndarray:
```

- **Example Input:** `format_ratings_with_grades(np.array([85, 90, 78, 92, 88]))`
- **Expected Output:** `np.array(["B", "A", "C", "A", "B"])`
- **Implementation Flow:**
  - Declare an empty list and use a `for` loop to iterate over input and apply conditions.
  - Map ratings: $\ge 90 \rightarrow$ `"A"`, $80\text{--}89 \rightarrow$ `"B"`, $70\text{--}79 \rightarrow$ `"C"`, $< 70 \rightarrow$ `"D"`.
  - Return grade labels as a string array.

---

### Pandas

#### 1. Food Delivery Order Analyzer (Pandas)

##### Problem Statement
A food-delivery analytics platform is analyzing delivery performance. You are provided with two datasets:
- **Delivery Log:** `OrderID`, `RestaurantCode`, `Area`, `DeliveryTime` (in minutes)
- **Restaurant Master:** `RestaurantCode`, `RestaurantName`

Your task is to analyze delivery patterns using Pandas — including merging data, calculating average delivery times, identifying frequent delays, and filtering critical areas.

##### Class Definition
```python
class DeliveryTimeAnalyzer:
```

##### Operations

###### 1. Create Delivery Log DataFrame
Creates a DataFrame from raw delivery-time records.

```python
def create_delivery_log_df(self, delivery_log: list) -> pd.DataFrame:
```

- **Example Input:**

  ```python
  create_delivery_log_df([
      [301, "RF", "Andheri-Mumbai", 30],
      [302, "TB", "Bandra-Mumbai", 60],
      [303, "RF", "Andheri-Mumbai", 10]
  ])
  ```
  
- **Expected Output:**
  | | OrderID | RestaurantCode | Area | DeliveryTime |
  |---|---|---|---|---|
  | 0 | 301 | RF | Andheri-Mumbai | 30 |
  | 1 | 302 | TB | Bandra-Mumbai | 60 |
  | 2 | 303 | RF | Andheri-Mumbai | 10 |
- **Implementation Flow:** Create a DataFrame with columns `["OrderID", "RestaurantCode", "Area", "DeliveryTime"]`.

###### 2. Create Restaurant Master DataFrame
Creates a DataFrame from master restaurant details.

```python
def create_restaurant_master_df(self, restaurant_master: list) -> pd.DataFrame:
```

- **Example Input:**

  ```python
  create_restaurant_master_df([
      ["RF", "Royal Foods"],
      ["TB", "Tasty Bites"]
  ])
  ```
- **Expected Output:**
  | | RestaurantCode | RestaurantName |
  |---|---|---|
  | 0 | RF | Royal Foods |
  | 1 | TB | Tasty Bites |
- **Implementation Flow:** Create a DataFrame with columns `["RestaurantCode", "RestaurantName"]`.

###### 3. Merge Restaurant Names into Delivery Log
Returns a DataFrame by merging delivery log with restaurant master.

```python
def merge_restaurant_names(self, delivery_log_df: pd.DataFrame, restaurant_master_df: pd.DataFrame) -> pd.DataFrame:
```

- **Example Input:** `merge_restaurant_names(delivery_df, restaurant_df)`
- **Expected Output:**
  | | OrderID | RestaurantCode | Area | DeliveryTime | RestaurantName |
  |---|---|---|---|---|---|
  | 0 | 301 | RF | Andheri-Mumbai | 30 | Royal Foods |
  | 1 | 302 | TB | Bandra-Mumbai | 60 | Tasty Bites |
  | 2 | 303 | RF | Andheri-Mumbai | 10 | Royal Foods |
- **Implementation Flow:** Join both input DataFrames using a `left` join on `RestaurantCode`.

###### 4. Calculate Average Delivery Time per Restaurant
Returns average delivery time per restaurant.

```python
def average_delivery_by_restaurant(self, merged_df: pd.DataFrame) -> pd.DataFrame:
```

- **Example Input:** `average_delivery_by_restaurant(merged_df)`
- **Expected Output:**
  | | RestaurantName | Average Delivery |
  |---|---|---|
  | 0 | Royal Foods | 20.0 |
  | 1 | Tasty Bites | 60.0 |
- **Implementation Flow:** Group by `"RestaurantName"` and calculate the mean of `"DeliveryTime"`. Use `.reset_index()` and rename the result column to `"Average Delivery"`.

###### 5. Filter Deliveries Above Threshold
Returns all deliveries where delivery time exceeds a given threshold.

```python
def filter_slow_deliveries(self, delivery_log_df: pd.DataFrame, threshold: int) -> pd.DataFrame:
```

- **Example Input:** `filter_slow_deliveries(delivery_log_df, 40)`
- **Expected Output:**
  | | OrderID | RestaurantCode | Area | DeliveryTime |
  |---|---|---|---|---|
  | 1 | 302 | TB | Bandra-Mumbai | 60 |

###### 6. Identify Slowest Delivery Area
Returns a single-row DataFrame with the area having the highest average delivery time.

```python
def slowest_delivery_area(self, delivery_log_df: pd.DataFrame) -> pd.DataFrame:
```

- **Example Input:** `slowest_delivery_area(delivery_log_df)`
- **Expected Output:**
  | | Area | Average Delivery |
  |---|---|---|
  | 0 | Bandra-Mumbai | 60.0 |
- **Implementation Flow:**
  - Group by `"Area"` and compute average delivery time (rename column to `"Average Delivery"`).
  - Find the maximum value from the average delivery column.
  - Filter the DataFrame where `Average Delivery == max_delay_value`.
  - Sort descending, use `.head(1)`, and apply `.reset_index(drop=True)`.

---

### OOPs & Python Data Structures

#### 1. Vehicle Service Tracker (Dictionary & Class)

##### Problem Statement
A Vehicle Service Tracker monitors customers' vehicles, tracks completed service visits, and records the total service amount spent. Each customer record is stored in a dictionary:
- **Key:** Customer Name
- **Value:** Dictionary containing:
  - `"services"` $\rightarrow$ Number of completed service visits
  - `"amount"` $\rightarrow$ Total service amount paid
  - `"status"` $\rightarrow$ `"Regular"` if services exceed 5, otherwise `"New"`

##### Class Definition
```python
class VehicleServiceTracker:
    def __init__(self):
        pass
```

##### Operations

###### 1. Register a New Customer
Adds a new customer to the system with an empty service history.

```python
def register_customer(self, service_data: dict, customer_name: str) -> dict:
```

- **Example Input:** `register_customer({}, "Arjun")`
- **Expected Output:** `{'Arjun': {'services': 0, 'amount': 0, 'status': 'New'}}`
- **Implementation Flow:**
  - Add a new entry with initial values: `services: 0`, `amount: 0`, `status: 'New'`.
  - Return the updated dictionary.

###### 2. Log a Service Visit
Updates the customer’s service count and amount paid. If services exceed 5, the `"status"` changes to `"Regular"`.

```python
def log_service(self, service_data: dict, customer_name: str, amount_paid: int) -> dict:
```

- **Example Input:** `log_service({'Arjun': {'services': 2, 'amount': 5000, 'status': 'New'}}, "Arjun", 3000)`
- **Expected Output:** `{'Arjun': {'services': 3, 'amount': 8000, 'status': 'New'}}`
- **Implementation Flow:**
  - Check if the customer exists; if not, raise `KeyError("Error: Customer not found")`.
  - Increase `"services"` count by 1 and add `amount_paid` to `"amount"`.
  - If services $> 5$, update `"status"` to `"Regular"`.
  - Return the updated dictionary.

###### 3. Calculate Average Service Amount
Computes the average amount paid per service visit for a given customer.

```python
def calculate_average_amount(self, service_data: dict, customer_name: str) -> float:
```

- **Example Input:** `calculate_average_amount({'Arjun': {'services': 3, 'amount': 8000, 'status': 'New'}}, "Arjun")`
- **Expected Output:** `2666.67`
- **Implementation Flow:**
  - If customer does not exist or service count is $0$, raise `KeyError("Error: Invalid customer or no services")`.
  - Calculate average as `total amount / services`.
  - Return the average.

###### 4. Generate Service Report
Returns a report categorizing customers as `"Basic"`, `"Regular"`, or `"Premium"` based on total amount paid.

```python
def generate_service_report(self, service_data: dict) -> dict:
```

- **Criteria:**
  - $< 10000 \rightarrow$ `"Basic"`
  - $10000 \text{ to } 50000 \text{ (exclusive of } 50000\text{)} \rightarrow$ `"Regular"`
  - $\ge 50000 \rightarrow$ `"Premium"`
- **Example Input:** `{'Arjun': {'services': 3, 'amount': 8000, 'status': 'New'}, 'Neha': {'services': 10, 'amount': 45000, 'status': 'Regular'}}`
- **Expected Output:** `{'Arjun': 'Basic', 'Neha': 'Regular'}`

---

#### 2. Library Inventory Management System (Dictionary & Class)

##### Problem Statement
The Library Inventory System keeps track of book copies and supports adding books, updating available copies, retrieving book details, and getting a list of available books. Each book is stored in a dictionary where:
- **Key:** Book title
- **Value:** Available copy quantity

##### Class Definition
```python
class LibraryInventorySystem:
```

##### Operations

###### 1. Add a New Book
Adds a book to the library with its available copy quantity. *(Note: If the test case of this function fails, all test cases will fail).*

```python
def add_book(self, inventory: dict, book_title: str, quantity: int) -> dict:
```

- **Example Input:** `add_book({}, "Python Basics", 10)`
- **Expected Output:** `{'Python Basics': 10}`
- **Implementation Flow:**
  - Check if the book already exists; if so, increase the quantity.
  - Otherwise, add the book to the dictionary.
  - Return the updated dictionary.

###### 2. Update Book Quantity
Updates the available copy quantity of an existing book.

```python
def update_book_quantity(self, inventory: dict, book_title: str, new_quantity: int) -> dict:
```

- **Example Input:** `update_book_quantity({"Python Basics": 10}, "Python Basics", 15)`
- **Expected Output:** `{'Python Basics': 15}`
- **Implementation Flow:**
  - Check if the book exists; if not, raise `KeyError("Not found")`.
  - Update the book's available quantity and return the updated dictionary.

###### 3. Retrieve Book Details
Fetches the available copy quantity of a specific book.

```python
def get_book_stock(self, inventory: dict, book_title: str) -> int:
```

- **Example Input:** `get_book_stock({"Python Basics": 15}, "Python Basics")`
- **Expected Output:** `15`
- **Implementation Flow:**
  - Check if the book exists; if not, raise `KeyError("Not found")`.
  - Retrieve and return the available copy quantity.

###### 4. Get List of Available Books
Returns a list of books that have copies available.

```python
def get_available_books(self, inventory: dict) -> list:
```

- **Example Input:** `get_available_books({"Python Basics": 15, "SQL Basics": 0, "Machine Learning": 5})`
- **Expected Output:** `['Python Basics', 'Machine Learning']`
- **Implementation Flow:**
  - Iterate over the dictionary using an explicit loop (do **not** use one-line list comprehensions).
  - Check each book's stock value; if $\text{stock} > 0$, add the book to a result list.
  - Return the final list of available books.
