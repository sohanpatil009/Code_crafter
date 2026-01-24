#!/bin/bash

# Color codes for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

BASE_URL="http://localhost:5000"

echo "🧪 Testing Crop Disease Detection API"
echo "======================================"
echo ""

# Test 1: Health Check
echo -e "${YELLOW}Test 1: Health Check${NC}"
response=$(curl -s $BASE_URL/)
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Server is running${NC}"
    echo "$response" | python3 -m json.tool 2>/dev/null || echo "$response"
else
    echo -e "${RED}❌ Server is not responding${NC}"
fi
echo ""

# Test 2: Languages Endpoint
echo -e "${YELLOW}Test 2: Get Supported Languages${NC}"
response=$(curl -s $BASE_URL/api/languages)
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Languages endpoint working${NC}"
    echo "$response" | python3 -m json.tool 2>/dev/null || echo "$response"
else
    echo -e "${RED}❌ Languages endpoint failed${NC}"
fi
echo ""

# Test 3: TTS Generation
echo -e "${YELLOW}Test 3: Generate TTS Audio${NC}"
response=$(curl -s -X POST -H "Content-Type: application/json" \
  -d '{"text":"टमाटर में रोग पाया गया","language":"hi"}' \
  $BASE_URL/api/tts/generate)
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ TTS generation working${NC}"
    echo "$response" | python3 -m json.tool 2>/dev/null || echo "$response"
else
    echo -e "${RED}❌ TTS generation failed${NC}"
fi
echo ""

# Test 4: Prediction Endpoint (requires image)
echo -e "${YELLOW}Test 4: Disease Prediction${NC}"
if [ -f "test_image.jpg" ]; then
    response=$(curl -s -X POST -F "image=@test_image.jpg" -F "language=hi" \
      $BASE_URL/api/predict)
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Prediction endpoint working${NC}"
        echo "$response" | python3 -m json.tool 2>/dev/null || echo "$response"
    else
        echo -e "${RED}❌ Prediction endpoint failed${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  No test_image.jpg found - skipping prediction test${NC}"
    echo "To test prediction, add a test_image.jpg file and run:"
    echo "curl -X POST -F 'image=@test_image.jpg' -F 'language=hi' $BASE_URL/api/predict"
fi
echo ""

# Summary
echo "======================================"
echo -e "${GREEN}✅ API Testing Complete!${NC}"
echo ""
echo "📝 Next Steps:"
echo "1. If all tests passed, backend is ready"
echo "2. Update Android app BASE_URL to connect"
echo "3. Test from Android app"
echo ""
