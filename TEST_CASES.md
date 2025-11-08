# Test Cases for Vietnam Travel Chatbot

## Overview
This document outlines test cases to validate all functional requirements (FR1-FR7) and non-functional requirements (NFR1-NFR4) from the SRS.

---

## FR1: Multilingual Support

### TC1.1: Vietnamese Question & Response
**Objective**: Verify bot responds in Vietnamese when asked in Vietnamese

**Test Steps**:
1. Start the application
2. Enter question: "Thời tiết ở Sa Pa tháng 12 như thế nào?"
3. Wait for response

**Expected Result**:
- Bot responds in Vietnamese
- Answer contains weather information about Sapa in December
- Response mentions cold temperatures (0-5°C)

**Pass Criteria**: ✅ Response is in Vietnamese with relevant content

---

### TC1.2: English Question & Response
**Objective**: Verify bot responds in English when asked in English

**Test Steps**:
1. Clear chat history
2. Enter question: "What is the best time to visit Ha Long Bay?"
3. Wait for response

**Expected Result**:
- Bot responds in English
- Answer mentions March-May or September-November
- Content is relevant to Ha Long Bay

**Pass Criteria**: ✅ Response is in English with relevant content

---

### TC1.3: Language Switch Within Conversation
**Objective**: Verify bot adapts to language changes

**Test Steps**:
1. Ask in English: "Tell me about Hanoi"
2. Follow up in Vietnamese: "Ẩm thực ở đó có gì đặc sắc?"
3. Follow up in English: "What about accommodation?"

**Expected Result**:
- First response in English
- Second response in Vietnamese
- Third response in English
- Context maintained across language switches

**Pass Criteria**: ✅ Bot matches language in each response

---

## FR2: Q&A System

### TC2.1: Destination Information Query
**Objective**: Verify accurate retrieval of destination info

**Test Steps**:
1. Ask: "Tell me about Hoi An Ancient Town"
2. Wait for response

**Expected Result**:
- Response mentions UNESCO Heritage Site
- Contains information about lanterns, old town, Japanese Bridge
- Information matches mock data

**Pass Criteria**: ✅ Accurate information retrieved from vector store

---

### TC2.2: Food Information Query
**Objective**: Verify accurate retrieval of food info

**Test Steps**:
1. Ask: "What is Pho and where did it originate?"
2. Wait for response

**Expected Result**:
- Response explains Pho (rice noodles, broth, beef/chicken)
- Mentions Hanoi origin in early 20th century
- May reference French influence

**Pass Criteria**: ✅ Accurate information about Pho

---

### TC2.3: Cultural Information Query
**Objective**: Verify cultural knowledge retrieval

**Test Steps**:
1. Ask: "What is water puppetry?"
2. Wait for response

**Expected Result**:
- Response explains water puppet tradition
- Mentions 1000+ years history
- May reference Thang Long Theatre

**Pass Criteria**: ✅ Accurate cultural information

---

## FR3: Recommendations

### TC3.1: Destination Recommendations
**Objective**: Verify bot can recommend destinations

**Test Steps**:
1. Ask: "Recommend the best beaches in Vietnam"
2. Wait for response

**Expected Result**:
- Response lists multiple beaches (e.g., My Khe, Nha Trang, Phu Quoc)
- Includes brief descriptions
- Suggestions are relevant

**Pass Criteria**: ✅ Multiple relevant beach recommendations provided

---

### TC3.2: Food Recommendations
**Objective**: Verify food recommendation capability

**Test Steps**:
1. Ask: "Recommend traditional Vietnamese dishes I should try"
2. Wait for response

**Expected Result**:
- Response lists multiple dishes (Pho, Banh Mi, Bun Cha, etc.)
- Brief description of each
- Relevant suggestions

**Pass Criteria**: ✅ Multiple relevant food recommendations

---

### TC3.3: Itinerary Suggestions
**Objective**: Verify itinerary planning capability

**Test Steps**:
1. Ask: "Create a 2-day itinerary for Da Nang"
2. Wait for response

**Expected Result**:
- Response provides structured itinerary
- Includes multiple attractions (My Khe Beach, Ba Na Hills, etc.)
- Logical day-by-day plan

**Pass Criteria**: ✅ Coherent itinerary with multiple activities

---

## FR4: Function Calling - External Links

### TC4.1: Restaurant Links via Function Call
**Objective**: Verify function calling retrieves restaurant links

**Test Steps**:
1. Ask: "Recommend good pho restaurants in Hanoi"
2. Wait for response
3. Check for external links

**Expected Result**:
- Response includes restaurant recommendations
- **Function call triggered** (get_external_links)
- Links displayed (Google Maps, reviews, etc.)
- At least 1-2 external links visible

