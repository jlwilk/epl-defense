#!/usr/bin/env python3
"""
Test runner script for the EPL Defense API.
"""

import subprocess
import sys
import os


def run_tests(test_type="all", coverage=True, verbose=True):
    """Run tests with specified options."""
    
    # Base pytest command
    cmd = ["python", "-m", "pytest"]
    
    # Add coverage if requested
    if coverage:
        cmd.extend(["--cov=app", "--cov-report=term-missing"])
    
    # Add verbosity if requested
    if verbose:
        cmd.append("-v")
    
    # Add test type filters
    if test_type == "unit":
        cmd.extend(["-m", "unit"])
    elif test_type == "integration":
        cmd.extend(["-m", "integration"])
    elif test_type == "fast":
        cmd.extend(["-m", "not slow"])
    
    # Add test discovery
    cmd.append("tests/")
    
    print(f"Running tests with command: {' '.join(cmd)}")
    print("-" * 60)
    
    try:
        result = subprocess.run(cmd, check=True)
        print("-" * 60)
        print("✅ All tests passed!")
        return True
    except subprocess.CalledProcessError as e:
        print("-" * 60)
        print(f"❌ Tests failed with exit code {e.returncode}")
        return False


def main():
    """Main test runner function."""
    
    if len(sys.argv) > 1:
        test_type = sys.argv[1]
    else:
        test_type = "all"
    
    print("🏃‍♂️ EPL Defense API Test Runner")
    print("=" * 60)
    
    # Validate test type
    valid_types = ["all", "unit", "integration", "fast"]
    if test_type not in valid_types:
        print(f"❌ Invalid test type: {test_type}")
        print(f"Valid types: {', '.join(valid_types)}")
        sys.exit(1)
    
    print(f"📋 Test type: {test_type}")
    
    # Check if we're in the right directory
    if not os.path.exists("tests/"):
        print("❌ Tests directory not found. Please run from the project root.")
        sys.exit(1)
    
    # Run tests
    success = run_tests(test_type)
    
    if success:
        print("🎉 Test run completed successfully!")
        sys.exit(0)
    else:
        print("💥 Test run failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()



