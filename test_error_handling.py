#!/usr/bin/env python3
"""
Test script to verify proper error handling in API endpoints.

This script tests:
1. Non-existent user returns error SVG with 502 status
2. Invalid data handling returns proper error messages
3. Actions endpoint requires authentication
4. Error responses are properly cached
"""

import requests
import json
import os
from datetime import datetime

from utils.logger import setup_logger

# API base URL
API_BASE = "http://localhost:8000"
VERBOSE_TESTS = os.getenv("VERBOSE_TESTS") == "1"
logger = setup_logger(__name__, level="INFO" if VERBOSE_TESTS else "WARNING")

def test_nonexistent_user():
    """Test API response for non-existent username"""
    logger.info("\n%s", "=" * 60)
    logger.info("TEST 1: Non-existent User Handling")
    logger.info("%s", "=" * 60)
    
    username = "nonexistentuser_" + datetime.now().strftime("%Y%m%d%H%M%S")
    endpoints = [
        "/api/stats",
        "/api/languages",
        "/api/contributions",
        "/api/trophy",
        "/api/streak",
        "/api/repos"
    ]
    
    for endpoint in endpoints:
        try:
            url = f"{API_BASE}{endpoint}?username={username}"
            response = requests.get(url, timeout=10)
            
            # Check status code
            if response.status_code == 502:
                logger.info("PASS %s: Correctly returns 502 Bad Gateway", endpoint)
                # Check for error header
                if response.headers.get("X-Error"):
                    logger.info("  Error header present: %s", response.headers.get("X-Error"))
                # Check content type is SVG
                if "image/svg+xml" in response.headers.get("Content-Type", ""):
                    logger.info("  Returns SVG error card")
                else:
                    logger.error("  Wrong content type: %s", response.headers.get("Content-Type"))
            elif response.status_code == 200:
                logger.error("FAIL %s: Returns 200 (should be 502) - FALLBACK TO MOCK DATA DETECTED", endpoint)
            else:
                logger.warning("%s: Returns %s", endpoint, response.status_code)
                
        except Exception as e:
            logger.error("FAIL %s: Error - %s", endpoint, e)


def test_actions_without_auth():
    """Test Actions endpoint requires authentication"""
    logger.info("\n%s", "=" * 60)
    logger.info("TEST 2: GitHub Actions Authentication")
    logger.info("%s", "=" * 60)
    
    url = f"{API_BASE}/api/actions?username=torvalds"
    
    try:
        # Without token
        response = requests.get(url, timeout=10)
        
        if response.status_code == 401:
            logger.info("PASS Actions endpoint correctly returns 401 without token")
            if "Unauthorized" in response.text or "authentication" in response.text.lower():
                logger.info("  Error message mentions authentication")
        elif response.status_code == 200:
            logger.error("FAIL Actions endpoint returns 200 (should require auth) - MOCK DATA RETURNED")
        else:
            logger.warning("Actions endpoint returns %s", response.status_code)
            
    except Exception as e:
        logger.error("FAIL Error: %s", e)


def test_actions_with_auth():
    """Test Actions endpoint with authentication"""
    logger.info("\n%s", "=" * 60)
    logger.info("TEST 3: GitHub Actions with Authentication")
    logger.info("%s", "=" * 60)
    
    # Using a non-existent user with token to test error handling
    url = f"{API_BASE}/api/actions?username=nonexistentuser_test"
    
    # Use a fake token to test
    headers = {"Authorization": "Bearer fake_token_for_testing"}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 502:
            logger.info("PASS Actions endpoint with invalid user returns 502")
            if response.headers.get("X-Error"):
                logger.info("  Error header present: %s", response.headers.get("X-Error"))
        elif response.status_code == 200:
            logger.error("FAIL Actions endpoint returns 200 (should return error for nonexistent user)")
        else:
            logger.warning("Actions endpoint returns %s", response.status_code)
            
    except Exception as e:
        logger.error("FAIL Error: %s", e)