**Pass Criteria**: ✅ Function called, links displayed

---

### TC4.2: Destination Links via Function Call
**Objective**: Verify function calling for destination links

**Test Steps**:
1. Ask: "Show me information about Ha Long Bay with links"
2. Wait for response

**Expected Result**:
- Response about Ha Long Bay
- Function call triggered
- Links to Google Maps, TripAdvisor, YouTube visible

**Pass Criteria**: ✅ Function called, multiple link types shown

---

### TC4.3: Cultural Activity Links
**Objective**: Verify links for cultural activities

**Test Steps**:
1. Ask: "Where can I see water puppet shows in Hanoi?"
2. Wait for response

**Expected Result**:
- Response mentions water puppet theatres
- Function call retrieves links
- Google Maps link to Thang Long Theatre
- Booking/review links provided

**Pass Criteria**: ✅ Relevant cultural activity links displayed

---

## FR5: Conversation Management

### TC5.1: Chat History Maintained
**Objective**: Verify conversation history is preserved

**Test Steps**:
1. Ask: "What is special about Hoi An?"
2. Wait for response
3. Ask follow-up: "What's the weather like there?"
4. Wait for response

**Expected Result**:
- Second question understands "there" refers to "Hoi An"
- Response provides Hoi An weather information
- Context from previous message maintained

**Pass Criteria**: ✅ Context-aware response

---

### TC5.2: Follow-up Question Suggestions
**Objective**: Verify follow-up questions are generated

**Test Steps**:
1. Ask any question about a destination
2. Wait for response
3. Observe UI below response

**Expected Result**:
- 2-3 follow-up questions displayed as buttons
- Questions are relevant to the topic
- Questions are in the same language as response

**Pass Criteria**: ✅ 2-3 relevant follow-up questions shown

---

### TC5.3: Follow-up Button Functionality
**Objective**: Verify clicking follow-up buttons works

**Test Steps**:
1. Ask: "Tell me about Sapa"
2. Wait for response and follow-up suggestions
3. Click one of the suggested questions
4. Wait for response

**Expected Result**:
- Clicking button submits that question
- New response generated
- New follow-up questions appear

**Pass Criteria**: ✅ Follow-up buttons work correctly

---

## FR6: Text-to-Speech

### TC6.1: TTS Button Appears
**Objective**: Verify TTS button is displayed

**Test Steps**:
1. Ensure HUGGINGFACE_API_KEY is set in .env
2. Ask any question
3. Wait for bot response
4. Observe response area

**Expected Result**:
- 🔊 icon/button appears next to bot response
- Button is clickable

**Pass Criteria**: ✅ TTS button visible

---

### TC6.2: TTS Vietnamese Playback
**Objective**: Verify Vietnamese TTS works

**Test Steps**:
1. Ask in Vietnamese: "Phở là gì?"
2. Wait for Vietnamese response
3. Click 🔊 button

**Expected Result**:
- Audio generation starts (spinner/loading)
- Audio plays automatically or with player controls
- Speech is in Vietnamese
- Speech is clear and understandable

**Pass Criteria**: ✅ Vietnamese audio plays correctly

---

### TC6.3: TTS English Playback
**Objective**: Verify English TTS works

**Test Steps**:
1. Ask in English: "What is Banh Mi?"
2. Wait for English response
3. Click 🔊 button

**Expected Result**:
- Audio generation starts
- Audio plays in English
- Speech is clear and understandable

**Pass Criteria**: ✅ English audio plays correctly

---

## FR7: User Interface

### TC7.1: Chat Interface Layout
**Objective**: Verify UI components are present

**Test Steps**:
1. Launch application
2. Observe interface

**Expected Result**:
- Title: "Vietnam Travel Chatbot" visible
- Chat history area visible
- Input box at bottom
- Sidebar with examples and settings
- Clean, organized layout

**Pass Criteria**: ✅ All UI elements present and organized

---

### TC7.2: Message Display
**Objective**: Verify messages display correctly

**Test Steps**:
1. Send several messages
2. Observe chat area

**Expected Result**:
- User messages aligned appropriately
- Bot messages distinguished from user messages
- Messages readable with proper formatting
- Markdown rendering works (bold, lists, etc.)

**Pass Criteria**: ✅ Messages display cleanly

---

### TC7.3: Example Questions
**Objective**: Verify example questions work

**Test Steps**:
1. Open sidebar
2. Expand "English Examples" or "Vietnamese Examples"
3. Click an example question

**Expected Result**:
- Question is submitted automatically
- Bot responds to the example question

**Pass Criteria**: ✅ Example questions functional

---

### TC7.4: Clear Chat History
**Objective**: Verify history clearing works

