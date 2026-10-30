# Zephra — A Conbuild Insight

Zephra is a local construction-project demonstration with three separate workspaces:

1. **BIM site twin** (`/bim`) — an interactive, phased 3D concept from site works and excavation through foundations, structure, MEP, and handover. Its two-storey house has rendered plain walls, cutaway views, room-separating partitions, staircases, living/dining rooms, a larger fitted kitchen, bedrooms, bathrooms, fixtures, entry steps, a railed balcony, pitched roof, solar panels, and landscaping. Color-coded cold/hot-water supplies, soil/waste stacks, drains, cleanouts, kitchen/bathroom branches routed along perimeter service zones, supported ceiling-perimeter conduits, lights, outlets, switches, meter, and distribution panel can be isolated by layer. Furnishings and kitchen fit-out are a separate layer and appear at handover. The drone/PTZ motion is simulated.
2. **Worker safety** (`/safety`) — the trained YOLO PPE image detector, with annotated results and confidence scores.
3. **Tender risk** (`/tender-risk`) — a transparent early-warning screen using current cost, earned-value, schedule, progress, payment, cash-flow, contractor, staffing, materials, and site-readiness inputs.

The BIM model is illustrative: it is not a surveyed or approved building-information model and is not connected to a live drone, PTZ camera, sensor, schedule, or common data environment (CDE). The progress feed intentionally says **Not connected** rather than presenting made-up project measurements.

## Requirements

- Python 3.10 or later.
- Internet access in the browser to load Three.js for the BIM viewer.
- The project model files in `models/`.

## Run the project

Run these commands from the project directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

