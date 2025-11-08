"""Function Calling Handlers for External Links"""

import json
import os
from typing import List, Dict, Any


def load_mock_links() -> Dict[str, Any]:
    """Load mock links from JSON file
    
    Returns:
        Dictionary of mock links data
    """
    mock_links_path = os.path.join("data", "mock_links.json")
    
    if not os.path.exists(mock_links_path):
        print(f"Warning: Mock links file not found at {mock_links_path}")
        return {}
    
    with open(mock_links_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_external_links(topic: str) -> str:
    """Get external links for a given topic
    
    This function is called by the LLM via Function Calling when it needs
    to provide external resources (maps, reviews, videos) about a topic.
    
    Args:
        topic: The topic to search for (e.g., "bun_cha", "ha_long_bay")
        
    Returns:
        Formatted string with links and descriptions
    """
    mock_links = load_mock_links()
    
    # Normalize topic (lowercase, replace spaces with underscores)
    normalized_topic = topic.lower().strip().replace(" ", "_")
    
    # Try exact match first
    if normalized_topic in mock_links:
        return format_links(mock_links[normalized_topic])
    
    # Try fuzzy matching by checking if normalized_topic is in any key
    for key, value in mock_links.items():
        if normalized_topic in key or key in normalized_topic:
            return format_links(value)
        
        # Check keywords
        keywords = value.get("keywords", [])
        for keyword in keywords:
            if normalized_topic in keyword.lower() or keyword.lower() in normalized_topic:
                return format_links(value)
    
    # No match found
    return f"No external links found for topic: {topic}"


def format_links(link_data: Dict[str, Any]) -> str:
    """Format link data into a readable string
    
    Args:
        link_data: Dictionary with 'type' and 'relevant_links'
        
    Returns:
        Formatted string with links
    """
    link_type = link_data.get("type", "general")
    links = link_data.get("relevant_links", [])
    
    if not links:
        return "No links available"
    
    result = f"External Resources ({link_type}):\n\n"
    
    for i, link in enumerate(links, 1):
        source = link.get("source", "Unknown")
        url = link.get("url", "")
        title = link.get("title", "Link")
        
        result += f"{i}. **{source}**: [{title}]({url})\n"
    
    return result


def search_links_by_keywords(keywords: List[str]) -> str:
    """Search for links matching any of the given keywords
    
    Args:
        keywords: List of keywords to search for
        
    Returns:
        Formatted string with matching links
    """
    mock_links = load_mock_links()
    matched_topics = []
    
    for keyword in keywords:
        normalized_kw = keyword.lower().strip()
        
        for key, value in mock_links.items():
            topic_keywords = value.get("keywords", [])
            
            # Check if keyword matches
            if any(normalized_kw in kw.lower() for kw in topic_keywords):
                if key not in matched_topics:
                    matched_topics.append(key)
    
    if not matched_topics:
        return f"No links found for keywords: {', '.join(keywords)}"
    
    # Format all matched topics
    result = f"Found links for {len(matched_topics)} topic(s):\n\n"
    
    for topic_key in matched_topics:
        topic_data = mock_links[topic_key]
        result += f"### {topic_key.replace('_', ' ').title()}\n"
        result += format_links(topic_data) + "\n"
    
    return result


# Define the function schema for OpenAI Function Calling
GET_EXTERNAL_LINKS_SCHEMA = {
    "name": "get_external_links",
    "description": """Get external links and resources for a Vietnamese travel topic. 
    Use this function when you need to provide users with:
    - Google Maps links to locations
    - Blog articles or reviews
    - YouTube videos
    - TripAdvisor reviews
    - Official websites
    
    Topics can be destinations (ha_long_bay, hoi_an, sapa, etc.), 
    food (pho, bun_cha, banh_mi, etc.), or cultural attractions (water_puppet, ao_dai, etc.).""",
    "parameters": {
        "type": "object",
        "properties": {
            "topic": {
                "type": "string",
                "description": """The topic to get links for. Can be a destination name, food item, or cultural topic.
                Examples: 'ha_long_bay', 'bun_cha', 'water_puppet', 'hanoi', 'pho'"""
            }
        },
        "required": ["topic"]
    }
}


# Alternative schema for searching by keywords
SEARCH_LINKS_BY_KEYWORDS_SCHEMA = {
    "name": "search_links_by_keywords",
    "description": "Search for external links matching multiple keywords",
    "parameters": {
        "type": "object",
        "properties": {
            "keywords": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of keywords to search for"
            }
        },
        "required": ["keywords"]
    }
}


# Function map for execution
AVAILABLE_FUNCTIONS = {
    "get_external_links": get_external_links,
    "search_links_by_keywords": search_links_by_keywords
}

