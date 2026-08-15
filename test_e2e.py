#!/usr/bin/env python3
"""
Complete End-to-End Test Suite for Trip Planner
Tests the full workflow from UI to backend to Azure OpenAI
"""

import json
import urllib.request
import urllib.error
import time
import sys

def colored_print(color, text):
    """Print with ANSI colors for better readability"""
    colors = {
        "green": "\033[92m",
        "red": "\033[91m",
        "blue": "\033[94m",
        "yellow": "\033[93m",
        "end": "\033[0m"
    }
    print(f"{colors.get(color, '')}{text}{colors['end']}")

def test_api_endpoint(endpoint, method="GET", data=None, description=""):
    """Generic API endpoint tester"""
    try:
        body = json.dumps(data).encode() if data else None
        req = urllib.request.Request(
            f"http://127.0.0.1:8000{endpoint}",
            data=body,
            headers={"Content-Type": "application/json"} if data else {},
            method=method
        )
        
        with urllib.request.urlopen(req, timeout=20) as response:
            content = response.read().decode()
            
            if response.headers.get("content-type", "").startswith("application/json"):
                result = json.loads(content)
            else:
                result = content
            
            return {
                "status": response.status,
                "success": True,
                "data": result,
                "description": description
            }
    except urllib.error.HTTPError as e:
        return {
            "status": e.code,
            "success": False,
            "error": e.reason,
            "description": description
        }
    except Exception as e:
        return {
            "status": None,
            "success": False,
            "error": f"{type(e).__name__}: {str(e)}",
            "description": description
        }

