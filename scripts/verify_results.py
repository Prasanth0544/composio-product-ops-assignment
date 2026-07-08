import csv
import json
import os

VERIF_PATH = os.path.join('data', 'verification_sample.csv')
METRICS_PATH = os.path.join('data', 'verification_metrics.json')

def calculate_metrics():
    if not os.path.exists(VERIF_PATH):
        print(f"Error: {VERIF_PATH} not found.")
        return
    
    total = 0
    first_pass_correct_count = 0
    final_correct_count = 0
    mistakes_fixes = []
    
    with open(VERIF_PATH, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            total += 1
            # Normalize strings for comparison
            fp = row.get('first_pass_correct', '').strip().lower()
            fs = row.get('final_status', '').strip().lower()
            
            if fp == 'yes':
                first_pass_correct_count += 1
            else:
                # Log the mistake and correction
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
    
    # Save metrics JSON
    with open(METRICS_PATH, 'w', encoding='utf-8-sig') as f:
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
    calculate_metrics()
