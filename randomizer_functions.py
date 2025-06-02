import random
import string
from datetime import datetime, timedelta

def generate_random_string( length=8, prefix=''):
    """Generate a random string with optional prefix"""
    chars = string.ascii_uppercase + string.digits
    return prefix + ''.join(random.choice(chars) for _ in range(length))

def generate_random_number( min_val=1, max_val=1000):
    """Generate a random number within range"""
    return random.randint(min_val, max_val)

def generate_random_date( start_date=None, end_date=None):
    """Generate a random date between start_date and end_date"""
    if not start_date:
        start_date = datetime.now() - timedelta(days=365)
    if not end_date:
        end_date = datetime.now() + timedelta(days=365)
    
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return (start_date + timedelta(days=random_days)).isoformat()
def generate_random_boolean():
    """Generate a random boolean value"""
    return random.choice([True, False])

def generate_random_float( min_val=0.0, max_val=100.0, precision=2):
    """Generate a random float with specified precision"""
    return round(random.uniform(min_val, max_val), precision)
