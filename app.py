from flask import Flask, render_template, request, jsonify
import os
import random
from datetime import datetime

app = Flask(__name__, static_folder='static', template_folder='templates')

# Comprehensive interview database - COMPLETELY OFFLINE
INTERVIEW_DATA = {
    "software engineer": {
        "name": "Software Engineering Interview",
        "questions": [
            "Tell me about a challenging technical problem you solved and how you approached it.",
            "How do you ensure code quality in your projects?",
            "Describe your experience with system design. Walk me through designing a URL shortening service.",
            "How do you handle technical debt when working on tight deadlines?",
            "What's your process for debugging a complex issue in production?",
            "How do you stay updated with new technologies and frameworks?",
            "Describe a time you had to collaborate with a difficult team member.",
            "What programming languages are you most comfortable with and why?",
            "How do you approach code reviews?",
            "Tell me about a project failure and what you learned from it."
        ],
        "follow_ups": [
            "Can you tell me more about that?",
            "What was the most challenging part?",
            "How did you measure success?",
            "What would you do differently next time?",
            "How did that experience help you grow?",
            "What technical details were involved?",
            "How did you collaborate with others?",
            "What was the business impact?"
        ]
    },
    "product manager": {
        "name": "Product Management Interview",
        "questions": [
            "How do you prioritize features in a product roadmap?",
            "Describe a time you used data to make a product decision.",
            "How do you gather and incorporate user feedback?",
            "What's your approach to working with engineering teams?",
            "How do you measure product success?",
            "Tell me about a product you admire and why.",
            "How do you handle conflicting priorities from stakeholders?",
            "Describe your product discovery process.",
            "What metrics would you track for a social media app?",
            "How do you decide when to build vs. buy a solution?"
        ],
        "follow_ups": [
            "How did you validate that approach?",
            "What data influenced your decision?",
            "How did you align stakeholders?",
            "What was the user impact?",
            "How did you measure ROI?",
            "What were the trade-offs?",
            "How did you handle pushback?",
            "What would you improve next time?"
        ]
    },
    "data scientist": {
        "name": "Data Science Interview",
        "questions": [
            "How do you validate a machine learning model?",
            "Describe your experience with A/B testing and statistical analysis.",
            "How do you handle missing or noisy data?",
            "What's your approach to feature selection?",
            "How do you explain complex models to non-technical stakeholders?",
            "Describe a time you used data to influence business decisions.",
            "What's the difference between supervised and unsupervised learning?",
            "How do you prevent overfitting in your models?",
            "What data visualization tools do you prefer and why?",
            "Tell me about a challenging data analysis project."
        ],
        "follow_ups": [
            "What statistical methods did you use?",
            "How did you ensure data quality?",
            "What was the business outcome?",
            "How did you validate your results?",
            "What challenges did you face?",
            "How did you communicate findings?",
            "What would you do differently?",
            "How did you measure model performance?"
        ]
    },
    "sales associate": {
        "name": "Sales Associate Interview",
        "questions": [
            "How do you approach cold calling or prospecting?",
            "Describe a time you overcame a major objection from a customer.",
            "How do you build long-term customer relationships?",
            "What's your process for understanding customer needs?",
            "How do you handle rejection in sales?",
            "Describe your most successful sale and what made it work.",
            "How do you use CRM tools in your sales process?",
            "What strategies do you use for upselling or cross-selling?",
            "How do you stay motivated during slow periods?",
            "What makes a great salesperson in your opinion?"
        ],
        "follow_ups": [
            "How did you build rapport?",
            "What was the key to success?",
            "How did you handle objections?",
            "What was the customer's main need?",
            "How did you follow up?",
            "What metrics did you track?",
            "How did you personalize your approach?",
            "What was the long-term outcome?"
        ]
    },
    "retail associate": {
        "name": "Retail Associate Interview",
        "questions": [
            "How would you handle an angry customer complaining about a product?",
            "What does excellent customer service mean to you?",
            "How do you stay knowledgeable about store products?",
            "Describe your approach to maintaining store appearance and organization.",
            "How would you handle a situation where a product is out of stock?",
            "What would you do if you saw a coworker behaving unprofessionally?",
            "How do you prioritize tasks during busy hours?",
            "What experience do you have with point-of-sale systems?",
            "How would you promote a new product to customers?",
            "Why do you want to work in retail?"
        ],
        "follow_ups": [
            "How would you de-escalate that situation?",
            "What steps would you take?",
            "How do you ensure customer satisfaction?",
            "What's your approach to teamwork?",
            "How do you handle multiple priorities?",
            "What makes good customer service?",
            "How do you handle stress?",
            "What would you do to go above and beyond?"
        ]
    }
}

# Interview session management
interview_sessions = {}

