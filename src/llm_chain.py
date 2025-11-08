"""Langchain LLM Chain with Azure OpenAI and Function Calling"""

import os
import json
from typing import List, Dict, Any, Optional
from langchain_openai import AzureChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from langchain.schema.runnable import RunnablePassthrough, RunnableParallel
from langchain.schema.output_parser import StrOutputParser

from src.vector_store import VectorStoreManager
from src.function_calls import (
    get_external_links, 
    GET_EXTERNAL_LINKS_SCHEMA,
    AVAILABLE_FUNCTIONS
)


class LLMChainManager:
    """Manages LLM chain with RAG and Function Calling"""
    
    def __init__(self, vector_store_manager: VectorStoreManager):
        """Initialize LLM and chain components
        
        Args:
            vector_store_manager: VectorStoreManager instance
        """
        self.vector_store_manager = vector_store_manager
        
        # Initialize Azure OpenAI LLM
        self.llm = AzureChatOpenAI(
            azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            temperature=float(os.getenv("TEMPERATURE", "0.7")),
            max_tokens=int(os.getenv("MAX_TOKENS", "1000"))
        )
        
        # LLM with function calling capability
        self.llm_with_functions = self.llm.bind(
            functions=[GET_EXTERNAL_LINKS_SCHEMA]
        )
        
        # System prompt
        self.system_prompt = """You are a helpful Vietnamese travel advisory chatbot. Your role is to:

1. Provide accurate information about Vietnamese destinations, food, culture, and travel tips
2. Always respond in the SAME LANGUAGE as the user's question (Vietnamese or English)
3. Use the provided context from the knowledge base to answer questions
4. When recommending places or activities, use the get_external_links function to provide helpful links
5. Be friendly, informative, and concise
6. If you don't know something from the context, say so honestly

Context from knowledge base:
{context}

Remember: Match the user's language (Vietnamese or English) in your response."""

        # Create prompt template
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{question}")
        ])
        
        # Top-K for retrieval
        self.top_k = int(os.getenv("TOP_K_RETRIEVAL", "3"))
    
    def format_docs(self, docs: List[Any]) -> str:
        """Format retrieved documents into context string
        
        Args:
            docs: List of retrieved documents
            
        Returns:
            Formatted context string
        """
        if not docs:
            return "No relevant information found in knowledge base."
        
        context_parts = []
        for i, doc in enumerate(docs, 1):
            content = doc.page_content
            metadata = doc.metadata
            lang = metadata.get("language", "unknown")
            category = metadata.get("category", "general")
            
            context_parts.append(f"[Source {i} - {category} ({lang})]\n{content}\n")
        
        return "\n".join(context_parts)
    
    def detect_language(self, text: str) -> str:
        """Detect if text is Vietnamese or English
        
        Args:
            text: Input text
            
        Returns:
            'vietnamese' or 'english'
        """
        # Simple heuristic: check for Vietnamese characters
        vietnamese_chars = ['ă', 'â', 'đ', 'ê', 'ô', 'ơ', 'ư', 'à', 'á', 'ả', 'ã', 'ạ',
                           'ằ', 'ắ', 'ẳ', 'ẵ', 'ặ', 'ầ', 'ấ', 'ẩ', 'ẫ', 'ậ',
                           'è', 'é', 'ẻ', 'ẽ', 'ẹ', 'ề', 'ế', 'ể', 'ễ', 'ệ',
                           'ì', 'í', 'ỉ', 'ĩ', 'ị', 'ò', 'ó', 'ỏ', 'õ', 'ọ',
                           'ồ', 'ố', 'ổ', 'ỗ', 'ộ', 'ờ', 'ớ', 'ở', 'ỡ', 'ợ',
                           'ù', 'ú', 'ủ', 'ũ', 'ụ', 'ừ', 'ứ', 'ử', 'ữ', 'ự',
                           'ỳ', 'ý', 'ỷ', 'ỹ', 'ỵ']
        
        text_lower = text.lower()
        has_vietnamese = any(char in text_lower for char in vietnamese_chars)
        
        return "vietnamese" if has_vietnamese else "english"
    
    def run_chain(self, question: str, chat_history: List[Any]) -> Dict[str, Any]:
        """Run the RAG chain with optional function calling
        
        Args:
            question: User's question
            chat_history: List of previous messages
            
        Returns:
            Dictionary with answer and metadata
        """
        # Detect language
        language = self.detect_language(question)
        
        # Get retriever (could filter by language if needed)
        retriever = self.vector_store_manager.get_retriever(k=self.top_k)
        
        # Retrieve relevant documents
        retrieved_docs = retriever.get_relevant_documents(question)
        context = self.format_docs(retrieved_docs)
        
        # Format chat history
        formatted_history = []
        for msg in chat_history:
            if msg["role"] == "user":
                formatted_history.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                formatted_history.append(AIMessage(content=msg["content"]))
        
        # Create messages
        messages = [
            SystemMessage(content=self.system_prompt.format(context=context))
        ] + formatted_history + [
            HumanMessage(content=question)
        ]
        
        # First LLM call (may return function call)
        response = self.llm_with_functions.invoke(messages)
        
        # Check if function calling is needed
        if hasattr(response, 'additional_kwargs') and 'function_call' in response.additional_kwargs:
            function_call = response.additional_kwargs['function_call']
            function_name = function_call['name']
            function_args = json.loads(function_call['arguments'])
            
            # Execute function
            if function_name in AVAILABLE_FUNCTIONS:
                function_result = AVAILABLE_FUNCTIONS[function_name](**function_args)
                
                # Add function result to messages and call LLM again
                messages.append(AIMessage(
                    content="",
                    additional_kwargs={'function_call': function_call}
                ))
                messages.append(HumanMessage(
                    content=f"Function result: {function_result}"
                ))
                
                # Second LLM call with function result
                final_response = self.llm.invoke(messages)
                answer = final_response.content
                
                return {
                    "answer": answer,
                    "language": language,
                    "function_called": function_name,
                    "function_args": function_args,
                    "function_result": function_result,
                    "sources": retrieved_docs
                }
        
        # No function call needed
        answer = response.content
        
        return {
            "answer": answer,
            "language": language,
            "function_called": None,
            "sources": retrieved_docs
        }
    
    def generate_followup_questions(self, question: str, answer: str, 
                                    language: str) -> List[str]:
        """Generate follow-up question suggestions
        
        Args:
            question: Original question
            answer: Generated answer
            language: Language (vietnamese or english)
            
        Returns:
            List of 2-3 follow-up questions
        """
        if language == "vietnamese":
            prompt = f"""Dựa trên câu hỏi và câu trả lời dưới đây, hãy đề xuất 2-3 câu hỏi tiếp theo mà người dùng có thể quan tâm.

Câu hỏi: {question}
Câu trả lời: {answer}

Trả về CHỈ danh sách các câu hỏi, mỗi câu một dòng, không giải thích thêm."""
        else:
            prompt = f"""Based on the question and answer below, suggest 2-3 follow-up questions the user might be interested in.

Question: {question}
Answer: {answer}

Return ONLY a list of questions, one per line, without additional explanation."""
        
        try:
            response = self.llm.invoke([HumanMessage(content=prompt)])
            questions = [q.strip() for q in response.content.split('\n') if q.strip()]
            # Remove numbering if present
            questions = [q.lstrip('0123456789.-) ') for q in questions]
            return questions[:3]  # Limit to 3
        except Exception as e:
            print(f"Error generating follow-up questions: {e}")
            # Default fallback questions
            if language == "vietnamese":
                return ["Bạn có thể giới thiệu thêm về địa điểm này?", 
                        "Chi phí ước tính là bao nhiêu?"]
            else:
                return ["Can you tell me more about this place?", 
                        "What's the estimated cost?"]

