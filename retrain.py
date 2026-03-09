"""Quick retrain script"""
import subprocess
import sys

print("=" * 60)
print("Retraining Vikas College Chatbot Model")
print("=" * 60)
print()

# Run train_model.py
result = subprocess.run([sys.executable, "train_model.py"], capture_output=False)

if result.returncode == 0:
    print("\n" + "=" * 60)
    print("✓ Model retrained successfully!")
    print("=" * 60)
else:
    print("\n" + "=" * 60)
    print("✗ Training failed!")
    print("=" * 60)
    sys.exit(1)