def test_error_response_format():
    """Test that error responses are valid SVG"""
    logger.info("\n%s", "=" * 60)
    logger.info("TEST 4: Error Response Format")
    logger.info("%s", "=" * 60)
    
    url = f"{API_BASE}/api/stats?username=invalid_user_12345"
    
    try:
        response = requests.get(url, timeout=10)
        
        if response.status_code == 502 and "image/svg+xml" in response.headers.get("Content-Type", ""):
            content = response.text
            
            # Check if it's valid SVG
            if content.startswith("<svg") and "</svg>" in content:
                logger.info("PASS Error response is valid SVG")
                
                # Check for error indicators
                if "Error" in content or "error" in content.lower():
                    logger.info("  SVG contains error message")
                if "!" in content or "exclamation" in content.lower():
                    logger.info("  SVG contains error icon/indicator")
            else:
                logger.error("FAIL Response is not valid SVG")
                logger.error("  First 200 chars: %s", content[:200])
        else:
            logger.warning("Status %s, Content-Type: %s", response.status_code, response.headers.get('Content-Type'))
            
    except Exception as e:
        logger.error("FAIL Error: %s", e)


def test_cache_not_caching_errors():
    """Test that error responses are not cached"""
    logger.info("\n%s", "=" * 60)
    logger.info("TEST 5: Error Response Caching")
    logger.info("%s", "=" * 60)
    
    url = f"{API_BASE}/api/stats?username=nonexistent_user_cache_test"
    
    try:
        response1 = requests.get(url, timeout=10)
        cache_control_1 = response1.headers.get("Cache-Control")
        
        response2 = requests.get(url, timeout=10)
        cache_control_2 = response2.headers.get("Cache-Control")
        
        if "no-cache" in cache_control_1 or "no-store" in cache_control_1:
            logger.info("PASS Error responses are not cached")
            logger.info("  Cache-Control: %s", cache_control_1)
        else:
            logger.error("FAIL Error responses may be cached")
            logger.error("  Cache-Control: %s", cache_control_1)
            
    except Exception as e:
        logger.error("FAIL Error: %s", e)


def test_valid_user_returns_200():
    """Test that valid users still return 200 OK"""
    logger.info("\n%s", "=" * 60)
    logger.info("TEST 6: Valid User Returns Success")
    logger.info("%s", "=" * 60)
    
    # Using a well-known GitHub user
    url = f"{API_BASE}/api/stats?username=torvalds"
    
    try:
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            logger.info("PASS Valid user returns 200 OK")
            if "image/svg+xml" in response.headers.get("Content-Type", ""):
                logger.info("  Returns SVG content")
        else:
            logger.warning("Valid user returns %s", response.status_code)
            if response.status_code == 502:
                logger.error("  GitHub API might be rate-limited or unavailable")
            
    except Exception as e:
        logger.error("FAIL Error: %s", e)


if __name__ == "__main__":
    logger.info("\nGitCanvas Error Handling Test Suite")
    logger.info("Testing API error responses and exception handling")
    
    try:
        # Quick health check
        response = requests.get(f"{API_BASE}/", timeout=5)
        if response.status_code == 200:
            logger.info("PASS API is running at %s", API_BASE)
        else:
            logger.error("FAIL API health check failed: %s", response.status_code)
            exit(1)
    except Exception as e:
        logger.error("FAIL Cannot reach API at %s: %s", API_BASE, e)
        logger.error("Make sure the API is running: uvicorn api.main:app --reload")
        exit(1)
    
    # Run tests
    test_nonexistent_user()
    test_actions_without_auth()
    test_actions_with_auth()
    test_error_response_format()
    test_cache_not_caching_errors()
    test_valid_user_returns_200()
    
    logger.info("\n%s", "=" * 60)
    logger.info("Test suite complete!")
    logger.info("%s\n", "=" * 60)