**Test Steps**:
1. Have several messages in chat
2. Click "Clear Chat History" in sidebar
3. Observe interface

**Expected Result**:
- All messages cleared
- Chat area empty
- Ready for new conversation

**Pass Criteria**: ✅ History cleared successfully

---

## Non-Functional Requirements

### NFR1: Performance - Response Time
**Objective**: Verify response time < 5 seconds

**Test Steps**:
1. Ask 5 different questions
2. Measure time from submission to full response display

**Expected Result**:
- Average response time < 5 seconds
- Maximum response time < 8 seconds
- System feels responsive

**Pass Criteria**: ✅ Meets performance target

---

### NFR2: Usability
**Objective**: Verify interface is intuitive

**Test Steps**:
1. Have a new user try the application
2. Observe without instruction

**Expected Result**:
- User can figure out how to ask questions
- Example questions are helpful
- Clear where to type
- No confusion about functionality

**Pass Criteria**: ✅ Interface is intuitive

---

### NFR3: Reliability - Answer Accuracy
**Objective**: Verify answers are accurate

**Test Steps**:
1. Ask 10 factual questions from mock data
2. Compare responses with source data

**Expected Result**:
- At least 8/10 answers are accurate
- No hallucinations (making up facts)
- Information matches mock data

**Pass Criteria**: ✅ 80%+ accuracy rate

---

### NFR4: TTS Voice Quality
**Objective**: Verify TTS voices are natural

**Test Steps**:
1. Generate Vietnamese TTS
2. Generate English TTS
3. Listen to both

**Expected Result**:
- Speech is clear and understandable
- Pronunciation is correct
- Natural intonation (not robotic)

**Pass Criteria**: ✅ TTS quality is acceptable

---

## Integration Tests

### INT1: End-to-End RAG Flow
**Objective**: Verify complete RAG pipeline

**Test Steps**:
1. Ask: "What are the best months to visit Vietnam?"
2. Observe backend logs (if available)

**Expected Result**:
- Query is embedded
- Pinecone retrieval occurs
- Context added to prompt
- LLM generates response
- Response displayed

**Pass Criteria**: ✅ Complete RAG flow works

---

### INT2: RAG + Function Calling
**Objective**: Verify RAG and Function Calling together

**Test Steps**:
1. Ask: "Tell me about Bun Cha and where to eat it"
2. Observe response

**Expected Result**:
- RAG retrieves Bun Cha information
- Function call retrieves restaurant links
- Combined response with info + links

**Pass Criteria**: ✅ RAG and function calling work together

---

### INT3: Full Conversation Flow
**Objective**: Verify complete conversation experience

**Test Steps**:
1. Ask about a destination
2. Click follow-up question
3. Ask for recommendations
4. Use TTS on response
5. Switch language

**Expected Result**:
- All features work seamlessly
- Context maintained
- No errors
- Smooth user experience

**Pass Criteria**: ✅ All features work together

---

## Summary Checklist

- [ ] TC1.1: Vietnamese Q&A
- [ ] TC1.2: English Q&A
- [ ] TC1.3: Language switching
- [ ] TC2.1: Destination info
- [ ] TC2.2: Food info
- [ ] TC2.3: Cultural info
- [ ] TC3.1: Destination recommendations
- [ ] TC3.2: Food recommendations
- [ ] TC3.3: Itinerary suggestions
- [ ] TC4.1: Restaurant links (Function Call)
- [ ] TC4.2: Destination links (Function Call)
- [ ] TC4.3: Cultural activity links
- [ ] TC5.1: Chat history maintained
- [ ] TC5.2: Follow-up suggestions generated
- [ ] TC5.3: Follow-up buttons work
- [ ] TC6.1: TTS button appears
- [ ] TC6.2: Vietnamese TTS works
- [ ] TC6.3: English TTS works
- [ ] TC7.1: UI layout complete
- [ ] TC7.2: Message display correct
- [ ] TC7.3: Example questions work
- [ ] TC7.4: Clear history works
- [ ] NFR1: Performance acceptable
- [ ] NFR2: Interface intuitive
- [ ] NFR3: Answers accurate
- [ ] NFR4: TTS quality good
- [ ] INT1: RAG flow complete
- [ ] INT2: RAG + Function Calling
- [ ] INT3: Full conversation flow

---

## Testing Notes

### Before Testing
1. Ensure `.env` file is properly configured
2. Run `python ingest_data.py` to populate Pinecone
3. Verify all API keys are valid
4. Check internet connectivity

### During Testing
1. Monitor console/logs for errors
2. Take screenshots of failures
3. Note any unexpected behavior
4. Record response times

### After Testing
1. Document all failures
2. Categorize issues (critical, major, minor)
3. Create fix priority list
4. Retest after fixes

