#!/bin/bash

# EPL Defense API - Development Scripts
# Provides convenient commands for development, testing, and deployment

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}🚀${NC} $1"
}

print_success() {
    echo -e "${GREEN}✅${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠️${NC} $1"
}

print_error() {
    echo -e "${RED}❌${NC} $1"
}

# Function to show help
show_help() {
    echo "EPL Defense API - Available Commands:"
    echo "======================================"
    echo "setup-dev      - Set up development environment"
    echo "install        - Install production dependencies"
    echo "install-dev    - Install development dependencies"
    echo "test           - Run all tests"
    echo "test-coverage  - Run tests with coverage"
    echo "lint           - Run linting checks"
    echo "format         - Format code"
    echo "run            - Run the FastAPI application"
    echo "dev            - Run in development mode"
    echo "database       - Initialize database"
    echo "clean          - Clean build artifacts"
    echo "status         - Show project status"
    echo "help           - Show this help message"
}

# Function to check if virtual environment is active
check_venv() {
    if [[ "$VIRTUAL_ENV" == "" ]]; then
        print_warning "Virtual environment not active. Activating .venv..."
        source .venv/bin/activate
    fi
}

# Function to setup development environment
setup_dev() {
    print_status "Setting up development environment..."
    
    if [ ! -d ".venv" ]; then
        python3 -m venv .venv
        print_success "Virtual environment created"
    fi
    
    source .venv/bin/activate
    pip install --upgrade pip
    pip install -e .
    pip install -e ".[dev]"
    
    print_success "Development environment ready!"
}

# Function to install dependencies
install_deps() {
    check_venv
    print_status "Installing dependencies..."
    pip install -e ".[dev]"
    print_success "Dependencies installed!"
}

# Function to run tests
run_tests() {
    check_venv
    print_status "Running tests..."
    
    if [ "$1" = "coverage" ]; then
        python -m pytest tests/ --cov=app --cov-report=term-missing --cov-report=html
    else
        python -m pytest tests/ -v
    fi
}

# Function to run linting
run_lint() {
    check_venv
    print_status "Running linting checks..."
    
    if command -v flake8 &> /dev/null; then
        flake8 app/ tests/
    else
        print_warning "flake8 not found, skipping..."
    fi
    
    if command -v pylint &> /dev/null; then
        pylint app/ tests/ || true
    else
        print_warning "pylint not found, skipping..."
    fi
}

# Function to format code
format_code() {
    check_venv
    print_status "Formatting code..."
    
    if command -v black &> /dev/null; then
        black app/ tests/
    else
        print_warning "black not found, skipping..."
    fi
    
    if command -v isort &> /dev/null; then
        isort app/ tests/
    else
        print_warning "isort not found, skipping..."
    fi
}

# Function to run the application
run_app() {
    check_venv
    print_status "Starting FastAPI application..."
    
    if [ "$1" = "prod" ]; then
        uvicorn app.main:app --host 0.0.0.0 --port 8001
    else
        uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
    fi
}

# Function to initialize database
init_database() {
    check_venv
    print_status "Initializing database..."
    python init_database.py
    print_success "Database initialized!"
}

# Function to clean build artifacts
clean_artifacts() {
    print_status "Cleaning build artifacts..."
    
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find . -type f -name "*.pyc" -delete 2>/dev/null || true
    find . -type f -name "*.pyo" -delete 2>/dev/null || true
    find . -type f -name "*.pyd" -delete 2>/dev/null || true
    rm -rf .pytest_cache/ 2>/dev/null || true
    rm -rf .coverage 2>/dev/null || true
    rm -rf htmlcov/ 2>/dev/null || true
    rm -rf dist/ 2>/dev/null || true
    rm -rf build/ 2>/dev/null || true
    rm -rf *.egg-info/ 2>/dev/null || true
    
    print_success "Cleanup complete!"
}

# Function to show project status
show_status() {
    echo "📊 EPL Defense API - Project Status"
    echo "=================================="
    echo "Python version: $(python --version 2>&1 || echo 'Not found')"
    
    if [ -d ".venv" ]; then
        echo "Virtual env: ✅ Found"
    else
        echo "Virtual env: ❌ Not found"
    fi
    
    if [ -f "epl_defense.db" ]; then
        echo "Database: ✅ Found"
    else
        echo "Database: ❌ Not found"
    fi
    
    if [ -d ".venv" ] && [ -f ".venv/bin/pip" ]; then
        echo "Dependencies: ✅ Installed"
    else
        echo "Dependencies: ❌ Not installed"
    fi
}

# Main script logic
case "${1:-help}" in
    "setup-dev")
        setup_dev
        ;;
    "install")
        install_deps
        ;;
    "install-dev")
        install_deps
        ;;
    "test")
        run_tests
        ;;
    "test-coverage")
        run_tests coverage
        ;;
    "lint")
        run_lint
        ;;
    "format")
        format_code
        ;;
    "run")
        run_app
        ;;
    "dev")
        run_app
        ;;
    "run-prod")
        run_app prod
        ;;
    "database")
        init_database
        ;;
    "clean")
        clean_artifacts
        ;;
    "status")
        show_status
        ;;
    "help"|*)
        show_help
        ;;
esac
