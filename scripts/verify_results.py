import csv
import json
import os


class VerificationAgent:
  """Audits the verification sample and computes calibrated accuracy metrics."""

  def __init__(self, verif_path=None, metrics_path=None):
    self.verif_path = verif_path or os.path.join('data', 'verification_sample.csv')
    self.metrics_path = metrics_path or os.path.join('data', 'verification_metrics.json')

  def calculate_metrics(self):
    """Manually audits the sample set and logs mismatch errors."""
    if not os.path.exists(self.verif_path):
      print(f"Error: {self.verif_path} not found.")
      return None

    total = 0
    first_pass_correct_count = 0
    final_correct_count = 0
    mistakes_fixes = []

    with open(self.verif_path, 'r', encoding='utf-8-sig') as f:
      reader = csv.DictReader(f)
      for row in reader:
        total += 1
        fp = row.get('first_pass_correct', '').strip().lower()
        fs = row.get('final_status', '').strip().lower()

        if fp == 'yes':
          first_pass_correct_count += 1
        else:
          mistakes_fixes.append({
            "id": row.get('id'),
            "app_name": row.get('app_name'),
            "category": row.get('category'),
            "auth_method": row.get('auth_method'),
            "correction": row.get('correction_applied', 'Unknown correction')
          })

        if fs == 'correct':
          final_correct_count += 1

    first_pass_accuracy = (first_pass_correct_count / total * 100) if total > 0 else 0
    final_accuracy = (final_correct_count / total * 100) if total > 0 else 0

    metrics = {
      "sample_size": total,
      "first_pass_correct": first_pass_correct_count,
      "first_pass_accuracy": round(first_pass_accuracy, 2),
      "final_correct": final_correct_count,
      "final_accuracy": round(final_accuracy, 2),
      "mistakes_fixes": mistakes_fixes
    }

    os.makedirs(os.path.dirname(self.metrics_path) or '.', exist_ok=True)
    with open(self.metrics_path, 'w', encoding='utf-8-sig') as f:
      json.dump(metrics, f, indent=4, ensure_ascii=False)

    print("=== Verification Audit Report ===")
    print(f"Sample Size Checked: {total} apps")
    print(f"First-pass Correct: {first_pass_correct_count} ({metrics['first_pass_accuracy']}% accuracy)")
    print(f"Final Corrected Status: {final_correct_count} ({metrics['final_accuracy']}% accuracy)")
    print(f"Mistakes Detected: {len(mistakes_fixes)}")
    for m in mistakes_fixes:
      print(f" - App {m['id']} ({m['app_name']}): {m['correction']}")

    return metrics


if __name__ == '__main__':
  VerificationAgent().calculate_metrics()
