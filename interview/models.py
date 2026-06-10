from django.db import models
from django.contrib.auth.models import User

class InterviewSession(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    TOPIC_CHOICES = [
        ('behavioral', 'Behavioral'),
        ('python', 'Python / Django Development'),
        ('system_design', 'System Design'),
        ('data_structures', 'Data Structures & Algorithms'),
        ('c_prog', 'C Programming'),
        ('cpp_prog', 'C++ Programming'),
        ('java_prog', 'Java Programming'),
        ('web_dev', 'Web Development (Full Stack Basics)'),
        ('react_dev', 'React Development'),
        ('dbms', 'Database Systems'),
        ('sql_db', 'PostgreSQL / MySQL'),
        ('os', 'Operating Systems'),
        ('networks', 'Computer Networks'),
        ('cybersecurity', 'Cyber Security Basics'),
        ('cloud_devops', 'Cloud & DevOps Basics'),
        ('sys_prog', 'System Programming Concepts'),
    ]

    ASSESSMENT_MODES = [
        ('mixed', 'Mixed Mode'),
        ('mcq', 'MCQ Practice'),
        ('written', 'Written Interview'),
        ('coding', 'Coding Simulation'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='sessions')
    topic = models.CharField(max_length=50, choices=TOPIC_CHOICES)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    mode = models.CharField(max_length=20, choices=ASSESSMENT_MODES, default='mixed')
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    score = models.FloatField(null=True, blank=True)  # Store the final average score (out of 10)
    current_question_index = models.IntegerField(default=1)  # Tracks active question order index (1-based)
    resume_text = models.TextField(null=True, blank=True)  # Optional context resume input
    
    def __str__(self):
        topic_name = dict(self.TOPIC_CHOICES).get(self.topic, self.topic)
        difficulty_name = dict(self.DIFFICULTY_CHOICES).get(self.difficulty, self.difficulty)
        mode_name = dict(self.ASSESSMENT_MODES).get(self.mode, self.mode)
        user_str = self.user.username if self.user else "Anonymous"
        return f"{user_str} - {topic_name} ({difficulty_name}) [{mode_name}] - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

class InterviewQuestion(models.Model):
    QUESTION_TYPES = [
        ('mcq', 'Multiple Choice'),
        ('written', 'Written Response'),
        ('coding', 'Coding Challenge'),
    ]

    session = models.ForeignKey(InterviewSession, related_name='questions', on_delete=models.CASCADE)
    question_text = models.TextField()
    question_type = models.CharField(max_length=15, choices=QUESTION_TYPES, default='written')
    order = models.IntegerField()  # 1-based order within the session
    option_a = models.TextField(blank=True, null=True)
    option_b = models.TextField(blank=True, null=True)
    option_c = models.TextField(blank=True, null=True)
    option_d = models.TextField(blank=True, null=True)
    correct_answer = models.CharField(max_length=10, blank=True, null=True)  # For MCQ: 'A', 'B', 'C', or 'D'
    user_answer = models.TextField(blank=True, null=True)
    score = models.IntegerField(null=True, blank=True)  # Grade out of 10 (or 10/0 for MCQ)
    strengths = models.TextField(blank=True, null=True)      # Also stores 'Correct Approach' for coding
    weaknesses = models.TextField(blank=True, null=True)     # Also stores 'Mistakes' for coding
    improved_answer = models.TextField(blank=True, null=True) # Also stores 'Optimized Solution' for coding / MCQ explanation
    tips = models.TextField(blank=True, null=True)
    evaluated = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['order']
        
    def __str__(self):
        return f"Q{self.order} for Session {self.session.id}"

class ChatSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_sessions', null=True, blank=True)
    resume_text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        user_str = self.user.username if self.user else "Anonymous"
        return f"Chat Session {self.id} for {user_str} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

class ChatMessage(models.Model):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=10, choices=[('user', 'User'), ('ai', 'AI')])
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Message {self.id} in Chat {self.session.id} by {self.sender}"
