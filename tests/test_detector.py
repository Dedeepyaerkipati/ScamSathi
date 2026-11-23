import unittest
from detection.message_detector import analyze_message


class ScamSathiDetectorTests(unittest.TestCase):
    def test_upi_qr_refund_scam_is_high_risk(self):
        msg = "Your refund is ready. Scan this QR to receive money and enter UPI PIN to receive the amount."
        result = analyze_message(msg)
        labels = {x["label"] for x in result["indicators"]}
        self.assertIn("UPI collect-request or QR-code pattern", labels)
        self.assertIn("Request for sensitive information", labels)
        self.assertGreaterEqual(result["rule_score"], 60)
        self.assertEqual(result["risk_level"], "High risk")

    def test_electricity_disconnection_scam_is_high_risk(self):
        msg = "Your electricity connection will be disconnected tonight due to pending bill. Pay immediately."
        result = analyze_message(msg)
        labels = {x["label"] for x in result["indicators"]}
        self.assertTrue(any("electricity" in label.lower() for label in labels))
        self.assertGreaterEqual(result["rule_score"], 55)
        self.assertEqual(result["risk_level"], "High risk")

    def test_normal_meeting_has_no_rule_warnings(self):
        result = analyze_message("Hi! Our project meeting is tomorrow at 10 AM. Please bring your laptop.")
        self.assertEqual(result["rule_score"], 0)
        self.assertEqual(len(result["indicators"]), 0)

    def test_normal_upi_payment_mention_is_not_automatically_flagged(self):
        result = analyze_message("I paid the shop 500 rupees through UPI. Thank you.")
        self.assertNotIn("UPI collect-request or QR-code pattern", {x["label"] for x in result["indicators"]})

    def test_safety_warning_about_upi_pin_is_not_flagged_as_request(self):
        result = analyze_message("Never enter your UPI PIN to receive money. A PIN only authorizes payments.")
        self.assertNotIn("Request for sensitive information", {x["label"] for x in result["indicators"]})
        self.assertNotIn("UPI collect-request or QR-code pattern", {x["label"] for x in result["indicators"]})

    def test_normal_electricity_bill_reminder_not_high_risk(self):
        result = analyze_message("Your electricity bill is due next week. Please pay using the official provider app.")
        self.assertNotEqual(result["risk_level"], "High risk")
        self.assertFalse(any("disconnection" in x["label"].lower() for x in result["indicators"]))

    def test_courier_fee_pattern(self):
        result = analyze_message("Your parcel is on hold due to an address issue. Pay customs fee to release it.")
        self.assertIn("Courier or parcel-fee pattern", {x["label"] for x in result["indicators"]})

    def test_job_upfront_fee_pattern(self):
        result = analyze_message("Work from home job. Pay registration fee to activate your account.")
        self.assertIn("Job or task scam with upfront payment", {x["label"] for x in result["indicators"]})


if __name__ == "__main__":
    unittest.main()
