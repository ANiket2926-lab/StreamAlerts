"""
Mock Donation Generator
For testing and stress testing the system
"""

import random
import threading
import time
from datetime import datetime
from typing import Callable, Optional, List

# Sample Indian names
SAMPLE_NAMES = [
    "Rahul Sharma", "Priya Patel", "Amit Kumar", "Sneha Gupta", "Vikram Singh",
    "Anjali Reddy", "Arjun Nair", "Deepika Iyer", "Karan Mehta", "Pooja Joshi",
    "Rohan Desai", "Neha Kapoor", "Siddharth Rao", "Divya Shah", "Aditya Verma",
    "Megha Chopra", "Varun Malhotra", "Ritika Saxena", "Kunal Bhatt", "Simran Kaur"
]

SAMPLE_MESSAGES = [
    "Love your stream! Keep it up! 🔥",
    "You're amazing! 💖",
    "Best streamer ever!",
    "Thanks for the entertainment!",
    "Great content as always! 🎮",
    "You make my day! ✨",
    "Keep grinding! 💪",
    "Sending love from Mumbai! 🌟",
    "First donation! Excited to support you!",
    "Been watching for 2 years, happy to finally donate!",
    "Your stream is the best! Never stop!",
    "Late night gang! 🌙",
    "Clutch that game! 🎯",
    "GG! Well played! 🏆",
    "You deserve more subs!",
    "Making my day better! 😊",
    "India represent! 🇮🇳",
    "Weekend vibes! 🎉",
    "Coffee money for you! ☕",
    "Marathon stream donation! 💎"
]

# Common donation amounts in INR
COMMON_AMOUNTS = [10, 20, 50, 100, 199, 299, 499, 500, 999, 1000, 1999, 2000, 5000]

# Weight distribution for amounts (smaller amounts more common)
AMOUNT_WEIGHTS = [15, 15, 20, 25, 10, 8, 5, 10, 3, 5, 2, 2, 1]


class MockDonationGenerator:
    """
    Generates mock donation events for testing
    """
    
    def __init__(self, on_donation: Optional[Callable[[dict], None]] = None):
        self._on_donation = on_donation
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        
        # Stats
        self._total_generated = 0
        self._total_amount = 0
    
    def set_callback(self, callback: Callable[[dict], None]):
        """Set the donation callback"""
        self._on_donation = callback
    
    def generate_single(self) -> dict:
        """Generate a single random donation event"""
        amount = random.choices(COMMON_AMOUNTS, weights=AMOUNT_WEIGHTS)[0]
        
        # Add some randomness
        if random.random() < 0.2:
            amount = random.randint(1, 1000)
        
        event = {
            "sender": random.choice(SAMPLE_NAMES),
            "amount": amount,
            "currency": "INR",
            "message": random.choice(SAMPLE_MESSAGES) if random.random() > 0.1 else "",
            "timestamp": datetime.now().isoformat()
        }
        
        self._total_generated += 1
        self._total_amount += amount
        
        if self._on_donation:
            self._on_donation(event)
        
        return event
    
    def start_continuous(self, min_interval: float = 3.0, max_interval: float = 10.0):
        """
        Start generating donations continuously at random intervals
        """
        if self._running:
            return
        
        self._running = True
        self._stop_event.clear()
        
        def generate_loop():
            while not self._stop_event.is_set():
                self.generate_single()
                interval = random.uniform(min_interval, max_interval)
                self._stop_event.wait(interval)
        
        self._thread = threading.Thread(target=generate_loop, daemon=True)
        self._thread.start()
    
    def stop_continuous(self):
        """Stop continuous generation"""
        self._running = False
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=2.0)
            self._thread = None
    
    def stress_test(self, count: int = 50, interval: float = 0.1):
        """
        Generate a burst of donations for stress testing
        """
        self._stress_stop = threading.Event()
        
        def burst():
            for i in range(count):
                if self._stress_stop.is_set():
                    break
                self.generate_single()
                time.sleep(interval)
        
        self._stress_thread = threading.Thread(target=burst, daemon=True)
        self._stress_thread.start()
        return self._stress_thread
    
    def stop_stress_test(self):
        """Stop ongoing stress test"""
        if hasattr(self, '_stress_stop'):
            self._stress_stop.set()
        if hasattr(self, '_stress_thread') and self._stress_thread:
            self._stress_thread.join(timeout=2.0)
            self._stress_thread = None
    
    def generate_batch(self, count: int) -> List[dict]:
        """Generate a batch of donations immediately"""
        return [self.generate_single() for _ in range(count)]
    
    @property
    def is_running(self) -> bool:
        return self._running
    
    @property
    def stats(self) -> dict:
        return {
            "total_generated": self._total_generated,
            "total_amount": self._total_amount,
            "average_amount": self._total_amount / max(1, self._total_generated)
        }
    
    def reset_stats(self):
        """Reset generation statistics"""
        self._total_generated = 0
        self._total_amount = 0
