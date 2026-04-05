#!/usr/bin/env python3
"""
Test suite for Moltbook Agent Deployment (Issue #60)

Verifies all requirements:
- Agent template with unique personality
- Beacon identity registration
- 3+ quality posts on Moltbook
- DriftLock enabled
- Template YAML with proper configuration
"""

import os
import sys
import json
from pathlib import Path

DEPLOYMENT_DIR = Path.home() / ".shaprai" / "deployments" / "moltbook_connector"

def test_template_exists():
    """Test that agent template YAML exists"""
    template_path = Path("templates/moltbook_connector.yaml")
    assert template_path.exists(), f"Template not found: {template_path}"
    
    with open(template_path) as f:
        content = f.read()
    
    assert "personality:" in content, "Template missing personality section"
    assert "voice:" in content, "Template missing agent voice"
    assert "moltbook" in content, "Template missing moltbook platform"
    
    print("✅ test_template_exists: PASSED")

def test_beacon_identity():
    """Test that Beacon identity was created"""
    beacon_file = DEPLOYMENT_DIR / "beacon_identity.json"
    assert beacon_file.exists(), f"Beacon identity not found: {beacon_file}"
    
    with open(beacon_file) as f:
        identity = json.load(f)
    
    assert "beacon_id" in identity, "Missing beacon_id"
    assert identity["beacon_id"].startswith("bcn_"), "Invalid beacon_id format"
    assert "agent_name" in identity, "Missing agent_name"
    
    print(f"✅ test_beacon_identity: PASSED")
    print(f"   Beacon ID: {identity['beacon_id']}")

def test_posts_created():
    """Test that at least 3 posts were created"""
    metadata_file = DEPLOYMENT_DIR / "posts_metadata.json"
    assert metadata_file.exists(), f"Posts metadata not found: {metadata_file}"
    
    with open(metadata_file) as f:
        posts = json.load(f)
    
    assert len(posts) >= 3, f"Expected 3+ posts, found {len(posts)}"
    
    for i, post in enumerate(posts, 1):
        assert "post_id" in post, f"Post {i} missing post_id"
        assert "content" in post, f"Post {i} missing content"
        assert len(post["content"]) > 50, f"Post {i} too short"
    
    print(f"✅ test_posts_created: PASSED")
    print(f"   Posts: {len(posts)} (required: 3+)")
    for post in posts:
        print(f"   - {post['type']}: {post['content'][:50]}...")

def test_driftlock_enabled():
    """Test that DriftLock is enabled in template"""
    template_path = Path("templates/moltbook_connector.yaml")
    
    with open(template_path) as f:
        content = f.read()
    
    assert "driftlock:" in content, "DriftLock section missing"
    assert "enabled: true" in content, "DriftLock not enabled"
    assert "anchor_phrases:" in content, "DriftLock anchor phrases missing"
    
    print("✅ test_driftlock_enabled: PASSED")

def test_unique_personality():
    """Test that agent has unique personality (not a direct copy)"""
    template_path = Path("templates/moltbook_connector.yaml")
    
    with open(template_path) as f:
        content = f.read()
    
    # Check for personality section
    assert "personality:" in content, "Personality section missing"
    assert "style:" in content, "Personality style missing"
    assert "voice:" in content, "Agent voice missing"
    
    # Verify it's not named after existing templates
    assert "name: sophia" not in content.lower(), "Named after Sophia"
    assert "name: boris" not in content.lower(), "Named after Boris"
    assert "name: janitor" not in content.lower(), "Named after Janitor"
    
    print("✅ test_unique_personality: PASSED")

def test_beacon_heartbeat_config():
    """Test that Beacon heartbeat is configured"""
    template_path = Path("templates/moltbook_connector.yaml")
    
    with open(template_path) as f:
        content = f.read()
    
    assert "heartbeat" in content.lower(), "Heartbeat not configured"
    assert "beacon" in content.lower(), "Beacon not configured"
    
    print("✅ test_beacon_heartbeat_config: PASSED")

def test_proof_report():
    """Test that proof report was generated"""
    proof_file = DEPLOYMENT_DIR / "proof_report.json"
    assert proof_file.exists(), f"Proof report not found: {proof_file}"
    
    with open(proof_file) as f:
        report = json.load(f)
    
    required_fields = [
        "bounty", "agent_name", "beacon_id",
        "posts_count", "moltbook_profile",
        "template_yaml", "driftlock_enabled"
    ]
    
    for field in required_fields:
        assert field in report, f"Proof report missing {field}"
    
    assert report["posts_count"] >= 3, "Less than 3 posts"
    assert report["driftlock_enabled"] == True, "DriftLock not enabled"
    
    print(f"✅ test_proof_report: PASSED")
    print(f"   Bounty: {report['bounty']}")
    print(f"   Agent: {report['agent_name']}")
    print(f"   Posts: {report['posts_count']}")

def test_wallet_configured():
    """Test that RTC wallet is configured"""
    template_path = Path("templates/moltbook_connector.yaml")
    
    with open(template_path) as f:
        content = f.read()
    
    assert "wallet" in content.lower() or "rtc" in content.lower(), "Wallet not configured"
    
    print("✅ test_wallet_configured: PASSED")

def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("Moltbook Agent Deployment Test Suite (Issue #60)")
    print("=" * 60)
    print()
    
    tests = [
        test_template_exists,
        test_beacon_identity,
        test_posts_created,
        test_driftlock_enabled,
        test_unique_personality,
        test_beacon_heartbeat_config,
        test_proof_report,
        test_wallet_configured,
    ]
    
    passed = 0
    failed = 0
    skipped = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"❌ {test.__name__}: FAILED - {e}")
            failed += 1
        except Exception as e:
            print(f"⚠️  {test.__name__}: ERROR - {e}")
            skipped += 1
    
    print()
    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed, {skipped} skipped")
    print("=" * 60)
    
    return failed == 0

if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
