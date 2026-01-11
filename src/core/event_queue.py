"""
Event Queue Manager
Handles the donation event queue with debounce protection
"""

import threading
import time
from collections import deque
from typing import Callable, Optional, List
from dataclasses import dataclass
from datetime import datetime, timedelta

from .models import DonationEvent


@dataclass
class QueueStats:
    """Statistics about the event queue"""
    total_received: int = 0
    total_processed: int = 0
    total_displayed: int = 0
    total_debounced: int = 0
    queue_size: int = 0
    is_processing: bool = False
    last_event_time: Optional[datetime] = None


class EventQueue:
    """
    Thread-safe event queue with debounce protection and priority handling
    """
    
    def __init__(
        self,
        debounce_ms: int = 500,
        max_queue_size: int = 100,
        on_event_ready: Optional[Callable[[DonationEvent], None]] = None
    ):
        self._queue: deque[DonationEvent] = deque(maxlen=max_queue_size)
        self._history: List[DonationEvent] = []
        self._lock = threading.RLock()
        self._debounce_ms = debounce_ms
        self._max_queue_size = max_queue_size
        self._on_event_ready = on_event_ready
        
        self._stats = QueueStats()
        self._last_event_hash: Optional[str] = None
        self._last_event_time: Optional[datetime] = None
        
        self._processing = False
        self._process_thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        
        self._current_display_duration = 5.0
    
    def set_display_duration(self, duration: float):
        """Set the display duration for events"""
        self._current_display_duration = duration
    
    def set_debounce(self, debounce_ms: int):
        """Update debounce time"""
        self._debounce_ms = debounce_ms
    
    def set_callback(self, callback: Callable[[DonationEvent], None]):
        """Set the callback for when an event is ready to display"""
        self._on_event_ready = callback
    
    def _get_event_hash(self, event: DonationEvent) -> str:
        """Generate a hash for debounce comparison"""
        return f"{event.sender}:{event.amount}:{event.message}"
    
    def _is_duplicate(self, event: DonationEvent) -> bool:
        """Check if event is a duplicate within debounce window"""
        if self._last_event_hash is None:
            return False
        
        current_hash = self._get_event_hash(event)
        if current_hash != self._last_event_hash:
            return False
        
        if self._last_event_time is None:
            return False
        
        time_diff = (datetime.now() - self._last_event_time).total_seconds() * 1000
        return time_diff < self._debounce_ms
    
    def add_event(self, event: DonationEvent) -> bool:
        """
        Add an event to the queue
        Returns True if added, False if debounced
        """
        with self._lock:
            self._stats.total_received += 1
            
            # Check for duplicate
            if self._is_duplicate(event):
                self._stats.total_debounced += 1
                return False
            
            # Update tracking
            self._last_event_hash = self._get_event_hash(event)
            self._last_event_time = datetime.now()
            self._stats.last_event_time = datetime.now()
            
            # Add to queue
            self._queue.append(event)
            self._stats.queue_size = len(self._queue)
            
            return True
    
    def get_next_event(self) -> Optional[DonationEvent]:
        """Get the next event from the queue"""
        with self._lock:
            if len(self._queue) == 0:
                return None
            
            event = self._queue.popleft()
            event.processed = True
            self._stats.total_processed += 1
            self._stats.queue_size = len(self._queue)
            
            return event
    
    def peek_next_event(self) -> Optional[DonationEvent]:
        """Peek at the next event without removing it"""
        with self._lock:
            if len(self._queue) == 0:
                return None
            return self._queue[0]
    
    def start_processing(self):
        """Start the event processing loop"""
        if self._processing:
            return
        
        self._processing = True
        self._stop_event.clear()
        self._process_thread = threading.Thread(target=self._process_loop, daemon=True)
        self._process_thread.start()
    
    def stop_processing(self):
        """Stop the event processing loop"""
        self._processing = False
        self._stop_event.set()
        if self._process_thread:
            self._process_thread.join(timeout=2.0)
    
    def _process_loop(self):
        """Main processing loop"""
        while not self._stop_event.is_set():
            event = self.get_next_event()
            
            if event and self._on_event_ready:
                self._stats.is_processing = True
                event.displayed = True
                self._stats.total_displayed += 1
                
                # Add to history
                with self._lock:
                    self._history.insert(0, event)
                    if len(self._history) > 500:  # Keep last 500 events
                        self._history = self._history[:500]
                
                # Trigger callback
                self._on_event_ready(event)
                
                # Wait for display duration
                time.sleep(self._current_display_duration)
                self._stats.is_processing = False
            else:
                # Small sleep when queue is empty
                time.sleep(0.1)
    
    def get_stats(self) -> QueueStats:
        """Get current queue statistics"""
        with self._lock:
            self._stats.queue_size = len(self._queue)
            return self._stats
    
    def get_history(self, limit: int = 50) -> List[DonationEvent]:
        """Get event history"""
        with self._lock:
            return self._history[:limit]
    
    def clear_queue(self):
        """Clear all pending events"""
        with self._lock:
            self._queue.clear()
            self._stats.queue_size = 0
    
    def clear_history(self):
        """Clear event history"""
        with self._lock:
            self._history.clear()
    
    @property
    def is_processing(self) -> bool:
        return self._processing
    
    @property
    def queue_size(self) -> int:
        with self._lock:
            return len(self._queue)
