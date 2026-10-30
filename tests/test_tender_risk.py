from datetime import date, timedelta
import unittest

from tender_risk import DEMO_EXAMPLES, assess_tender_risk, parse_tender_inputs


class TenderRiskTests(unittest.TestCase):
    def setUp(self):
        self.values = {
            "snapshot_date": "2025-01-15",
            "baseline_cost_crore": 100,
            "forecast_final_cost_crore": 102,
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
            "change_order_pct": 1,
            "cashflow_coverage_months": 4,
            "workers_present": 48,
            "workers_planned": 50,
            "material_cost_exposure_pct": 1,
            "supplier_payment_delay_days": 0,
            "site_readiness": "ready",
            "security_status": "valid",
        }

    def test_on_plan_inputs_have_no_screening_flags(self):
        result = assess_tender_risk(self.values)

        self.assertEqual(result["level"], "No prominent rule flags")
        self.assertEqual(result["signals"], [])
        self.assertIn("not a probability", result["score_label"])

    def test_multiple_project_control_signals_are_explained(self):
        self.values.update(
            forecast_final_cost_crore=125,
            planned_progress_pct=65,
            actual_progress_pct=50,
            last_week_progress_pct=0.4,
            certified_payment_delay_days=75,
            site_readiness="blocked",
        )

        result = assess_tender_risk(self.values)

        self.assertEqual(result["level"], "High concern")
        self.assertGreaterEqual(len(result["signals"]), 5)
        self.assertTrue(all(signal["explanation"] for signal in result["signals"]))
        self.assertEqual(result["workers_present"], 48)

    def test_worker_count_is_only_compared_to_planned_work_package_staff(self):
        result = assess_tender_risk(self.values)

        workforce_flags = [
            signal for signal in result["signals"]
            if signal["label"] == "Workforce against plan"
        ]
        self.assertEqual(workforce_flags, [])

    def test_form_rejects_non_numeric_and_out_of_range_values(self):
        form = {
            "snapshot_date": "2025-01-15",
            "baseline_cost_crore": "NaN",
            "forecast_final_cost_crore": "-1",
            "planned_value_crore": "50",
            "earned_value_crore": "49",
            "actual_cost_crore": "48",
            "baseline_duration_days": "365",
            "elapsed_days": "180",
            "planned_progress_pct": "50",
            "actual_progress_pct": "49",
            "last_week_progress_pct": "2",
            "planned_weekly_progress_pct": "2",
            "certified_payment_delay_days": "0",
            "change_order_pct": "1",
            "cashflow_coverage_months": "4",
            "workers_present": "48",
            "workers_planned": "50",
            "material_cost_exposure_pct": "1",
            "supplier_payment_delay_days": "0",
            "site_readiness": "ready",
            "security_status": "valid",
        }

        values, errors = parse_tender_inputs(form)

        self.assertEqual(len(errors), 2)
        self.assertNotIn("baseline_cost_crore", values)
        self.assertNotIn("forecast_final_cost_crore", values)

    def test_form_rejects_incorrect_site_status(self):
        form = {key: str(value) for key, value in self.values.items()}
        form["site_readiness"] = "guess"

        values, errors = parse_tender_inputs(form)

        self.assertEqual(len(errors), 1)
        self.assertIn("site access", errors[0].lower())

    def test_forecast_cost_cannot_be_below_incurred_cost(self):
        form = {key: str(value) for key, value in self.values.items()}
        form["actual_cost_crore"] = "110"

        _, errors = parse_tender_inputs(form)

        self.assertTrue(any("lower than actual cost" in error for error in errors))

    def test_form_rejects_invalid_snapshot_date(self):
        form = {key: str(value) for key, value in self.values.items()}
        form["snapshot_date"] = "not-a-date"

        _, errors = parse_tender_inputs(form)

        self.assertTrue(any("reporting date" in error.lower() for error in errors))

    def test_form_rejects_future_reporting_date(self):
        form = {key: str(value) for key, value in self.values.items()}
        form["snapshot_date"] = (date.today() + timedelta(days=1)).isoformat()

        _, errors = parse_tender_inputs(form)

        self.assertTrue(any("cannot be in the future" in error for error in errors))

    def test_zero_planned_or_actual_cost_leaves_index_unavailable(self):
        self.values.update(planned_value_crore=0, actual_cost_crore=0)

        result = assess_tender_risk(self.values)

        self.assertIsNone(result["schedule_performance_index"])
        self.assertIsNone(result["cost_performance_index"])

    def test_demo_examples_are_valid_and_match_their_rule_outputs(self):
        for example in DEMO_EXAMPLES.values():
            with self.subTest(example=example["title"]):
                form = {
                    field: str(value)
                    for field, value in example["values"].items()
                }
                values, errors = parse_tender_inputs(form)

                self.assertEqual(errors, [])
                result = assess_tender_risk(values)
                self.assertEqual(result["level"], example["expected_level"])
                self.assertEqual(result["score"], example["expected_score"])


if __name__ == "__main__":
    unittest.main()
