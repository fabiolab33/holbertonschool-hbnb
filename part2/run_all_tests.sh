#!/bin/bash

# HBnB API Complete Test Suite Runner
# This script runs all tests: unit tests and integration tests

echo "============================================"
echo "HBnB API - Complete Test Suite"
echo "============================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if server is running
echo "Checking if API server is running..."
if ! curl -s http://localhost:5001/api/users > /dev/null 2>&1; then
    echo -e "${RED}❌ ERROR: Server is not running on port 5001${NC}"
    echo ""
    echo "Please start the server in another terminal:"
    echo "  cd part2"
    echo "  source venv/bin/activate"
    echo "  python3 run.py"
    echo ""
    exit 1
fi

echo -e "${GREEN}✅ Server is running on port 5001${NC}"
echo ""

# Run pytest unit tests
echo "============================================"
echo "PART 1: Unit Tests (pytest)"
echo "============================================"
echo ""

if command -v pytest &> /dev/null; then
    pytest tests/test_models.py -v --tb=short
    PYTEST_EXIT_CODE=$?
    echo ""
    
    if [ $PYTEST_EXIT_CODE -eq 0 ]; then
        echo -e "${GREEN}✅ All unit tests passed!${NC}"
    else
        echo -e "${RED}❌ Some unit tests failed${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  pytest not installed. Skipping unit tests.${NC}"
    echo "Install with: pip install pytest"
    PYTEST_EXIT_CODE=1
fi

echo ""
echo "============================================"
echo "PART 2: Integration Tests (API with cURL)"
echo "============================================"
echo ""

# Run the automated integration test script
if [ -f "test_api.py" ]; then
    python3 test_api.py
    API_TEST_EXIT_CODE=$?
    echo ""
    
    if [ $API_TEST_EXIT_CODE -eq 0 ]; then
        echo -e "${GREEN}✅ All integration tests passed!${NC}"
    else
        echo -e "${YELLOW}⚠️  Check integration test results above${NC}"
    fi
else
    echo -e "${RED}❌ test_api.py not found${NC}"
    API_TEST_EXIT_CODE=1
fi

echo ""
echo "============================================"
echo "Test Suite Summary"
echo "============================================"
echo ""

if [ $PYTEST_EXIT_CODE -eq 0 ] && [ $API_TEST_EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✅ ALL TESTS PASSED!${NC}"
    echo ""
    echo "Your HBnB API is working correctly!"
else
    echo -e "${YELLOW}⚠️  Some tests need attention${NC}"
    echo ""
    if [ $PYTEST_EXIT_CODE -ne 0 ]; then
        echo "  - Unit tests: FAILED"
    else
        echo "  - Unit tests: PASSED"
    fi
    
    if [ $API_TEST_EXIT_CODE -ne 0 ]; then
        echo "  - Integration tests: CHECK RESULTS"
    else
        echo "  - Integration tests: PASSED"
    fi
fi

echo ""
echo "============================================"
echo "Additional Resources"
echo "============================================"
echo ""
echo "📚 Swagger Documentation:"
echo "   http://localhost:5001/api/docs"
echo ""
echo "🧪 To run only unit tests:"
echo "   pytest tests/test_models.py -v"
echo ""
echo "🔍 To run only integration tests:"
echo "   python3 test_api.py"
echo ""
echo "📊 To run tests with coverage:"
echo "   pytest tests/test_models.py --cov=app/business --cov-report=html"
echo "   Then open: htmlcov/index.html"
echo ""