Open [http://127.0.0.1:5050](http://127.0.0.1:5050) and choose a workspace:

- **BIM site twin** — open the construction-stage viewer; choose a phase, toggle model layers, and start the simulated PTZ sweep. Switch off **Walls & openings** to inspect the room interiors; **Interiors** controls partitions, floor finishes, and stairs, while **Furnishings** controls furniture and the kitchen fit-out. Choose **MEP & openings** to inspect open-room service rough-ins; choose **Finishes** to add the envelope, glazing, kitchen, and room furnishings for the handover concept.
- **Worker safety** — upload a JPG, PNG, or WEBP site image (up to 10 MB) and run PPE detection.
- **Tender risk** — submit a project snapshot to see rule-by-rule review signals.

Press `Ctrl+C` in the terminal to stop the server. On a later run, reactivate the environment first:

```bash
source .venv/bin/activate
python app.py
```

## BIM construction phases

The phase selector changes the visible model layers to illustrate a build-up toward handover:

1. **Site overview** — the complete furnished concept and all systems.
2. **Excavation** — the below-grade excavation and temporary access.
3. **Basement & foundations** — the basement structure, below-grade drainage, and water entry.
4. **Frame & structural slabs** — the concrete frame, slabs, interior room layout, and stairs before fit-out.
5. **MEP coordination & rough-in** — connected plumbing, drainage, and electrical routes in an open, unfurnished model.
6. **Finishes & handover** — rendered envelope and windows, then the fitted kitchen and furnished rooms.

The stage checklist and progress feed are demonstration labels only; they are not connected to a schedule, inspection record, site feed, or approved BIM/CDE.

## PPE classes

The trained detector recognizes these 10 classes:

1. Hardhat
2. Mask
3. NO-Hardhat
4. NO-Mask
5. NO-Safety Vest
6. Person
7. Safety Cone
8. Safety Vest
9. machinery
10. vehicle

### PPE detector and dataset

The safety page loads `models/best.pt` with Ultralytics and runs object detection on each uploaded image. The loaded checkpoint is a YOLO-family `detect` model with a C2f/SPPF backbone; detections are returned as bounding boxes, class labels, and confidence scores, then drawn with Ultralytics' plot helper and saved by OpenCV. The app does not set a project-specific confidence threshold. This image detector is separate from the tender-risk screen.

The dataset metadata in `data/` identifies Roboflow Universe's **Construction Site Safety v28** export (CC BY 4.0), with 2,801 images reported by its dataset README. That README says images were resized to 640×640 and five augmented versions were created using horizontal flips, crops, rotations, shear, brightness/exposure, and blur. `data/data.yaml` lists the train/validation/test paths and the 10 classes above. In this checkout, those image directories are not present; `data/` has metadata/configuration files only. The checkpoint can run inference without the training images, but the training run cannot be reproduced from the current files: no training command, split counts, or validation metrics are supplied. Check the dataset's source and license before reusing its material.

## Tender risk screen: what it measures

The risk workspace is an **explainable, illustrative screening checklist**, not a trained machine-learning model and not a prediction that a project will or will not be abandoned. It reports its input, rule, and explanation. Its point total is an uncalibrated review-priority aid—not a probability or statistically validated score. The example thresholds are starting points for discussion, not universal contractual or research-validated cut-offs. Set project-specific thresholds with the owner, contractor, contract administrator, and project-controls team before operational use.

Use one reporting date and current, verifiable project records. In the form, currency is in **₹ crore**:

| Input | Useful definition | Interpretation and limitation |
|---|---|---|
| Approved budget and forecast final cost | Approved cost baseline and a documented estimate at completion | Shows forecast variance against the approved baseline; update for approved scope and contractual price adjustments. A forecast depends on the assumptions and remaining-work estimate. |
| Planned value (PV), earned value (EV), actual cost (AC) | Budgeted value of planned work, budgeted value of verified completed work, and actual cost to the same status date | The screen reports **SPI = EV / PV** and **CPI = EV / AC** where the denominators are non-zero. These require consistent scope, a dated baseline, reliable progress measurement, and cost cut-offs. They are project-control measures, not validated abandonment probabilities. |
| Planned and verified physical progress | Cumulative percent complete at the report date from the approved, dated programme and measured quantities | The gap is shown in percentage points. Do not infer planned progress from elapsed time using a straight-line assumption. |
| Planned and earned progress for the last seven days | Measured physical progress gained over the reporting week and the weekly target | A short-term trend is interpretable; investigate the affected work package and cause rather than treating one poor week as a diagnosis. |
| Certified payment overdue | Age in days of the oldest certified/approved payment still unpaid | Keep employer payment delay separate from contractor liquidity and verify dates, amounts, contract terms, and disputed sums. |
| Supplier/subcontractor arrears | Age of a reported overdue obligation, checked against dated statements | Treat unverified claims as missing information, not established adverse evidence. |
| Contractor cash-flow cover | Available project liquidity divided by forecast monthly site cash burn | A rough context measure. Validate liquidity sources and the remaining work programme; a ratio alone is not proof of insolvency or abandonment. |
| Approved change orders | Approved variation value as a share of the original approved baseline | Legitimate changes are not automatically distress. Review time impact and separate approved variations from unresolved claims and disputes. |
| Material cost exposure | Forecast, unmitigated price change for remaining measured quantities using current quotations or contract-relevant indices | Context only. Separate contractual escalation, remaining quantities, and mitigation; a broad inflation rate is not a project-specific cost forecast. |
| Performance security | Verified status and expiry of the required guarantee/bond | Check the executed contract and issuer evidence. Missing data are not the same as an adverse finding. |
| Workers present versus planned crew | Same shift, work package, trade mix, phase, and available workfront | Headcount alone is a weak proxy: the required crew changes with phase, sequencing, access, and weather. It is context—not a standalone abandonment trigger. |
| Site access and critical permits | Dated status, responsible party, and activities blocked by possession, access, utility clearances, or permits | Describe the actual blocker and affected workfront, not just an unqualified status. |

### Exact tender form inputs and validation

All 21 fields below are required by the current form. Numeric bounds are inclusive; currency fields use ₹ crore. `forecast_final_cost_crore` must also be greater than or equal to `actual_cost_crore`. The screen does not load a dataset or fit a model at runtime.

| Input name | Meaning / accepted values | Affects points? |
|---|---|---|
| `snapshot_date` | ISO calendar date, today or earlier; all measurements should share this status date | No; validated and displayed |
| `baseline_cost_crore` | Approved cost baseline; 0.01–1,000,000 | Yes |
| `forecast_final_cost_crore` | Forecast final cost; 0.01–1,000,000 | Yes |
| `planned_value_crore` | Planned value (PV); 0–1,000,000 | Yes; SPI unavailable if zero |
| `earned_value_crore` | Earned value (EV); 0–1,000,000 | Yes, through CPI and SPI |
| `actual_cost_crore` | Actual cost (AC); 0–1,000,000 | Yes; CPI unavailable if zero |
| `baseline_duration_days` | Approved duration; 1–36,500 days | No; used for displayed elapsed percentage |
| `elapsed_days` | Elapsed duration; 0–36,500 days | No; used for displayed elapsed percentage |
| `planned_progress_pct` | Cumulative planned physical progress; 0–100% | Yes |
| `actual_progress_pct` | Cumulative verified physical progress; 0–100% | Yes |
| `last_week_progress_pct` | Measured progress gained in the last seven days; 0–100 percentage points | Yes |
| `planned_weekly_progress_pct` | Planned progress per week; 0.01–100 percentage points | Yes; denominator for weekly attainment |
| `certified_payment_delay_days` | Age of oldest certified payment overdue; 0–3,650 days | Yes |
| `supplier_payment_delay_days` | Age of oldest verified supplier/subcontractor arrears; 0–3,650 days | Yes |
| `change_order_pct` | Approved change orders as a percent of baseline; 0–1,000% | Yes |
| `cashflow_coverage_months` | Available project liquidity / forecast monthly site cash burn; 0–120 months | Yes |
| `workers_present` | People present for the shift; 0–1,000,000 | Yes, relative to planned crew |
| `workers_planned` | Planned people for the same shift/work package; 1–1,000,000 | Yes, relative to present crew |
| `material_cost_exposure_pct` | Unmitigated material exposure; 0–1,000% | No; displayed as context |
| `site_readiness` | `ready`, `partial`, or `blocked` (access and critical permits) | Yes |
| `security_status` | `valid`, `expiring`, or `missing` (performance security) | No; displayed as context |

### Rule calculations and score mapping

The screen derives `forecast cost growth = (forecast final cost / baseline cost − 1) × 100`, `CPI = EV / AC`, `SPI = EV / PV`, `progress gap = planned progress − actual progress` in percentage points, `weekly attainment = last-week progress / planned weekly progress × 100`, and `staffing shortfall = max(0, 1 − workers present / workers planned) × 100`. CPI and SPI are not scored when their denominator is zero. Each applicable rule contributes once; a **high** flag adds 2 points and a **watch** flag adds 1 point:

| Indicator | High flag (2 points) | Watch flag (1 point) |
|---|---|---|
| Forecast cost growth | ≥20% | ≥10% and <20% |
| CPI and SPI, independently | <0.80 | ≥0.80 and <0.90 |
| Planned vs. actual progress gap | ≥10 percentage points | ≥5 and <10 percentage points |
| Weekly progress attainment | <50% of plan | ≥50% and <80% of plan |
| Certified payment overdue | ≥60 days | ≥30 and <60 days |
| Supplier/subcontractor arrears | ≥60 days | ≥30 and <60 days |
| Approved change orders | ≥20% of baseline | ≥10% and <20% |
| Cash-flow cover | <1 month | ≥1 and <2 months |
| Workforce shortfall | No high tier | ≥15% (including ≥30%) |
| Site access / critical permits | `blocked` | `partial` |

The total maps to **0: No prominent rule flags**, **1–2: Monitor closely**, **3–5: Elevated signals**, and **6 or more: High concern**. These point weights and cut-offs are local illustrative rules, not learned or calibrated. A result of zero does not establish that abandonment cannot occur, and a high result is not a finding that it will.

The page provides two **synthetic, editable** examples that fill and submit the form. “Steady delivery” is designed to return 0 points / No prominent rule flags. “Multiple stress signals” is designed to return 21 points / High concern. These are software demonstrations of the thresholds, not project observations, outcome labels, or predictions.

### Tender dataset status and provenance

There is **no verified, longitudinal tender-abandonment dataset used by the app**, and no tender machine-learning model has been trained. The local `tender/mock_construction_projects.csv` file has 100 rows and 25 columns, including an `Abandoned_Tender` column (90 `No`, 10 `Yes`) and `Project_Status` values (57 `Completed`, 33 `Ongoing`, 10 `Abandoned`). Its columns are `Project_ID`, `Project_Name`, `State`, `Project_Type`, `Estimated_Cost_Cr`, `Final_Cost_Cr`, `Cost_Overrun_%`, `Start_Date`, `Expected_End_Date`, `Actual_End_Date`, `Project_Status`, `Abandonment_Reason`, `Funds_Utilized_%`, `Tender_Float_Delay_Days`, `Fatal_Accidents`, `Weather_Delays_Days`, `Local_Opposition`, `Land_Acquisition_Status`, `Fund_Transparency_Score`, `Payment_Pending_Days`, `Quality_Inspection_Count`, `Project_Manager_Experience_Yrs`, `Contractor_Experience`, `Worker_Shortage`, and `Abandoned_Tender`.

The CSV uses generic project names and has no traceable source, data dictionary, label adjudication, or dated project-status snapshots. Its apparent labels and values therefore cannot be verified as real or representative. It is not imported by the application, and `.gitignore` excludes it. Do not use it as training or test truth; the 100 rows and 10 positive labels are not enough to establish a valid prediction model.

### Why the screen is not called a trained abandonment model

Published abandonment studies identify plausible causes and risks, but the reviewed studies are retrospective questionnaires or small, context-specific case samples—not prospective validation that a particular indicator or score predicts abandonment. Cost, schedule, and earned-value metrics are useful for project control; that does **not** make them proven abandonment predictors. The screen therefore:

- does not train on the bundled sample CSV; that file is excluded from Git and is not treated as verified project/outcome data;
- does not produce a percentage probability, a guarantee, or an automated terminate/award decision;
- shows evidence flags separately so a reviewer can check the source record and explain a response;
- treats worker numbers, materials exposure, security status, and other context as evidence to review—not universal outcome labels.

## Steps to build and validate a project-specific ML model

Do these steps **before** describing any output as a learned probability or prediction:

1. **Define the decision and observation date.** Decide whether the target is construction contract abandonment, formal termination, prolonged suspension, completion followed by non-use, or another outcome. Keep these separate: they are different events. Choose when the forecast is made (for example, each monthly status date) and how far ahead it should look.
2. **Agree on outcome labels with domain experts.** Write inclusion and exclusion rules. Record the event date and source documents. Distinguish temporary stop, resequencing, weather/site-access pause, delayed completion, formal termination, restart/rescue, and post-completion non-use. Have more than one reviewer adjudicate ambiguous historical cases.
3. **Collect a longitudinal project history.** Use one dated row per project and reporting period—not a single final row. Preserve original and approved revised baselines, project type and size, PV/EV/AC, cost-to-complete forecasts and assumptions, measured quantities and milestones, dated schedule updates, certified invoices and payments, approved changes and unresolved claims, material exposure for remaining quantities, site possession/permit status, contractor capacity evidence, and worker hours/trade mix where reliably recorded.
4. **Freeze the reporting-date data definition.** Store an `as_of_date`, currency and price basis, units, project identifier, data source, and missing-data reason. Ensure every feature was knowable on that date. Treat missing values as missing—not as a negative event or evidence of distress.
5. **Prevent target leakage.** Exclude facts recorded after the forecast date, including termination paperwork, final cost, actual completion date, retrospective abandonment reason, and records that only exist because the outcome occurred. Keep the final outcome in a separate, reviewed label table.
6. **Check coverage, duplicates, and bias.** Measure how many independent projects, owners, contractors, regions, project types, and abandonment cases are represented. Document sampling and label uncertainty. Do not use the bundled mock CSV as ground truth. If cases are scarce or data definitions are inconsistent, remain rule-based.
7. **Establish simple baselines first.** Compare against a clear rule-based checklist and an interpretable model (such as regularized logistic regression) before considering more complex methods. Split validation by **project/contractor** and by **time** so the same project or contractor’s later rows do not leak across train and test. Fit preprocessing and any class balancing only on training folds.
8. **Evaluate the actual decision, not just accuracy.** Report the number and prevalence of labelled abandonment events; precision and recall; precision–recall and ROC curves; calibration and Brier score if probabilities are used; false alarms and missed cases at the chosen action threshold; uncertainty ranges; and performance by project type, value band, region, owner, and contractor where sample size permits.
9. **Calibrate and pilot prospectively.** Check probability calibration on later projects, compare predictions with adjudicated outcomes, test data drift and subgroup errors, and run in shadow mode before any operational use. Agree who investigates an alert and how it can be challenged.
10. **Govern the model over time.** Version the data dictionary, source extracts, code, labels, trained model, calibration, thresholds, and review approvals. Monitor performance and drift; define retraining and rollback criteria; keep a human decision-maker accountable; and stop using the model if evidence quality degrades.

## Research and evidence

The sources below support disciplined project controls and illustrate the limits of abandonment evidence; they do not justify a universal threshold or establish that this dashboard predicts abandonment.

1. **World Bank, _Procurement Regulations for IPF Borrowers_, sixth edition (February 2025).** Official procurement governance and document-retention context; not validation of project-risk predictors. [Official PDF](https://documents1.worldbank.org/curated/en/099722402252531135/pdf/IDU10a2d5d23110cc14a561badf1ef6ba448d853.pdf) · [Official text](https://documents1.worldbank.org/curated/en/099722402252531135/txt/IDU10a2d5d23110cc14a561badf1ef6ba448d853.txt)
2. **U.S. Government Accountability Office (2016), _Schedule Assessment Guide: Best Practices for Project Schedules_ (GAO-16-89G).** Schedule quality and assessment guidance, not evidence that SPI predicts abandonment. [Official guide page](https://www.gao.gov/products/gao-16-89g)
3. **U.S. Government Accountability Office (2020), _Cost Estimating and Assessment Guide_ (GAO-20-195G).** Cost-estimating and assessment guidance, not validation of the screen’s thresholds. [Official guide page](https://www.gao.gov/products/gao-20-195g)
4. **Adil, Abdulmajid & Mahdi (2019), “Analytical Study of the Causes of Abandoned Construction Projects.”** Questionnaire study with 101 respondents in Iraq; retrospective rankings of reported causes, not longitudinal predictive validation. [DOI / article](https://doi.org/10.28991/cej-2019-03091426)
5. **Al Amri & Marey-Pérez (2020), “Towards a sustainable construction industry: Delays and cost overrun causes in construction projects of Oman.”** Literature review and survey of 100 project managers; useful context for delay/overrun causes, not an abandonment prediction study. [DOI / article](https://doi.org/10.5267/j.jpm.2020.1.001)
6. **Nana-Addy, Musonda & Okoro, “Assessing Causative Characteristics of Abandoned Completed Urban Market Projects in Ghana.”** Eight purposively sampled abandoned completed markets; illustrates that abandonment may mean post-completion non-use, which must not be conflated with a contractor stopping work. [DOI / article](https://doi.org/10.21315/jcdc-02-21-0028)

## Testing

From the activated environment, run the focused tender-screen tests:

```bash
python -m unittest discover -s tests -v
```

## GitHub repository and local files

The intended repository display name is **Zephra - A Conbuild Insight** (GitHub slug: `zephra-a-conbuild-insight`). The house model is approved for publishing. No repository or remote has been created yet; publishing requires an authenticated GitHub account. Do not put credentials or access tokens in this repository.

Images, videos, generated results, source demo media, the tender notebook with embedded image outputs, and the bundled mock CSV are excluded from Git. Only `models/best.pt`, the trained checkpoint used by the app, is included so PPE inference works after cloning. User uploads and generated annotations remain local.

## Remaining work

This is a runnable demonstration, not yet a production construction-monitoring platform. Complete these items with the project owner and qualified construction, BIM, electrical, plumbing, safety, and project-controls professionals:

- [ ] Review the detailed concept house with the user; refine the rendered walls, openings, room layouts, and routed plumbing/electrical systems to match an agreed architectural design. The current Three.js geometry is illustrative and uses approximate dimensions.
- [ ] Accept an approved, dimensioned BIM source (for example IFC) and map real building elements, levels, coordinates, revisions, quantities, and MEP systems instead of treating the hand-built concept as a surveyed building.
- [ ] Connect each construction stage to approved drawings, inspection checklists, schedule activities, progress evidence, and revision history. The current stage selector is a demonstration; it does not read BIM/CDE or schedule data.
- [ ] Integrate authorized site evidence: georeferenced drone/PTZ imagery, site measurements, progress records, and any approved CDE/API feeds. Add authentication, access control, consent, retention, and audit history before storing site data.
- [ ] Validate the PPE detector on representative, permissioned site images. Measure class-level precision/recall, confidence calibration, camera and lighting limitations, and false-negative risks; do not treat it as a replacement for safety inspections.
- [ ] Keep the tender screen labelled as rule-based until verified longitudinal records and adjudicated outcomes support a prospectively validated model. Follow the ten-step data, leakage, evaluation, calibration, pilot, and governance workflow above; do not use the mock CSV as ground truth.
- [ ] Add automated browser regression coverage for BIM phases/layers, safety image upload/results, and tender form validation. Add persistence, operational logging, deployment configuration, and monitoring only when the production requirements are agreed.
- [ ] Create and push the GitHub repository after authenticating the intended owner account. Preserve all image/video exclusions and verify the exact files offered to Git before publishing.

## Copy/paste continuation prompt

Use this prompt to continue the project in a new coding session:

> Continue **Zephra — A Conbuild Insight** in the existing project folder. First inspect the current files and local changes; preserve work already present and do not overwrite or reset anything.
>
> **Run the app:** create/activate a Python 3.10+ virtual environment, install `requirements.txt`, run `python app.py`, and open `http://127.0.0.1:5050`. Port 5050 is intentional on this Mac because port 5000 is occupied. The main entry point is `app.py`; its separate workspaces are `/bim`, `/safety`, and `/tender-risk`.
>
> **Current implementation:** the Flask app uses a trained YOLO PPE checkpoint in `models/` at `/safety`; it reports ten classes listed above. The single-file Three.js BIM concept is in `templates/bim.html`, with staged site/excavation/foundation/structure/MEP/finishes views, a two-storey rendered-wall cutaway house, separate rooms, stairs, furnishings, a railed balcony, color-coded plumbing/drain/soil routes, and electrical risers with supported ceiling-perimeter circuits, lights, outlets, and a panel. The PTZ/drone controls are simulated. The BIM geometry, progress, and inspections are not connected to a real design, site, camera, schedule, or CDE. Three.js currently loads from a browser CDN, so the BIM page needs internet access.
>
> **Risk-screen boundary:** `/tender-risk` calls `tender_risk.py` and is a transparent, uncalibrated rule-based checklist—not a trained abandonment model, probability, or automated award/termination decision. Do not treat `tender/mock_construction_projects.csv` as truth. Use the README's ten-step research/data/label/leakage/split/evaluation/calibration/pilot/governance workflow before any ML claim.
> The tender page includes two editable synthetic buttons that fill and submit the full required form; their output demonstrates rule thresholds only, not project outcomes.
>
> **Priority next:** authenticate the intended GitHub account, confirm repository visibility, inspect the staged file list, then create and push the approved project. Keep every image/video and generated-result exclusion in `.gitignore`. Continue to label the BIM, simulated PTZ, PPE detector, and tender screen according to the limitations documented above.
>
> **Production work still needs user-provided/approved inputs:** a dimensioned BIM source such as IFC; design revisions and coordinate system; actual schedule and inspection records; authorized drone/PTZ/CDE feeds; and verified, longitudinal construction outcomes if a future abandonment model is desired. Do not fabricate these or infer them from the concept model. Use appropriately qualified professionals to validate design, structure, MEP, safety, and project-control decisions. Add access controls, retention/audit policy, automated browser tests, and operational deployment only after their requirements are agreed.
>
> **GitHub:** the intended repository display name is **Zephra - A Conbuild Insight**, slug `zephra-a-conbuild-insight`. The house is approved, but no repository or remote exists yet. Authenticate the intended GitHub account and confirm repository visibility before publishing. Preserve `.gitignore` exclusions for all image/video files, the embedded-image notebook, uploads/results, and mock CSV; verify the exact Git contents before any push. The README contains the run commands, detector classes, research citations, assumptions, and ML workflow.
