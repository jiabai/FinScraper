"""Tests for retry module."""
import pytest
from finscraper.core.retry import retry_with_backoff


def test_retry_success_on_first_attempt():
    call_count = 0
    
    @retry_with_backoff(max_retries=3, delay=0.1)
    def successful_function():
        nonlocal call_count
        call_count += 1
        return "success"
    
    result = successful_function()
    assert result == "success"
    assert call_count == 1


def test_retry_success_after_failures():
    call_count = 0
    
    @retry_with_backoff(max_retries=3, delay=0.1)
    def eventually_successful_function():
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise ValueError("Temporary error")
        return "success"
    
    result = eventually_successful_function()
    assert result == "success"
    assert call_count == 3


def test_retry_max_retries_exceeded():
    call_count = 0
    
    @retry_with_backoff(max_retries=2, delay=0.1)
    def always_failing_function():
        nonlocal call_count
        call_count += 1
        raise ValueError("Permanent error")
    
    with pytest.raises(ValueError, match="Permanent error"):
        always_failing_function()
    
    assert call_count == 3  # Initial + 2 retries
