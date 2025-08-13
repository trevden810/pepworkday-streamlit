#!/usr/bin/env python3
"""
Test runner script for the Streamlit application.

This script provides various options for running tests including:
- All tests
- Specific test categories
- Coverage reports
- Verbose output

Usage:
    python run_tests.py                    # Run all tests
    python run_tests.py --unit             # Run only unit tests
    python run_tests.py --integration      # Run only integration tests
    python run_tests.py --coverage         # Run tests with coverage report
    python run_tests.py --verbose          # Run tests with verbose output
"""

import sys
import subprocess
import argparse
from pathlib import Path


def run_command(command, description=""):
    """Run a command and handle errors."""
    print(f"\n{'='*60}")
    if description:
        print(f"Running: {description}")
    print(f"Command: {' '.join(command)}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(command, check=True, capture_output=False)
        print(f"\n✅ {description or 'Command'} completed successfully!")
        return result.returncode
    except subprocess.CalledProcessError as e:
        print(f"\n❌ {description or 'Command'} failed with exit code {e.returncode}")
        return e.returncode
    except FileNotFoundError:
        print(f"\n❌ Command not found: {command[0]}")
        print("Make sure pytest is installed: pip install pytest")
        return 1


def check_pytest_installation():
    """Check if pytest is installed."""
    try:
        subprocess.run([sys.executable, "-m", "pytest", "--version"], 
                      check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def install_test_dependencies():
    """Install test dependencies if not present."""
    print("Installing test dependencies...")
    dependencies = [
        "pytest>=7.4.0",
        "pytest-cov>=4.1.0", 
        "pytest-mock>=3.11.0",
        "pytest-timeout>=2.1.0"
    ]
    
    for dep in dependencies:
        command = [sys.executable, "-m", "pip", "install", dep]
        result = run_command(command, f"Installing {dep}")
        if result != 0:
            return False
    return True


def main():
    """Main test runner function."""
    parser = argparse.ArgumentParser(description="Run tests for the Streamlit application")
    parser.add_argument("--unit", action="store_true", help="Run only unit tests")
    parser.add_argument("--integration", action="store_true", help="Run only integration tests")
    parser.add_argument("--csv", action="store_true", help="Run only CSV-related tests")
    parser.add_argument("--merge", action="store_true", help="Run only merge-related tests")
    parser.add_argument("--coverage", action="store_true", help="Run tests with coverage report")
    parser.add_argument("--verbose", action="store_true", help="Run tests with verbose output")
    parser.add_argument("--install-deps", action="store_true", help="Install test dependencies")
    parser.add_argument("--file", type=str, help="Run specific test file")
    parser.add_argument("--function", type=str, help="Run specific test function")
    
    args = parser.parse_args()
    
    # Install dependencies if requested
    if args.install_deps:
        if not install_test_dependencies():
            print("❌ Failed to install test dependencies")
            return 1
        print("✅ Test dependencies installed successfully")
    
    # Check if pytest is available
    if not check_pytest_installation():
        print("❌ pytest is not installed.")
        print("Install it with: pip install pytest")
        print("Or run: python run_tests.py --install-deps")
        return 1
    
    # Build pytest command
    command = [sys.executable, "-m", "pytest"]
    
    # Add test directory
    test_dir = Path("tests")
    if test_dir.exists():
        command.append(str(test_dir))
    else:
        print(f"❌ Test directory '{test_dir}' not found")
        return 1
    
    # Add specific file if requested
    if args.file:
        command = [sys.executable, "-m", "pytest", args.file]
    
    # Add specific function if requested
    if args.function:
        if args.file:
            command.append(f"::{args.function}")
        else:
            command.extend(["-k", args.function])
    
    # Add marker-based filtering
    markers = []
    if args.unit:
        markers.append("unit")
    if args.integration:
        markers.append("integration")
    if args.csv:
        markers.append("csv")
    if args.merge:
        markers.append("merge")
    
    if markers:
        command.extend(["-m", " or ".join(markers)])
    
    # Add coverage if requested
    if args.coverage:
        command.extend([
            "--cov=data_loader",
            "--cov=app", 
            "--cov-report=html",
            "--cov-report=term-missing",
            "--cov-report=xml"
        ])
    
    # Add verbose output if requested
    if args.verbose:
        command.append("-v")
    else:
        command.append("-v")  # Always use verbose by default
    
    # Add other useful options
    command.extend([
        "--tb=short",
        "--color=yes",
        "--durations=10"
    ])
    
    # Run the tests
    description = "Running tests"
    if markers:
        description += f" (markers: {', '.join(markers)})"
    if args.coverage:
        description += " with coverage"
    
    exit_code = run_command(command, description)
    
    # Show coverage report location if generated
    if args.coverage and exit_code == 0:
        print(f"\n📊 Coverage report generated:")
        print(f"   HTML: file://{Path.cwd()}/htmlcov/index.html")
        print(f"   XML:  {Path.cwd()}/coverage.xml")
    
    return exit_code


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
