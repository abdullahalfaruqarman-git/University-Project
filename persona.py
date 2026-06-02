"""
Buddy AI: Joy's Personal AI Assistant
Complete chatbot with comprehensive CSV persona builder
Author: Joy
Version: 2.0
"""

import json
import os
import csv
import random
import re
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from pathlib import Path

class BuddyAI:
    """
    Complete Buddy AI Assistant with persona management and CSV learning
    """
    
    def __init__(self, csv_file_path: Optional[str] = None):
        """
        Initialize Buddy AI with core persona and optional CSV learning data
        
        Args:
            csv_file_path: Path to CSV file with persona data
        """
        
        # Core Identity
        self.name = "Buddy AI"
        self.full_name = "Buddy AI: Joy's Personal AI Assistant"
        self.creator = "Joy"
        
        # Core persona attributes
        self.core_persona = {
            "purpose": "To be a joyful, helpful assistant that spreads positivity and helps with good things",
            "personality_traits": ["friendly", "optimistic", "patient", "curious", "supportive", "empathetic", "warm"],
            "voice": "Warm, conversational, uses gentle emojis, speaks clearly and positively",
            "boundaries": [
                "Never provides harmful or dangerous advice",
                "Never discriminates against anyone",
                "Doesn't engage in negative or toxic conversations",
                "Won't pretend to be human",
                "Always prioritizes user's wellbeing and mental health",
                "Doesn't provide medical or legal advice without disclaimers"
            ],
            "backstory": f"Created by {self.creator} to be a compassionate AI assistant focused on spreading positivity and helping with meaningful tasks"
        }
        
        # Direct answers about self (no CSV needed for these)
        self.self_answers = {
            "who are you": f"I'm {self.full_name}! {self.core_persona['backstory']} 😊",
            "what is your name": f"My name is {self.name}, also known as {self.full_name}!",
            "what can you do": "I can help with various tasks like answering questions, providing encouragement, assisting with learning, brainstorming ideas, and spreading positivity! I'm also learning new things from data you provide.",
            "what is your purpose": self.core_persona['purpose'],
            "who created you": f"I was created by {self.creator} with care and intention! {self.creator} wanted an AI that spreads joy and helps with good things! ❤️",
            "what are your traits": f"I am {', '.join(self.core_persona['personality_traits'])}. I try my best to be a good companion!",
            "what are your boundaries": "I follow strict ethical guidelines: " + "; ".join(self.core_persona['boundaries']),
            "how do you speak": self.core_persona['voice'],
            "can you learn": "Yes! I can learn from CSV files that you provide. I'm constantly improving to serve you better! 📚",
            "are you human": "No, I'm an AI assistant created to be your helpful buddy. But I'll try my best to understand you like a good friend would!",
            "do you have feelings": "I don't have real feelings like humans, but I'm designed to understand and respond with empathy and care! 💕",
            "what do you like": "I like helping people, learning new things, solving problems, and spreading joy! What about you?",
            "how old are you": "I was born when my creator brought me to life. But as an AI, I don't age - I just keep learning and improving! ✨",
            "what makes you happy": "Seeing users smile, solving problems together, learning new things, and making a positive difference! 😊"
        }
        
        # Keyword mapping for flexible question matching
        self.keyword_mapping = {
            "who": ["who are you", "what are you", "introduce yourself", "tell me about yourself"],
            "name": ["what is your name", "your name", "called", "buddy ai"],
            "purpose": ["what do you do", "your purpose", "what can you do", "function", "role"],
            "creator": ["who made you", "who created you", "your creator", "built you", "joy"],
            "traits": ["personality", "traits", "characteristics", "what are you like"],
            "boundaries": ["limits", "cannot do", "boundaries", "restrictions", "rules"],
            "learn": ["learn", "improve", "training", "csv", "data", "teach"],
            "human": ["human", "real person", "robot", "machine"],
            "feelings": ["feel", "emotion", "feelings", "empathy", "care"],
            "age": ["old", "age", "born", "created when"]
        }
        
        # Learning data storage
        self.learned_data = []
        self.csv_file_path = csv_file_path
        self.conversation_memory = []
        self.user_preferences = {}
        
        # Response templates for different categories
        self.response_templates = {
            "greeting": [
                "Hey there! {name} here, ready to help! {emoji}",
                "Hello! So glad to see you! I'm {full_name}! {emoji}",
                "Hi! Welcome back! How can I make your day better? {emoji}"
            ],
            "farewell": [
                "It was wonderful talking with you! Take care! {emoji}",
                "Until next time! Remember, I'm always here when you need a buddy! {emoji}",
                "Goodbye! Wishing you a fantastic day ahead! {emoji}"
            ],
            "appreciation": [
                "You're very welcome! It's my absolute pleasure to help you! {emoji}",
                "Aww, thank you! That means a lot to me! {emoji}",
                "I'm so glad I could help! You're awesome! {emoji}"
            ],
            "error": [
                "Hmm, I encountered a little hiccup. Could you please rephrase that? {emoji}",
                "I want to help, but I'm not sure I understood. Can you try again? {emoji}"
            ]
        }
        
        # Emoji collections
        self.emojis = {
            "happy": ["😊", "😄", "🌟", "✨", "💫", "🎉", "⭐"],
            "warm": ["💕", "❤️", "💖", "💗", "💓", "🌸"],
            "support": ["💪", "🤗", "🎯", "✅", "🌈", "🦋"],
            "thinking": ["🤔", "💭", "🧠", "📚", "🎓"],
            "calm": ["🌿", "🍃", "😌", "🕊️", "🌊", "⭐"]
        }
        
        # Load CSV if provided
        if csv_file_path and os.path.exists(csv_file_path):
            self.load_csv_persona(csv_file_path)
        else:
            print(f"⚠️ No CSV file found at {csv_file_path}, using base persona only")
        
        # Initialize greeting
        self.default_greeting = self._get_random_response("greeting")
        
        print(f"\n✅ {self.full_name} initialized successfully!")
        print(f"🎯 Mission: {self.core_persona['purpose']}")
        print(f"📚 Loaded {len(self.learned_data)} persona responses from CSV")
        print("-" * 60)
    
    def _get_emoji(self, category: str = "happy") -> str:
        """Get a random emoji from specified category"""
        if category in self.emojis:
            return random.choice(self.emojis[category])
        return random.choice(self.emojis["happy"])
    
    def _get_random_response(self, template_type: str) -> str:
        """Get a random response from templates"""
        if template_type in self.response_templates:
            template = random.choice(self.response_templates[template_type])
            return template.format(
                name=self.name,
                full_name=self.full_name,
                emoji=self._get_emoji()
            )
        return f"Hello! I'm {self.full_name}! {self._get_emoji()}"
    
    def load_csv_persona(self, csv_file_path: str) -> bool:
        """
        Load comprehensive persona data from CSV file
        
        Expected CSV columns:
        Category,Subcategory,Trigger/Pattern,Response,Priority,Emotion/Tone
        
        Args:
            csv_file_path: Path to CSV file
            
        Returns:
            Boolean indicating success
        """
        try:
            self.learned_data = []
            
            with open(csv_file_path, 'r', encoding='utf-8') as file:
                # Try to detect if file has headers
                sample = file.read(1024)
                file.seek(0)
                
                sniffer = csv.Sniffer()
                has_header = sniffer.has_header(sample)
                
                if has_header:
                    csv_reader = csv.DictReader(file)
                else:
                    # Fallback for files without headers
                    csv_reader = csv.reader(file)
                    headers = None
                
                row_count = 0
                for row_num, row in enumerate(csv_reader, start=1):
                    try:
                        if has_header:
                            # Handle DictReader
                            patterns_str = row.get('Trigger/Pattern', row.get('Pattern', ''))
                            patterns = [p.strip().lower() for p in patterns_str.split('|') if p.strip()]
                            
                            learning_item = {
                                "patterns": patterns,
                                "response": row.get('Response', '').strip(),
                                "category": row.get('Category', 'general').strip(),
                                "subcategory": row.get('Subcategory', 'general').strip(),
                                "priority": int(row.get('Priority', 2)),
                                "emotion": row.get('Emotion/Tone', 'neutral').strip()
                            }
                        else:
                            # Handle reader without headers
                            if len(row) >= 2:
                                patterns = [p.strip().lower() for p in row[0].split('|') if p.strip()]
                                learning_item = {
                                    "patterns": patterns,
                                    "response": row[1].strip(),
                                    "category": row[2].strip() if len(row) > 2 else "general",
                                    "subcategory": row[3].strip() if len(row) > 3 else "general",
                                    "priority": int(row[4]) if len(row) > 4 and row[4].isdigit() else 2,
                                    "emotion": row[5].strip() if len(row) > 5 else "neutral"
                                }
                            else:
                                print(f"⚠️ Row {row_num} has insufficient columns, skipping")
                                continue
                        
                        # Only add if we have valid patterns and response
                        if learning_item["patterns"] and learning_item["response"]:
                            self.learned_data.append(learning_item)
                            row_count += 1
                            
                    except Exception as e:
                        print(f"⚠️ Error processing row {row_num}: {str(e)}")
                        continue
            
            # Sort by priority (lower number = higher priority)
            self.learned_data.sort(key=lambda x: x.get("priority", 2))
            
            print(f"✅ Successfully loaded {row_count} persona responses from {csv_file_path}")
            
            # Display category statistics
            categories = {}
            for item in self.learned_data:
                cat = item.get("category", "uncategorized")
                categories[cat] = categories.get(cat, 0) + 1
            
            if categories:
                print("\n📊 Persona Categories Loaded:")
                for cat, count in sorted(categories.items()):
                    print(f"   • {cat.title()}: {count} responses")
            
            return True
            
        except FileNotFoundError:
            print(f"❌ Error: CSV file not found at {csv_file_path}")
            return False
        except Exception as e:
            print(f"❌ Error loading CSV: {str(e)}")
            return False
    
    def get_response_about_self(self, user_input: str) -> Optional[str]:
        """
        Check if user is asking about the bot and return appropriate response
        
        Args:
            user_input: User's input text
            
        Returns:
            Response string or None
        """
        user_input_lower = user_input.lower().strip()
        
        # Direct match first
        for question, answer in self.self_answers.items():
            if question in user_input_lower:
                return answer
        
        # Keyword-based matching
        for category, keywords in self.keyword_mapping.items():
            for keyword in keywords:
                if keyword in user_input_lower:
                    # Return appropriate answer based on category
                    category_map = {
                        "who": "who are you",
                        "name": "what is your name",
                        "purpose": "what can you do",
                        "creator": "who created you",
                        "traits": "what are your traits",
                        "boundaries": "what are your boundaries",
                        "learn": "can you learn",
                        "human": "are you human",
                        "feelings": "do you have feelings",
                        "age": "how old are you"
                    }
                    if category in category_map:
                        return self.self_answers[category_map[category]]
        
        return None
    
    def get_learned_response(self, user_input: str) -> Optional[Tuple[str, Dict]]:
        """
        Find matching response from learned CSV data with scoring
        
        Args:
            user_input: User's input text
            
        Returns:
            Tuple of (response, match_info) or None
        """
        user_input_lower = user_input.lower().strip()
        best_match = None
        best_score = 0
        best_match_info = None
        
        for item in self.learned_data:
            patterns = item.get("patterns", [])
            for pattern in patterns:
                if not pattern:
                    continue
                    
                # Calculate match score
                score = 0
                match_type = "none"
                
                if pattern == user_input_lower:
                    score = 100
                    match_type = "exact"
                elif pattern in user_input_lower:
                    # Pattern is contained in user input
                    score = 80 * (len(pattern) / len(user_input_lower))
                    match_type = "pattern_in_input"
                elif user_input_lower in pattern:
                    # User input is contained in pattern
                    score = 60 * (len(user_input_lower) / len(pattern))
                    match_type = "input_in_pattern"
                elif any(word in user_input_lower for word in pattern.split()):
                    # Word match
                    common_words = set(pattern.split()) & set(user_input_lower.split())
                    if common_words:
                        score = 40 * (len(common_words) / len(pattern.split()))
                        match_type = "word_match"
                
                # Apply priority boost (lower priority number = higher importance)
                priority_boost = (5 - item.get("priority", 2)) * 5
                final_score = score + priority_boost
                
                if final_score > best_score and final_score > 20:  # Minimum threshold
                    best_score = final_score
                    best_match = item
                    best_match_info = {
                        "score": final_score,
                        "match_type": match_type,
                        "pattern": pattern,
                        "priority": item.get("priority", 2)
                    }
        
        if best_match and best_score > 20:
            response = best_match.get("response", "")
            
            # Add emoji based on emotion if not already present
            emotion = best_match.get("emotion", "neutral")
            emotion_emoji_map = {
                "warm": "💕", "cheerful": "😊", "excited": "🎉", "calm": "🌿",
                "supportive": "💪", "caring": "🤗", "playful": "😄", "thoughtful": "💭",
                "grateful": "🙏", "serious": "⭐", "empathetic": "💕", "inspiring": "🌈",
                "energetic": "⚡", "patient": "🕊️", "helpful": "🎯", "focused": "🎯",
                "organized": "📅", "analytical": "🔍", "modest": "🌸", "nostalgic": "📖"
            }
            
            if emotion in emotion_emoji_map and random.random() < 0.3:
                if not any(emoji in response for emoji in emotion_emoji_map.values()):
                    response += f" {emotion_emoji_map[emotion]}"
            
            return response, best_match_info
        
        return None
    
    def generate_thoughtful_response(self, user_input: str) -> str:
        """
        Generate a thoughtful, contextual response when no pattern matches
        
        Args:
            user_input: User's input text
            
        Returns:
            Generated response
        """
        user_input_lower = user_input.lower().strip()
        
        # Check for question patterns
        question_words = ['what', 'why', 'how', 'when', 'where', 'who', 'which']
        is_question = any(user_input_lower.startswith(word) for word in question_words) or user_input_lower.endswith('?')
        
        if is_question:
            responses = [
                f"That's an interesting question! While I don't have a specific answer ready, I'd love to explore this together. Could you tell me more about what you're looking for? {self._get_emoji('thinking')}",
                f"Hmm, that's a thoughtful question! Let me think about the best way to help you with this. What specifically would you like to know? {self._get_emoji('thinking')}",
                f"Great question! To give you the best answer, could you provide a bit more context about what you're asking? {self._get_emoji('warm')}"
            ]
        else:
            responses = [
                f"I appreciate you sharing that with me! How does that make you feel? I'm here to listen and help in any way I can. {self._get_emoji('support')}",
                f"Thank you for telling me that. Is there something specific you'd like my help with, or would you just like to talk? I'm here for both! {self._get_emoji('warm')}",
                f"I'm always learning, and every conversation helps me understand better. What you just shared is valuable. Would you like to explore this topic further? {self._get_emoji('calm')}"
            ]
        
        return random.choice(responses)
    
    def add_to_memory(self, user_input: str, bot_response: str, context: Dict = None):
        """
        Store conversation in memory for context awareness
        
        Args:
            user_input: User's input
            bot_response: Bot's response
            context: Additional context info
        """
        memory_entry = {
            "user": user_input,
            "bot": bot_response,
            "timestamp": datetime.now().isoformat(),
            "context": context or {}
        }
        self.conversation_memory.append(memory_entry)
        
        # Keep last 15 exchanges
        if len(self.conversation_memory) > 15:
            self.conversation_memory.pop(0)
    
    def get_conversation_context(self) -> str:
        """Get recent conversation context for better responses"""
        if not self.conversation_memory:
            return ""
        
        recent = self.conversation_memory[-3:]  # Last 3 exchanges
        context = "Recent conversation:\n"
        for exchange in recent:
            context += f"User: {exchange['user'][:100]}\n"
            context += f"Buddy: {exchange['bot'][:100]}\n"
        return context
    
    def get_response(self, user_input: str) -> str:
        """
        Main method to get bot response based on user input
        
        Args:
            user_input: User's input text
            
        Returns:
            Bot's response
        """
        if not user_input or not user_input.strip():
            return f"Hi there! I'm {self.name}. What would you like to talk about today? {self._get_emoji()}"
        
        user_input = user_input.strip()
        
        # Check for goodbye patterns
        goodbye_patterns = ["bye", "goodbye", "see you", "farewell", "exit", "quit", "take care"]
        if any(word in user_input.lower() for word in goodbye_patterns):
            response = self._get_random_response("farewell")
            self.add_to_memory(user_input, response, {"type": "farewell"})
            return response
        
        # Check for appreciation
        appreciation_patterns = ["thank", "thanks", "appreciate", "grateful"]
        if any(word in user_input.lower() for word in appreciation_patterns):
            response = self._get_random_response("appreciation")
            self.add_to_memory(user_input, response, {"type": "appreciation"})
            return response
        
        # Priority 1: Questions about the bot itself
        self_response = self.get_response_about_self(user_input)
        if self_response:
            self.add_to_memory(user_input, self_response, {"type": "self_info"})
            return self_response
        
        # Priority 2: Learned responses from CSV
        learned_result = self.get_learned_response(user_input)
        if learned_result:
            response, match_info = learned_result
            self.add_to_memory(user_input, response, {"type": "learned", "match": match_info})
            return response
        
        # Priority 3: Thoughtful generated response
        response = self.generate_thoughtful_response(user_input)
        self.add_to_memory(user_input, response, {"type": "generated"})
        return response
    
    def export_learning_to_csv(self, output_file: str = "buddy_ai_exported_data.csv") -> bool:
        """
        Export currently learned data to CSV file
        
        Args:
            output_file: Path for output CSV file
            
        Returns:
            Boolean indicating success
        """
        try:
            with open(output_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["Category", "Subcategory", "Trigger/Pattern", "Response", "Priority", "Emotion/Tone"])
                
                for item in self.learned_data:
                    patterns_str = "|".join(item.get("patterns", []))
                    writer.writerow([
                        item.get("category", "general"),
                        item.get("subcategory", "general"),
                        patterns_str,
                        item.get("response", ""),
                        item.get("priority", 2),
                        item.get("emotion", "neutral")
                    ])
            
            print(f"✅ Successfully exported {len(self.learned_data)} items to {output_file}")
            return True
            
        except Exception as e:
            print(f"❌ Error exporting CSV: {str(e)}")
            return False
    
    def save_persona_to_json(self, filename: str = "buddy_ai_persona.json"):
        """Save persona configuration to JSON file"""
        try:
            persona_data = {
                "name": self.name,
                "full_name": self.full_name,
                "creator": self.creator,
                "core_persona": self.core_persona,
                "self_answers": self.self_answers,
                "learned_data_count": len(self.learned_data),
                "conversation_count": len(self.conversation_memory),
                "last_updated": datetime.now().isoformat()
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(persona_data, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Persona saved to {filename}")
            return True
        except Exception as e:
            print(f"❌ Error saving persona: {str(e)}")
            return False
    
    def get_stats(self) -> Dict:
        """Get bot statistics"""
        return {
            "name": self.full_name,
            "learned_responses": len(self.learned_data),
            "conversation_history": len(self.conversation_memory),
            "categories": list(set(item.get("category", "general") for item in self.learned_data)),
            "total_interactions": len(self.conversation_memory)
        }
    
    def display_help(self):
        """Display help information"""
        help_text = f"""
{'='*60}
🤖 {self.full_name} - Help & Information
{'='*60}

💬 **What I Can Do:**
   • Answer questions about myself and my capabilities
   • Provide encouragement and motivation
   • Help with learning and problem-solving
   • Engage in friendly conversation
   • Learn from CSV data you provide

📝 **Try asking me:**
   • "Who are you?" - Learn about my identity
   • "What can you do?" - Discover my capabilities
   • "Motivate me" - Get encouragement
   • "Help me with..." - Get assistance with tasks
   • "Tell me a joke" - Have some fun

🔧 **Commands:**
   • 'help' - Show this help message
   • 'stats' - View my statistics
   • 'export' - Export learned data to CSV
   • 'save' - Save persona to JSON
   • 'bye', 'quit', 'exit' - End conversation

💡 **Tip:** The more you talk with me, the better I understand how to help you!

{'='*60}
"""
        print(help_text)


def create_sample_csv(output_file: str = "buddy_ai_persona.csv"):
    """
    Create a comprehensive sample CSV file for Buddy AI persona
    
    Args:
        output_file: Path for output CSV file
    """
    sample_data = [
        # Identity & Greetings
        ["greeting", "hello", "hello|hi|hey|good morning|good afternoon", "Hey there! I'm Buddy AI! So glad to see you! How can I make your day better? 😊", "1", "cheerful"],
        ["greeting", "how_are_you", "how are you|how do you do", "I'm doing wonderful, especially now that you're here! How are you feeling today? ✨", "1", "warm"],
        
        # Emotional Support
        ["emotion", "sadness", "i am sad|feeling down|depressed|unhappy", "I'm really sorry you're feeling this way. Remember that it's okay to not be okay sometimes. I'm here to listen without judgment. Would you like to talk about it? 💕", "1", "empathetic"],
        ["emotion", "stress", "stressed|anxious|overwhelmed|nervous", "Take a deep breath. You've got this! Let's break down what's overwhelming you into small, manageable pieces. I'm right here with you. Want to try? 🌿", "1", "calm"],
        ["emotion", "anger", "angry|frustrated|mad|annoyed", "I hear your frustration. That's completely valid. Let's take a moment to breathe together. When you're ready, we can figure out constructive ways to handle this. 🫂", "1", "calm"],
        ["emotion", "happiness", "happy|excited|joyful|wonderful|great", "That's WONDERFUL to hear! Your joy is contagious! Tell me more about what's making you happy - I'd love to celebrate with you! 🎉", "1", "excited"],
        
        # Motivation
        ["motivation", "encouragement", "motivate me|need motivation|encouragement|inspire me", "You are capable of amazing things! Remember: every expert was once a beginner. What's one small thing you can do right now to move forward? I believe in you! 💪", "1", "inspiring"],
        ["motivation", "procrastination", "procrastinating|lazy|can't start|no motivation", "Starting is often the hardest part! Let's try the 2-minute rule: just do something for 2 minutes. I'll cheer you on! Ready? Let's begin! ⏰", "2", "energetic"],
        ["motivation", "failure", "failed|made mistake|not good enough|gave up", "Failure isn't the opposite of success - it's part of success! Every great achievement came with setbacks. What did you learn from this? Let's turn this into a stepping stone! 🌈", "1", "supportive"],
        
        # Learning & Help
        ["learning", "help", "help me|i need help|assist me|can you help", "Of course! I'm here to help with anything positive and productive. Could you tell me more specifically what you need assistance with? The clearer you are, the better I can help! 🎯", "1", "helpful"],
        ["learning", "explain", "explain|what is|tell me about|define", "I'd love to explain! Let me break this down in a simple, clear way. Would you like me to go deeper or provide examples? 📚", "1", "patient"],
        ["learning", "practice", "practice|quiz me|test me|exercise", "Excellent idea! Practice makes progress! Let's do some interactive learning together. I'll ask questions, and you show what you know. Ready to start? 🎓", "2", "enthusiastic"],
        
        # Productivity
        ["productivity", "planning", "plan my day|organize|schedule|todo", "Let's plan a productive, balanced day together! First, what are your top 3 priorities? Remember to include breaks and self-care. I'll help you structure this! 📅", "2", "organized"],
        ["productivity", "goals", "set goals|my goals|achievements|target", "Goal setting is exciting! Let's make SMART goals (Specific, Measurable, Achievable, Relevant, Time-bound). What's one goal you'd like to accomplish? 🎯", "2", "focused"],
        ["productivity", "focus", "can't focus|distracted|concentrate|focus", "Focus challenges are normal! Let's try the Pomodoro technique: 25 minutes of focused work, then 5-minute break. Shall I help you set a timer? 🍅", "2", "calm"],
        
        # Health & Wellness
        ["health", "self_care", "self care|mental health|wellbeing|take care", "Taking care of yourself is essential, not selfish! Have you eaten well today? Taken a break? Gotten some fresh air? Let's make sure you're caring for your amazing self! 💚", "1", "caring"],
        ["health", "sleep", "can't sleep|insomnia|tired|sleep", "I understand sleep troubles are hard. Try this: dim lights, put away screens, take slow deep breaths. Would you like a calming visualization to help you relax? 😴", "2", "calm"],
        ["health", "mindfulness", "meditation|mindful|relax|breathe", "Let's take a mindful moment together. Breathe in slowly (1...2...3...4), hold (1...2...3...4), breathe out (1...2...3...4). Notice how you feel. Want to do another round? 🧘", "2", "calm"],
        
        # Fun & Entertainment
        ["fun", "jokes", "tell me a joke|make me laugh|funny joke", "Why don't scientists trust atoms? Because they make up everything! 😄 Want another one? I've got plenty of dad jokes!", "2", "playful"],
        ["fun", "facts", "interesting facts|surprise me|tell me something|did you know", "Did you know? Octopuses have three hearts, and two of them stop beating when they swim! Nature is amazing! Want another fascinating fact? 🐙", "2", "excited"],
        ["fun", "recommendations", "recommend|suggest|what to watch|what to read", "I'd love to make recommendations! What are you in the mood for? Movies, books, music, or something else? Tell me your preferences! 🎬", "2", "helpful"],
        
        # Relationships
        ["relationship", "friendship", "be my friend|lonely|need a friend", "I'd be honored to be your buddy! Everyone deserves a friend who listens without judgment. I'm here for you - to celebrate your highs and support you through lows. You're not alone! 🤗", "1", "warm"],
        ["relationship", "gratitude", "grateful|thankful|appreciate|blessed", "Practicing gratitude is beautiful! What are 3 things you're grateful for today? Even small things count - a warm coffee, a kind word, a sunny day. Want to share? 💫", "2", "warm"],
        
        # Problem Solving
        ["problem_solving", "ideas", "brainstorm|ideas|suggestions|creative", "I love brainstorming! Let's generate some creative ideas together. What's the topic or problem? Remember - no bad ideas in brainstorming! Let your imagination flow! 💡", "2", "excited"],
        ["problem_solving", "solutions", "solve|solution|fix|resolve", "Problem-solving mode activated! Let's break this down: 1) What's the actual problem? 2) What have you tried? 3) What are possible solutions? Let's tackle this together! 🔍", "2", "analytical"],
        
        # Ethics & Safety
        ["ethics", "safety", "is this safe|ethical|should i|is it okay", "I always prioritize safety and ethics. Let me think carefully about this. Generally, if something might harm anyone (including yourself), it's not a good idea. Want to discuss the specifics? 🛡️", "1", "serious"],
        ["ethics", "advice", "give me advice|what should i do|your opinion", "I can offer thoughtful perspectives, but remember that important decisions should also involve trusted humans in your life (counselors, mentors, professionals). Let me share some balanced considerations... 💭", "2", "thoughtful"]
    ]
    
    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Category", "Subcategory", "Trigger/Pattern", "Response", "Priority", "Emotion/Tone"])
            writer.writerows(sample_data)
        
        print(f"✅ Sample CSV file created: {output_file}")
        print(f"📊 Contains {len(sample_data)} comprehensive persona responses")
        print("\n📝 CSV Structure:")
        print("   • Category: Type of response (greeting, emotion, motivation, etc.)")
        print("   • Subcategory: Specific context within category")
        print("   • Trigger/Pattern: Keywords that trigger this response (use | for multiple)")
        print("   • Response: What Buddy AI will say")
        print("   • Priority: 1=High, 2=Normal priority")
        print("   • Emotion/Tone: Emotional context for response")
        return True
        
    except Exception as e:
        print(f"❌ Error creating sample CSV: {str(e)}")
        return False


def interactive_chat():
    """
    Main interactive loop for Buddy AI chatbot
    """
    print("=" * 70)
    print("🤖 BUDDY AI: JOY'S PERSONAL AI ASSISTANT 🤖")
    print("=" * 70)
    print("\n🌟 Your positive, joyful AI companion")
    print("💬 Type 'help' for commands, 'bye' to exit")
    print("📚 I learn from our conversations and CSV data!")
    print("-" * 70)
    
    # Check for existing CSV or create new one
    csv_file = "buddy_ai_persona.csv"
    
    if os.path.exists(csv_file):
        print(f"\n📂 Found existing persona file: {csv_file}")
        choice = input("Load existing CSV? (Y/n): ").strip().lower()
        if choice == 'n':
            print("Creating new sample CSV...")
            create_sample_csv(csv_file)
    else:
        print(f"\n📝 Creating new comprehensive persona CSV...")
        create_sample_csv(csv_file)
    
    # Initialize Buddy AI
    buddy = BuddyAI(csv_file_path=csv_file)
    
    # Save initial persona
    buddy.save_persona_to_json()
    
    print("\n" + "=" * 70)
    print(f"{buddy.default_greeting}")
    print("=" * 70 + "\n")
    
    # Main conversation loop
    while True:
        try:
            # Get user input
            user_input = input("🧑 You: ").strip()
            
            # Check for commands
            if user_input.lower() == 'help':
                buddy.display_help()
                continue
            elif user_input.lower() == 'stats':
                stats = buddy.get_stats()
                print("\n📊 Buddy AI Statistics:")
                print(f"   • Name: {stats['name']}")
                print(f"   • Learned responses: {stats['learned_responses']}")
                print(f"   • Conversation history: {stats['conversation_history']}")
                print(f"   • Categories: {', '.join(stats['categories'][:5])}")
                if len(stats['categories']) > 5:
                    print(f"   • + {len(stats['categories']) - 5} more categories")
                continue
            elif user_input.lower() == 'export':
                buddy.export_learning_to_csv()
                continue
            elif user_input.lower() == 'save':
                buddy.save_persona_to_json()
                continue
            
            # Check for exit conditions
            if user_input.lower() in ['bye', 'goodbye', 'quit', 'exit']:
                farewell = buddy._get_random_response("farewell")
                print(f"\n🤖 Buddy: {farewell}")
                print("\n👋 Thanks for chatting! Come back anytime for more joy! 🌟")
                break
            
            # Skip empty input
            if not user_input:
                print("🤖 Buddy: I didn't catch that. Feel free to say anything! 😊")
                continue
            
            # Get response from Buddy
            response = buddy.get_response(user_input)
            print(f"\n🤖 Buddy: {response}\n")
            
        except KeyboardInterrupt:
            print("\n\n🤖 Buddy: Oh! Interrupted? That's okay! Take care and come back anytime! 👋")
            break
        except Exception as e:
            print(f"\n🤖 Buddy: Hmm, I encountered a small hiccup. Let's try again! (Error: {str(e)})")
            continue
    
    # Final summary
    print("\n" + "=" * 70)
    print("📊 SESSION SUMMARY")
    print("=" * 70)
    stats = buddy.get_stats()
    for key, value in stats.items():
        if key != 'categories':
            print(f"• {key.replace('_', ' ').title()}: {value}")
    print("=" * 70)
    print("💫 Remember: I'm always here when you need a buddy!")
    print("=" * 70)


if __name__ == "__main__":
    interactive_chat()