import os
import glob

def scan_for_secrets(directory):
    print(f"[*] Scanning directory for security risks: {directory}\n")
    
    # ज्या शब्दांवर शंका घ्यायची आहे
    risk_keywords = ["password", "secret", "api_key", "access_token", "private_key"]
    
    issues_found = 0
    
    # फोल्डरमधील सर्व पायथन (.py) फाईल्स शोधणे
    python_files = glob.glob(os.path.join(directory, "**", "*.py"), recursive=True)
    
    if not python_files:
        print("[!] No Python files found in this directory.")
        return

    for file_path in python_files:
        # स्वतःच्या scanner.py फाईलला स्कॅन करणे टाळण्यासाठी (Skip self)
        if file_path.endswith("scanner.py"):
            continue

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
                for line_no, line in enumerate(lines, 1):
                    for keyword in risk_keywords:
                        if keyword in line.lower() and "=" in line:
                            print(f"[!] SECURITY RISK FOUND:")
                            print(f"    File: {file_path}")
                            print(f"    Line {line_no}: {line.strip()}\n")
                            issues_found += 1
        except Exception as e:
            print(f"[x] Could not read file {file_path}: {e}")

    if issues_found == 0:
        print("[+] Scan complete! No hardcoded secrets found. Your code looks safe.")
    else:
        print(f"[!] Scan complete. Total potential security issues found: {issues_found}")

if __name__ == "__main__":
    current_dir = os.getcwd()
    scan_for_secrets(current_dir)