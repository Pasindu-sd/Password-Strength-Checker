# password_checker_improved.py
import re
import string
import math
import random

class PasswordChecker:
    def __init__(self):
        self.common_passwords = self.load_common_passwords()
    
    def load_common_passwords(self):
        # Basic common list, optionally extend from file
        common = ["password", "123456", "qwerty", "letmein", "admin"]
        try:
            with open("common_passwords.txt", "r", encoding="utf-8") as f:
                common.extend([line.strip() for line in f if line.strip()])
        except FileNotFoundError:
            pass
        return set(p.lower() for p in common)
    
    def check_strength(self, password):
        score = 0
        feedback = []
        
        # Length check
        if len(password) >= 12:
            score += 2
            feedback.append("Length is strong (>=12)")
        elif len(password) >= 8:
            score += 1
            feedback.append("Length is acceptable (>=8), consider longer")
        else:
            feedback.append("Password should be at least 8 characters")
        
        # Character variety checks
        has_lower = bool(re.search(r"[a-z]", password))
        has_upper = bool(re.search(r"[A-Z]", password))
        has_digit = bool(re.search(r"[0-9]", password))
        has_special = bool(re.search(r"[{}]".format(re.escape(string.punctuation)), password))
        
        if has_lower:
            score += 1
            feedback.append("Contains lowercase letters")
        else:
            feedback.append("Add lowercase letters")
        
        if has_upper:
            score += 1
            feedback.append("Contains uppercase letters")
        else:
            feedback.append("Add uppercase letters")
        
        if has_digit:
            score += 1
            feedback.append("Contains numbers")
        else:
            feedback.append("Add numbers")
        
        if has_special:
            score += 1
            feedback.append("Contains special characters")
        else:
            feedback.append("Add special characters (e.g. !@#$%)")
        
        # If very common password, override and mark as very weak
        if password.lower() in self.common_passwords:
            score = 0
            feedback.append("This is a very common password — AVOID!")
        
        # Calculate entropy (bits)
        entropy = self.calculate_entropy(password)
        
        # Estimate crack time using a reasonable attacker speed (default 1e9 guesses/sec)
        crack_estimates = {
            "1k/sec": self.estimate_crack_time(entropy, 1e3),
            "1M/sec": self.estimate_crack_time(entropy, 1e6),
            "1B/sec": self.estimate_crack_time(entropy, 1e9),
        }
        
        # Strength level (cap score to 5)
        strength = self.get_strength_level(score)
        
        return {
            "score": min(score, 5),
            "strength": strength,
            "feedback": feedback,
            "entropy": round(entropy, 2),
            "crack_estimates": crack_estimates
        }
    
    def calculate_entropy(self, password):
        # Determine character set size used
        char_set = 0
        if any(c in string.ascii_lowercase for c in password): char_set += 26
        if any(c in string.ascii_uppercase for c in password): char_set += 26
        if any(c in string.digits for c in password): char_set += 10
        if any(c in string.punctuation for c in password): char_set += len(string.punctuation)
        # Note: if password contains other unicode symbols, this simple method won't count them.
        
        if char_set == 0:
            return 0.0
        
        # Standard entropy formula: length * log2(character_set_size)
        entropy = len(password) * math.log2(char_set)
        return entropy
    
    def estimate_crack_time(self, entropy_bits, guesses_per_second):
        # number of possible combinations (worst-case): 2 ** entropy_bits
        # time_seconds = guesses / guesses_per_second
        if entropy_bits <= 0:
            return "instant"
        try:
            guesses = 2 ** entropy_bits
        except OverflowError:
            # extremely large entropy -> practically uncrackable with given rates
            return "practically infinite"
        
        seconds = guesses / guesses_per_second
        return self._human_readable_time(seconds)
    
    def _human_readable_time(self, seconds):
        # Convert seconds to human readable format
        if seconds < 1:
            return f"{seconds:.3f} seconds"
        minute = 60
        hour = minute * 60
        day = hour * 24
        year = day * 365.25
        
        if seconds < minute:
            return f"{seconds:.2f} seconds"
        elif seconds < hour:
            return f"{seconds / minute:.2f} minutes"
        elif seconds < day:
            return f"{seconds / hour:.2f} hours"
        elif seconds < year:
            return f"{seconds / day:.2f} days"
        else:
            yrs = seconds / year
            if yrs > 1e6:
                return f"{yrs:.2e} years"
            return f"{yrs:.2f} years"
    
    def get_strength_level(self, score):
        # Map score to level
        levels = {
            0: "Very Weak",
            1: "Weak",
            2: "Fair",
            3: "Good",
            4: "Strong",
            5: "Very Strong"
        }
        return levels.get(min(score, 5), "Very Weak")
    
    def suggest_password(self, length=14):
        # Generate a suggested strong password
        if length < 8:
            length = 8
        chars = string.ascii_letters + string.digits + string.punctuation
        # ensure at least one from each class
        pw = [
            random.choice(string.ascii_lowercase),
            random.choice(string.ascii_uppercase),
            random.choice(string.digits),
            random.choice(string.punctuation),
        ]
        pw += [random.choice(chars) for _ in range(length - len(pw))]
        random.shuffle(pw)
        return ''.join(pw)

def main():
    checker = PasswordChecker()
    print("Improved Password Strength Checker")
    print("=" * 40)
    while True:
        password = input("\nEnter password to check (or 'quit' to exit): ")
        if password.lower() == 'quit':
            break
        
        result = checker.check_strength(password)
        print(f"\nPassword Strength: {result['strength']}")
        print(f"Score: {result['score']}/5")
        print(f"Entropy: {result['entropy']} bits")
        print("\nFeedback:")
        for item in result['feedback']:
            print(" ", item)
        
        print("\nEstimated crack time (attacker speeds):")
        for k, v in result['crack_estimates'].items():
            print(f"  {k}: {v}")
        
        if result['score'] < 3:
            print("\nSuggestion: Use a longer password with a mix of upper/lower/digits/specials.")
            print("Suggested strong password:", checker.suggest_password(14))
        else:
            print("\nGood password! Consider using a password manager for unique passwords.")

if __name__ == "__main__":
    main()
