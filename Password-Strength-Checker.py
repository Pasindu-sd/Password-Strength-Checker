# password_checker.py
import re
import string

class PasswordChecker:
    def __init__(self):
        self.common_passwords = self.load_common_passwords()
    
    def load_common_passwords(self):
        # Load common passwords from file or create basic list
        common = ["password", "123456", "qwerty", "letmein", "admin"]
        try:
            with open("common_passwords.txt", "r") as f:
                common.extend([line.strip() for line in f])
        except FileNotFoundError:
            pass
        return set(common)
    
    def check_strength(self, password):
        score = 0
        feedback = []
        
        # Length check
        if len(password) >= 12:
            score += 2
        elif len(password) >= 8:
            score += 1
            feedback.append("Password length is good")
        else:
            feedback.append("Password should be at least 8 characters")
        
        # Character variety checks
        if re.search(r"[a-z]", password):
            score += 1
        else:
            feedback.append("Add lowercase letters")
        
        if re.search(r"[A-Z]", password):
            score += 1
        else:
            feedback.append("Add uppercase letters")
        
        if re.search(r"[0-9]", password):
            score += 1
        else:
            feedback.append("Add numbers")
        
        if re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]", password):
            score += 1
        else:
            feedback.append("Add special characters")
        
        # Common password check
        if password.lower() in self.common_passwords:
            score = 0
            feedback.append("This is a very common password - AVOID!")
        
        # Entropy calculation (advanced)
        entropy = self.calculate_entropy(password)
        
        return score, feedback, entropy
    
    def calculate_entropy(self, password):
        # Simple entropy calculation
        char_set = 0
        if any(c in string.ascii_lowercase for c in password): char_set += 26
        if any(c in string.ascii_uppercase for c in password): char_set += 26
        if any(c in string.digits for c in password): char_set += 10
        if any(c in string.punctuation for c in password): char_set += 32
        
        if char_set == 0:
            return 0
        
        entropy = len(password) * (char_set.bit_length())
        return entropy
    
    def get_strength_level(self, score):
        levels = {
            0: "Very Weak",
            1: "Weak",
            2: "Fair",
            3: "Good",
            4: "Strong",
            5: "Very Strong"
        }
        return levels.get(min(score, 5), "Very Weak")

# Main function
def main():
    checker = PasswordChecker()
    
    print("🔐 Password Strength Checker")
    print("=" * 30)
    
    while True:
        password = input("\nEnter password to check (or 'quit' to exit): ")
        
        if password.lower() == 'quit':
            break
        
        score, feedback, entropy = checker.check_strength(password)
        strength = checker.get_strength_level(score)
        
        print(f"\nPassword Strength: {strength}")
        
        print("\nFeedback:")
        for item in feedback:
            print(f"  {item}")
        
        # Generate suggestion
        if score < 3:
            print("\n💡 Suggestion: Use longer passwords with mix of characters")

if __name__ == "__main__":
    main()