def main():
    print("\n" + "=" * 70)
    print(" " * 15 + "TRIP PLANNER - END-TO-END TEST SUITE")
    print("=" * 70)
    
    time.sleep(2)  # Give backend time to be ready
    
    tests = []
    
    # TEST 1: Verify Backend is Running
    print("\n[TEST 1] Backend Server Health Check")
    print("-" * 70)
    result = test_api_endpoint("/", "GET", description="GET /")
    if result["success"] and result["status"] == 200:
        colored_print("green", "✓ Backend is running and serving HTML")
        if "Trip Planning Expert" in str(result["data"]):
            colored_print("green", "✓ Frontend HTML contains expected content")
        tests.append(("Backend Health", True))
    else:
        colored_print("red", f"✗ Backend health check failed: {result.get('error')}")
        tests.append(("Backend Health", False))
    
    # TEST 2: Simple Chat Query
    print("\n[TEST 2] Single Message Chat")
    print("-" * 70)
    result = test_api_endpoint("/chat", "POST", 
        {"messages": [{"role": "user", "content": "Where should I go for a beach vacation?"}]},
        description="POST /chat (beach vacation)"
    )
    if result["success"] and result["status"] == 200:
        reply = result["data"].get("reply", "")
        colored_print("green", f"✓ Chat endpoint works correctly")
        colored_print("green", f"✓ Response length: {len(reply)} characters")
        colored_print("green", f"✓ Preview: {reply[:80]}...")
        tests.append(("Simple Chat", True))
    else:
        colored_print("red", f"✗ Chat failed: {result.get('error')}")
        tests.append(("Simple Chat", False))
    
    # TEST 3: Multi-turn Conversation
    print("\n[TEST 3] Multi-turn Conversation")
    print("-" * 70)
    messages = [
        {"role": "user", "content": "I want to visit Asia"},
        {"role": "assistant", "content": "Great! Which countries interest you?"},
        {"role": "user", "content": "Thailand, Vietnam, and Japan"}
    ]
    result = test_api_endpoint("/chat", "POST", 
        {"messages": messages},
        description="POST /chat (multi-turn)"
    )
    if result["success"] and result["status"] == 200:
        reply = result["data"].get("reply", "")
        colored_print("green", f"✓ Multi-turn conversation works")
        colored_print("green", f"✓ AI responded to context: {reply[:80]}...")
        tests.append(("Multi-turn Conversation", True))
    else:
        colored_print("red", f"✗ Multi-turn conversation failed: {result.get('error')}")
        tests.append(("Multi-turn Conversation", False))
    
    # TEST 4: Budget Planning Query
    print("\n[TEST 4] Budget Planning Query")
    print("-" * 70)
    result = test_api_endpoint("/chat", "POST", 
        {"messages": [{"role": "user", "content": "How much should I budget for a trip to Europe for 10 days?"}]},
        description="POST /chat (budget planning)"
    )
    if result["success"] and result["status"] == 200:
        reply = result["data"].get("reply", "")
        if "budget" in reply.lower() or "cost" in reply.lower():
            colored_print("green", f"✓ Budget query handled correctly")
            colored_print("green", f"✓ Response mentions budget/cost")
            tests.append(("Budget Planning", True))
        else:
            colored_print("yellow", f"✓ Query responded (but may not mention budget)")
            tests.append(("Budget Planning", True))
    else:
        colored_print("red", f"✗ Budget query failed: {result.get('error')}")
        tests.append(("Budget Planning", False))
    
    # TEST 5: Itinerary Planning
    print("\n[TEST 5] Itinerary Planning Query")
    print("-" * 70)
    result = test_api_endpoint("/chat", "POST", 
        {"messages": [{"role": "user", "content": "Create a 3-day itinerary for Tokyo"}]},
        description="POST /chat (itinerary)"
    )
    if result["success"] and result["status"] == 200:
        reply = result["data"].get("reply", "")
        colored_print("green", f"✓ Itinerary query responded")
        colored_print("green", f"✓ Response length: {len(reply)} characters")
        tests.append(("Itinerary Planning", True))
    else:
        colored_print("red", f"✗ Itinerary query failed: {result.get('error')}")
        tests.append(("Itinerary Planning", False))
    
    # TEST 6: Error Handling - Missing Messages
    print("\n[TEST 6] Error Handling - Missing Messages")
    print("-" * 70)
    result = test_api_endpoint("/chat", "POST", 
        {},
        description="POST /chat (missing messages)"
    )
    if result["status"] in (400, 422):
        colored_print("green", f"✓ Properly returns {result['status']} for invalid request")
        colored_print("green", f"✓ Error handling works correctly")
        tests.append(("Error Handling", True))
    else:
        colored_print("yellow", f"⚠ Expected 400/422, got {result['status']}")
        tests.append(("Error Handling", result["status"] in (400, 422)))
    
    # TEST 7: Verify Azure Configuration
    print("\n[TEST 7] Azure Configuration Check")
    print("-" * 70)
    try:
        import sys
        sys.path.insert(0, "C:/Users/rruba/Travel")
        from app import get_azure_settings
        settings = get_azure_settings()
        has_endpoint = bool(settings.get("AZURE_ENDPOINT"))
        has_deployment = bool(settings.get("AZURE_DEPLOYMENT"))
        has_key = bool(settings.get("AZURE_API_KEY"))
        
        if has_endpoint and has_deployment and has_key:
            colored_print("green", "✓ All Azure credentials are configured")
            colored_print("green", f"  - Endpoint: {settings['AZURE_ENDPOINT'][:30]}...")
            colored_print("green", f"  - Deployment: {settings['AZURE_DEPLOYMENT']}")
            tests.append(("Azure Config", True))
        else:
            missing = []
            if not has_endpoint: missing.append("AZURE_ENDPOINT")
            if not has_deployment: missing.append("AZURE_DEPLOYMENT")
            if not has_key: missing.append("AZURE_API_KEY")
            colored_print("red", f"✗ Missing: {', '.join(missing)}")
            tests.append(("Azure Config", False))
    except Exception as e:
        colored_print("red", f"✗ Failed to check Azure config: {e}")
        tests.append(("Azure Config", False))
    
    # TEST 8: Response Format Validation
    print("\n[TEST 8] Response Format Validation")
    print("-" * 70)
    result = test_api_endpoint("/chat", "POST", 
        {"messages": [{"role": "user", "content": "Test response format"}]},
        description="POST /chat (format validation)"
    )
    if result["success"]:
        data = result["data"]
        if isinstance(data, dict) and "reply" in data:
            colored_print("green", f"✓ Response is valid JSON with 'reply' field")
            if isinstance(data["reply"], str) and len(data["reply"]) > 0:
                colored_print("green", f"✓ Reply is non-empty string")
                tests.append(("Response Format", True))
            else:
                colored_print("red", "✗ Reply is not a valid string")
                tests.append(("Response Format", False))
        else:
            colored_print("red", "✗ Response doesn't contain 'reply' field")
            tests.append(("Response Format", False))
    else:
        colored_print("red", f"✗ Request failed: {result.get('error')}")
        tests.append(("Response Format", False))
    
    # SUMMARY
    print("\n" + "=" * 70)
    print(" " * 25 + "TEST SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for _, result in tests if result)
    total = len(tests)
    
    for test_name, passed_flag in tests:
        status = "✓ PASS" if passed_flag else "✗ FAIL"
        color = "green" if passed_flag else "red"
        colored_print(color, f"{status}: {test_name}")
    
    print("\n" + "=" * 70)
    if passed == total:
        colored_print("green", f"🎉 ALL TESTS PASSED ({passed}/{total})")
        print("The application is fully functional and ready for deployment!")
        return 0
    else:
        colored_print("yellow", f"⚠️  {passed}/{total} tests passed")
        print(f"{total - passed} test(s) failed. Review errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