def generate_offline_response(user_message, role, session, mode):
    """Generate intelligent responses without any API calls"""
    
    if mode == "feedback":
        return generate_offline_feedback(role, session)
    
    role_data = INTERVIEW_DATA[role]
    
    # Handle start of interview
    if "start" in user_message.lower() or session["question_index"] == 0:
        session["question_index"] = 1
        first_question = role_data["questions"][0]
        return f"Great! Let's begin the {role_data['name']}. {first_question}"
    
    # Handle explicit request for next question
    if "next" in user_message.lower() or "another question" in user_message.lower():
        if session["question_index"] < len(role_data["questions"]):
            next_q = role_data["questions"][session["question_index"]]
            session["question_index"] += 1
            return next_q
        else:
            return "We've covered all the main questions. Would you like feedback on your performance?"
    
    # Handle interview completion request
    if any(word in user_message.lower() for word in ["done", "finish", "end", "feedback", "conclude"]):
        return "That concludes our interview. Click 'Get Feedback' for detailed feedback on your performance!"
    
    # Generate follow-up question (70% chance) or move to next question (30% chance)
    if random.random() < 0.7:  # Follow-up question
        follow_up = random.choice(role_data["follow_ups"])
        return follow_up
    else:  # Move to next main question
        if session["question_index"] < len(role_data["questions"]):
            next_q = role_data["questions"][session["question_index"]]
            session["question_index"] += 1
            return f"Interesting. Now, {next_q}"
        else:
            return "We've covered all questions. Ready for feedback?"

def generate_offline_feedback(role, session):
    """Generate comprehensive feedback without any API"""
    
    role_data = INTERVIEW_DATA[role]
    
    feedback_templates = {
        "software engineer": """
**Technical Interview Feedback**

**Strengths:**
• Good technical foundation and problem-solving approach
• Clear communication of technical concepts
• Demonstrated practical experience with real projects

**Areas for Improvement:**
• Provide more specific code examples and technical details
• Use more data to quantify your impact (e.g., "improved performance by 40%")
• Practice explaining complex systems more simply

**Technical Skills Assessment:**
- Problem Solving: 8/10
- Technical Depth: 7/10  
- Communication: 8/10
- Practical Experience: 7/10

**Recommendation:**
Strong candidate with good fundamentals. Focus on quantifying achievements and providing more detailed technical examples.
""",
        "product manager": """
**Product Management Interview Feedback**

**Strengths:**
• Strategic thinking about product roadmaps
• Customer-focused approach to decision making
• Good understanding of stakeholder management

**Areas for Improvement:**
• Include more specific metrics in your examples
• Practice articulating trade-offs more clearly
• Provide more detailed examples of data-driven decisions

**Skill Assessment:**
- Strategic Thinking: 8/10
- Data Analysis: 7/10
- Stakeholder Management: 8/10
- Product Vision: 7/10

**Recommendation:**
Solid product thinking. Work on adding quantitative results to your stories.
""",
        "data scientist": """
**Data Science Interview Feedback**

**Strengths:**
• Good understanding of statistical concepts
• Clear explanation of technical methodologies
• Practical approach to problem-solving

**Areas for Improvement:**
• Provide more specific examples of model performance
• Practice explaining technical concepts to non-technical audiences
• Include more business context in your examples

**Skill Assessment:**
- Technical Knowledge: 8/10
- Statistical Understanding: 8/10
- Business Impact: 7/10
- Communication: 7/10

**Recommendation:**
Strong technical skills. Focus on connecting your work to business outcomes.
""",
        "sales associate": """
**Sales Interview Feedback**

**Strengths:**
• Customer-focused approach
• Good understanding of relationship building
• Positive and persistent attitude

**Areas for Improvement:**
• Add specific numbers to your success stories
• Practice handling objections more systematically
• Include more examples of long-term relationship building

**Skill Assessment:**
- Customer Rapport: 8/10
- Persistence: 8/10
- Product Knowledge: 7/10
- Closing Skills: 7/10

**Recommendation:**
Natural sales personality. Quantify your achievements with specific numbers.
""",
        "retail associate": """
**Retail Interview Feedback**

**Strengths:**
• Strong customer service orientation
• Good problem-solving approach
• Team-oriented mindset

**Areas for Improvement:**
• Provide more specific examples of handling difficult situations
• Practice explaining your contribution to team success
• Include examples of going above and beyond

**Skill Assessment:**
- Customer Service: 9/10
- Problem Solving: 8/10
- Teamwork: 8/10
- Product Knowledge: 7/10

**Recommendation:**
Excellent customer service mindset. Add more specific examples from your experience.
"""
    }
    
    return feedback_templates.get(role, feedback_templates["software engineer"])

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/interview", methods=["POST"])
def interview():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"reply": "Please provide valid data", "source": "offline"}), 400
            
        user_message = data.get("message", "").strip()
        role = data.get("role", "software engineer")
        mode = data.get("mode", "mock")
        session_id = data.get("session_id")
        
        print(f"Processing: '{user_message}' for {role} in {mode} mode")  # Debug log
        
        # Validate role
        if role not in INTERVIEW_DATA:
            return jsonify({"reply": "Please select a valid role", "source": "offline"}), 400
        
        # Get or create session
        if not session_id or session_id not in interview_sessions:
            session_id = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            interview_sessions[session_id] = {
                "role": role,
                "question_index": 0,
                "start_time": datetime.now().isoformat()
            }
        
        session = interview_sessions[session_id]
        
        # Generate response
        reply = generate_offline_response(user_message, role, session, mode)
        
        return jsonify({
            "reply": reply,
            "session_id": session_id,
            "source": "offline"
        })
        
    except Exception as e:
        print(f"Error: {str(e)}")  # Debug log
        return jsonify({
            "reply": "I encountered an error. Please try again or restart the interview.",
            "source": "error"
        }), 500

@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy", "mode": "offline"})

if __name__ == "__main__":
    print("🚀 Starting Interview Practice Partner (OFFLINE MODE)")
    print("📊 Available roles:", list(INTERVIEW_DATA.keys()))
    print("🌐 Server running at http://localhost:5000")
    app.run(debug=True, port=5000)