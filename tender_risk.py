from datetime import date
from math import isfinite


FIELD_RANGES = {
    "baseline_cost_crore": (0.01, 1_000_000),
    "forecast_final_cost_crore": (0.01, 1_000_000),
    "planned_value_crore": (0, 1_000_000),
    "earned_value_crore": (0, 1_000_000),
    "actual_cost_crore": (0, 1_000_000),
    "baseline_duration_days": (1, 36_500),
    "elapsed_days": (0, 36_500),
    "planned_progress_pct": (0, 100),
    "actual_progress_pct": (0, 100),
    "last_week_progress_pct": (0, 100),
    "planned_weekly_progress_pct": (0.01, 100),
    "certified_payment_delay_days": (0, 3_650),
    "change_order_pct": (0, 1_000),
    "cashflow_coverage_months": (0, 120),
    "workers_present": (0, 1_000_000),
    "workers_planned": (1, 1_000_000),
    "material_cost_exposure_pct": (0, 1_000),
    "supplier_payment_delay_days": (0, 3_650),
}

READINESS_LABELS = {
    "ready": "Site access and permits ready",
    "partial": "Partial site access or permits outstanding",
    "blocked": "Site access or a critical permit blocked",
}
SECURITY_LABELS = {
    "valid": "Performance security current",
    "expiring": "Performance security expires within 90 days",
    "missing": "Performance security expired or not verified",
}

DEMO_EXAMPLES = {
    "steady": {
        "title": "Steady delivery",
        "description": "Synthetic on-plan values with no threshold flags.",
        "expected_level": "No prominent rule flags",
        "expected_score": 0,
        "values": {
            "snapshot_date": date.today().isoformat(),
            "baseline_cost_crore": 100,
            "forecast_final_cost_crore": 104,
            "planned_value_crore": 50,
            "earned_value_crore": 49,
            "actual_cost_crore": 48,
            "baseline_duration_days": 365,
            "elapsed_days": 180,
            "planned_progress_pct": 50,
            "actual_progress_pct": 49,
            "last_week_progress_pct": 2,
            "planned_weekly_progress_pct": 2,
            "certified_payment_delay_days": 0,
            "change_order_pct": 5,
            "cashflow_coverage_months": 3.5,
            "workers_present": 48,
            "workers_planned": 50,
            "material_cost_exposure_pct": 3,
            "supplier_payment_delay_days": 0,
            "site_readiness": "ready",
            "security_status": "valid",
        },
    },
    "multiple_stress_signals": {
        "title": "Multiple stress signals",
        "description": "Synthetic inputs that cross several review thresholds.",
        "expected_level": "High concern",
        "expected_score": 21,
        "values": {
            "snapshot_date": date.today().isoformat(),
            "baseline_cost_crore": 100,
            "forecast_final_cost_crore": 125,
            "planned_value_crore": 70,
            "earned_value_crore": 45,
            "actual_cost_crore": 60,
            "baseline_duration_days": 365,
            "elapsed_days": 220,
            "planned_progress_pct": 65,
            "actual_progress_pct": 48,
            "last_week_progress_pct": 0.4,
            "planned_weekly_progress_pct": 2,
            "certified_payment_delay_days": 75,
            "change_order_pct": 22,
            "cashflow_coverage_months": 0.5,
            "workers_present": 28,
            "workers_planned": 50,
            "material_cost_exposure_pct": 35,
            "supplier_payment_delay_days": 68,
            "site_readiness": "blocked",
            "security_status": "missing",
        },
    },
}


def parse_tender_inputs(form):
    values = {}
    errors = []

    snapshot_date = form.get("snapshot_date", "")
    try:
        parsed_date = date.fromisoformat(snapshot_date)
    except (TypeError, ValueError):
        errors.append("Reporting date must be a valid ISO calendar date.")
    else:
        if parsed_date > date.today():
            errors.append("Reporting date cannot be in the future.")
        else:
            values["snapshot_date"] = parsed_date.isoformat()

    for field, (minimum, maximum) in FIELD_RANGES.items():
        try:
            value = float(form.get(field, ""))
        except (TypeError, ValueError):
            errors.append(f"{field.replace('_', ' ').capitalize()} must be a number.")
            continue

        if not isfinite(value) or not minimum <= value <= maximum:
            errors.append(
                f"{field.replace('_', ' ').capitalize()} must be between "
                f"{minimum:g} and {maximum:g}."
            )
            continue
        values[field] = value

    readiness = form.get("site_readiness", "")
    if readiness not in READINESS_LABELS:
        errors.append("Choose a valid site access and permit status.")
    else:
        values["site_readiness"] = readiness

    security_status = form.get("security_status", "")
    if security_status not in SECURITY_LABELS:
        errors.append("Choose a valid performance-security status.")
    else:
        values["security_status"] = security_status

    if not errors and values["forecast_final_cost_crore"] < values["actual_cost_crore"]:
        errors.append("Forecast final cost cannot be lower than actual cost already incurred.")

    return values, errors


def assess_tender_risk(values):
    """Return a transparent, uncalibrated project-monitoring screen, not a probability."""
    baseline_cost = values["baseline_cost_crore"]
    forecast_cost = values["forecast_final_cost_crore"]
    cost_overrun_pct = (forecast_cost / baseline_cost - 1) * 100
    planned_value = values["planned_value_crore"]
    earned_value = values["earned_value_crore"]
    actual_cost = values["actual_cost_crore"]
    schedule_index = earned_value / planned_value if planned_value else None
    cost_index = earned_value / actual_cost if actual_cost else None
    progress_gap_pct = values["planned_progress_pct"] - values["actual_progress_pct"]
    planned_week = values["planned_weekly_progress_pct"]
    weekly_attainment_pct = values["last_week_progress_pct"] / planned_week * 100
    staffing_shortfall_pct = max(
        0,
        (1 - values["workers_present"] / values["workers_planned"]) * 100,
    )

    signals = []

    def add_signal(label, value, severity, explanation):
        signals.append(
            {
                "label": label,
                "value": value,
                "severity": severity,
                "points": 2 if severity == "high" else 1,
                "explanation": explanation,
            }
        )

    if cost_overrun_pct >= 20:
        add_signal(
            "Forecast cost growth",
            f"{cost_overrun_pct:.1f}%",
            "high",
            "The forecast-at-completion exceeds the approved baseline by at least 20%.",
        )
    elif cost_overrun_pct >= 10:
        add_signal(
            "Forecast cost growth",
            f"{cost_overrun_pct:.1f}%",
            "watch",
            "The forecast-at-completion is 10–20% above the approved baseline.",
        )

    if cost_index is not None and cost_index < 0.8:
        add_signal(
            "Earned-value cost index",
            f"CPI {cost_index:.2f}",
            "high",
            "Earned value is below 80% of actual cost to date; verify the approved measurement rules and cost cut-off.",
        )
    elif cost_index is not None and cost_index < 0.9:
        add_signal(
            "Earned-value cost index",
            f"CPI {cost_index:.2f}",
            "watch",
            "Earned value is below 90% of actual cost to date; verify the approved measurement rules and cost cut-off.",
        )

    if schedule_index is not None and schedule_index < 0.8:
        add_signal(
            "Earned-value schedule index",
            f"SPI {schedule_index:.2f}",
            "high",
            "Earned value is below 80% of planned value to date; check the critical path and remaining-work forecast.",
        )
    elif schedule_index is not None and schedule_index < 0.9:
        add_signal(
            "Earned-value schedule index",
            f"SPI {schedule_index:.2f}",
            "watch",
            "Earned value is below 90% of planned value to date; check the critical path and remaining-work forecast.",
        )

    if progress_gap_pct >= 10:
        add_signal(
            "Schedule / progress gap",
            f"{progress_gap_pct:.1f} percentage points behind",
            "high",
            "Reported physical progress is at least 10 percentage points behind the dated plan.",
        )
    elif progress_gap_pct >= 5:
        add_signal(
            "Schedule / progress gap",
            f"{progress_gap_pct:.1f} percentage points behind",
            "watch",
            "Reported physical progress is 5–10 percentage points behind the dated plan.",
        )

    if weekly_attainment_pct < 50:
        add_signal(
            "Recent progress rate",
            f"{weekly_attainment_pct:.0f}% of plan",
            "high",
            "Last week's earned progress is less than half the planned weekly rate.",
        )
    elif weekly_attainment_pct < 80:
        add_signal(
            "Recent progress rate",
            f"{weekly_attainment_pct:.0f}% of plan",
            "watch",
            "Last week's earned progress is below 80% of the planned weekly rate.",
        )

    payment_delay = values["certified_payment_delay_days"]
    if payment_delay >= 60:
        add_signal(
            "Certified payment delay",
            f"{payment_delay:.0f} days",
            "high",
            "An approved/certified payment is at least 60 days overdue.",
        )
    elif payment_delay >= 30:
        add_signal(
            "Certified payment delay",
            f"{payment_delay:.0f} days",
            "watch",
            "An approved/certified payment is 30–59 days overdue.",
        )

    supplier_delay = values["supplier_payment_delay_days"]
    if supplier_delay >= 60:
        add_signal(
            "Supplier / subcontractor payment delay",
            f"{supplier_delay:.0f} days",
            "high",
            "Verify reported payment arrears against current subcontractor and supplier statements.",
        )
    elif supplier_delay >= 30:
        add_signal(
            "Supplier / subcontractor payment delay",
            f"{supplier_delay:.0f} days",
            "watch",
            "Verify reported payment arrears against current subcontractor and supplier statements.",
        )

    change_orders = values["change_order_pct"]
    if change_orders >= 20:
        add_signal(
            "Approved change orders",
            f"{change_orders:.1f}% of baseline",
            "high",
            "Approved change orders total at least 20% of the baseline contract value.",
        )
    elif change_orders >= 10:
        add_signal(
            "Approved change orders",
            f"{change_orders:.1f}% of baseline",
            "watch",
            "Approved change orders total 10–20% of the baseline contract value.",
        )

    cash_cover = values["cashflow_coverage_months"]
    if cash_cover < 1:
        add_signal(
            "Contractor cash-flow cover",
            f"{cash_cover:.1f} months",
            "high",
            "Reported available liquidity covers less than one month of forecast site burn.",
        )
    elif cash_cover < 2:
        add_signal(
            "Contractor cash-flow cover",
            f"{cash_cover:.1f} months",
            "watch",
            "Reported available liquidity covers less than two months of forecast site burn.",
        )

    if staffing_shortfall_pct >= 30:
        add_signal(
            "Workforce against plan",
            f"{staffing_shortfall_pct:.0f}% below plan",
            "watch",
            "Reported headcount is at least 30% below the work-package plan; headcount alone is not an abandonment predictor.",
        )
    elif staffing_shortfall_pct >= 15:
        add_signal(
            "Workforce against plan",
            f"{staffing_shortfall_pct:.0f}% below plan",
            "watch",
            "Reported headcount is 15–30% below the work-package plan; review the trade mix and phase.",
        )

    if values["site_readiness"] == "blocked":
        add_signal(
            "Access / critical permits",
            "Blocked",
            "high",
            "Site access or a critical permit is reported blocked.",
        )
    elif values["site_readiness"] == "partial":
        add_signal(
            "Access / critical permits",
            "Partial",
            "watch",
            "Site access or permits remain partially outstanding.",
        )

    points = sum(signal["points"] for signal in signals)
    if points >= 6:
        level = "High concern"
        summary = "Several material warning signals need immediate project-control review."
    elif points >= 3:
        level = "Elevated signals"
        summary = "Review the flagged drivers with the project team and update the forecast."
    elif points:
        level = "Monitor closely"
        summary = "One or two screening flags are present; validate them with current project records."
    else:
        level = "No prominent rule flags"
        summary = "The entered values did not cross this screen's review thresholds."

    return {
        "level": level,
        "summary": summary,
        "signals": signals,
        "snapshot_date": values["snapshot_date"],
        "cost_overrun_pct": round(cost_overrun_pct, 1),
        "cost_performance_index": round(cost_index, 2) if cost_index is not None else None,
        "schedule_performance_index": round(schedule_index, 2) if schedule_index is not None else None,
        "progress_gap_pct": round(progress_gap_pct, 1),
        "weekly_attainment_pct": round(weekly_attainment_pct, 1),
        "duration_elapsed_pct": round(
            values["elapsed_days"] / values["baseline_duration_days"] * 100, 1
        ),
        "staffing_shortfall_pct": round(staffing_shortfall_pct, 1),
        "workers_present": int(values["workers_present"]),
        "workers_planned": int(values["workers_planned"]),
        "material_cost_exposure_pct": round(values["material_cost_exposure_pct"], 1),
        "score": points,
        "score_label": "unvalidated screening points — not a probability",
        "site_readiness": READINESS_LABELS[values["site_readiness"]],
        "security_status": SECURITY_LABELS[values["security_status"]],
    }
