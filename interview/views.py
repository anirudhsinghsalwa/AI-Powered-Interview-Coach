import io
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.http import HttpResponse, Http404
from django.db.models import Avg, Count

# ReportLab imports for PDF generation
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

from .models import InterviewSession, InterviewQuestion, ChatSession, ChatMessage
from .services import generate_session_questions, evaluate_candidate_answer, generate_chat_reply

# -------------------------------------------------------------------------
# AUTHENTICATION VIEWS
# -------------------------------------------------------------------------

from django import forms
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email Address")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

def user_signup(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome to Interview Coach Pro, {user.username}!")
            return redirect('dashboard')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        form = CustomUserCreationForm()
    return render(request, 'interview/signup.html', {'form': form})


def user_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'interview/login.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')

# -------------------------------------------------------------------------
# DASHBOARD VIEW
# -------------------------------------------------------------------------

@login_required
def dashboard(request):
    # Retrieve user's sessions
    sessions = InterviewSession.objects.filter(user=request.user).order_by('-created_at')
    completed_sessions = sessions.filter(completed=True)
    
    # Calculate stats
    total_attempts = completed_sessions.count()
    
    avg_score_raw = completed_sessions.aggregate(Avg('score'))['score__avg']
    avg_score = round(avg_score_raw * 10, 1) if avg_score_raw is not None else 0.0 # scale to percentage index or out of 10
    
    # Track progression by counting sessions grouped by topic
    topic_stats = completed_sessions.values('topic').annotate(count=Count('id'))
    topic_counts = {t[0]: 0 for t in InterviewSession.TOPIC_CHOICES}
    for item in topic_stats:
        topic_counts[item['topic']] = item['count']
    
    # Prep history list
    history = []
    for s in sessions:
        topic_name = dict(s.TOPIC_CHOICES).get(s.topic, s.topic)
        difficulty_name = dict(s.DIFFICULTY_CHOICES).get(s.difficulty, s.difficulty)
        history.append({
            'id': s.id,
            'topic': topic_name,
            'difficulty': difficulty_name,
            'created_at': s.created_at,
            'completed': s.completed,
            'score': round(s.score, 1) if s.score is not None else None,
        })

    # Calculate aggregated counts
    prog_count = sum(topic_counts.get(t, 0) for t in ['python', 'c_prog', 'cpp_prog', 'java_prog', 'web_dev', 'react_dev'])
    sys_count = sum(topic_counts.get(t, 0) for t in ['system_design', 'os', 'networks', 'cybersecurity', 'cloud_devops', 'sys_prog', 'dbms', 'sql_db'])
    core_count = topic_counts.get('data_structures', 0) + topic_counts.get('behavioral', 0)

    context = {
        'total_attempts': total_attempts,
        'avg_score': avg_score, # out of 10.0 scale, e.g., 7.8/10
        'history': history,
        'prog_count': prog_count,
        'sys_count': sys_count,
        'core_count': core_count,
    }
    return render(request, 'interview/dashboard.html', context)

# -------------------------------------------------------------------------
# INTERVIEW SESSION FLOW VIEWS
# -------------------------------------------------------------------------

@login_required
def session_start(request):
    if request.method == 'POST':
        topic = request.POST.get('topic')
        difficulty = request.POST.get('difficulty')
        mode = request.POST.get('mode', 'mixed')
        
        # Validate selections
        valid_topics = [t[0] for t in InterviewSession.TOPIC_CHOICES]
        valid_diffs = [d[0] for d in InterviewSession.DIFFICULTY_CHOICES]
        valid_modes = [m[0] for m in InterviewSession.ASSESSMENT_MODES]
        
        if topic not in valid_topics or difficulty not in valid_diffs or mode not in valid_modes:
            messages.error(request, "Invalid topic, difficulty, or mode selection.")
            return redirect('session_start')
            
        resume_text = request.POST.get('resume_text', '').strip() or None
        
        # Create a new session
        session = InterviewSession.objects.create(
            user=request.user,
            topic=topic,
            difficulty=difficulty,
            mode=mode,
            resume_text=resume_text,
            completed=False
        )
        
        # Generate 5 questions via service (Gemini API / Fallback)
        questions_list = generate_session_questions(topic, difficulty, mode, resume_text=resume_text)
        
        # Save questions in database
        for index, q_data in enumerate(questions_list, start=1):
            InterviewQuestion.objects.create(
                session=session,
                question_text=q_data['question'],
                question_type=q_data['type'],
                order=index,
                option_a=q_data.get('option_a', ''),
                option_b=q_data.get('option_b', ''),
                option_c=q_data.get('option_c', ''),
                option_d=q_data.get('option_d', ''),
                correct_answer=q_data.get('correct_answer', ''),
                improved_answer=q_data.get('expected_answer', ''),
                evaluated=False
            )
            
        return redirect('question_view', session_id=session.id, question_order=1)
        
    # GET request
    topics = InterviewSession.TOPIC_CHOICES
    difficulties = InterviewSession.DIFFICULTY_CHOICES
    modes = InterviewSession.ASSESSMENT_MODES
    selected_mode = request.GET.get('mode', 'mixed')
    return render(request, 'interview/session_start.html', {
        'topics': topics,
        'difficulties': difficulties,
        'modes': modes,
        'selected_mode': selected_mode
    })


@login_required
def question_view(request, session_id, question_order):
    session = get_object_or_404(InterviewSession, id=session_id, user=request.user)
    question = get_object_or_404(InterviewQuestion, session=session, order=question_order)
    
    # If already evaluated, redirect straight to feedback page
    if question.evaluated:
        return redirect('question_feedback', session_id=session.id, question_order=question_order)
        
    # Update active tracking index
    session.current_question_index = question_order
    session.save()
    
    total_questions = session.questions.count()
    progress_percent = int((question_order - 1) / total_questions * 100)
    
    context = {
        'session': session,
        'question': question,
        'question_order': question_order,
        'total_questions': total_questions,
        'progress_percent': progress_percent,
        'topic_name': dict(session.TOPIC_CHOICES).get(session.topic, session.topic),
        'difficulty_name': dict(session.DIFFICULTY_CHOICES).get(session.difficulty, session.difficulty),
        'mode_name': dict(session.ASSESSMENT_MODES).get(session.mode, session.mode),
    }
    return render(request, 'interview/question.html', context)


@login_required
def question_submit(request, session_id, question_order):
    if request.method != 'POST':
        return redirect('question_view', session_id=session_id, question_order=question_order)
        
    session = get_object_or_404(InterviewSession, id=session_id, user=request.user)
    question = get_object_or_404(InterviewQuestion, session=session, order=question_order)
    
    user_answer = request.POST.get('user_answer', '').strip()
    
    if question.question_type == 'mcq':
        # Grade MCQ instantly on server side
        correct = (user_answer.upper() == question.correct_answer.upper())
        question.user_answer = user_answer
        question.score = 10 if correct else 0
        question.strengths = "Correct response!" if correct else ""
        question.weaknesses = "" if correct else f"Incorrect. You selected option {user_answer}, but the correct option was {question.correct_answer}."
        # expected_answer is already stored in improved_answer during creation
        question.tips = "Review the explanation below to reinforce your understanding."
        question.evaluated = True
        question.save()
    else:
        # Run evaluation via Service Layer (Gemini / Fallback) for Written and Coding types
        evaluation = evaluate_candidate_answer(question.question_text, user_answer, question.question_type)
        
        # Save evaluation back to question
        question.user_answer = user_answer
        question.score = evaluation['score']
        question.strengths = evaluation['strengths']
        question.weaknesses = evaluation['weaknesses']
        question.improved_answer = evaluation['improved_answer']
        question.tips = evaluation['tips']
        question.evaluated = True
        question.save()
    
    return redirect('question_feedback', session_id=session.id, question_order=question_order)


@login_required
def question_feedback(request, session_id, question_order):
    session = get_object_or_404(InterviewSession, id=session_id, user=request.user)
    question = get_object_or_404(InterviewQuestion, session=session, order=question_order)
    
    if not question.evaluated:
        return redirect('question_view', session_id=session.id, question_order=question_order)
        
    total_questions = session.questions.count()
    is_last = (question_order >= total_questions)
    next_order = question_order + 1
    
    # Determine visual badge color
    score = question.score or 0
    if score >= 8:
        score_color = 'green'
    elif score >= 5:
        score_color = 'yellow'
    else:
        score_color = 'red'
        
    context = {
        'session': session,
        'question': question,
        'question_order': question_order,
        'total_questions': total_questions,
        'is_last': is_last,
        'next_order': next_order,
        'score_color': score_color,
        'topic_name': dict(session.TOPIC_CHOICES).get(session.topic, session.topic),
    }
    return render(request, 'interview/feedback.html', context)


@login_required
def results_view(request, session_id):
    session = get_object_or_404(InterviewSession, id=session_id, user=request.user)
    questions = session.questions.all()
    
    # Mark session as completed and compute final average score
    scores = [q.score for q in questions if q.score is not None]
    if scores:
        session.score = sum(scores) / len(scores)
    else:
        session.score = 0.0
        
    session.completed = True
    session.save()
    
    # Score color
    avg_score = session.score
    if avg_score >= 8.0:
        result_color = 'green'
    elif avg_score >= 5.0:
        result_color = 'yellow'
    else:
        result_color = 'red'
        
    context = {
        'session': session,
        'questions': questions,
        'result_color': result_color,
        'topic_name': dict(session.TOPIC_CHOICES).get(session.topic, session.topic),
        'difficulty_name': dict(session.DIFFICULTY_CHOICES).get(session.difficulty, session.difficulty),
        'mode_name': dict(session.ASSESSMENT_MODES).get(session.mode, session.mode),
    }
    return render(request, 'interview/results.html', context)

# -------------------------------------------------------------------------
# PDF GENERATION VIEW
# -------------------------------------------------------------------------

@login_required
def download_pdf(request, session_id):
    session = get_object_or_404(InterviewSession, id=session_id, user=request.user)
    if not session.completed:
        raise Http404("Session is not completed yet.")
        
    questions = session.questions.all()
    
    # Create file-like buffer to receive PDF data
    buffer = io.BytesIO()
    
    # Create the PDF object, using letter size
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=54,
        leftMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    story = []
    
    # Custom styles
    styles = getSampleStyleSheet()
    
    # Define color scheme (Linear/Vercel style - slate/dark colors with violet accent)
    primary_color = colors.HexColor("#6D28D9") # Violet-700
    dark_neutral = colors.HexColor("#1F2937")  # Slate-800
    light_neutral = colors.HexColor("#F3F4F6") # Slate-100
    border_color = colors.HexColor("#E5E7EB")  # Slate-200
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        textColor=primary_color,
        spaceAfter=15
    )
    
    h2_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=16,
        textColor=dark_neutral,
        spaceBefore=15,
        spaceAfter=8
    )
    
    h3_style = ParagraphStyle(
        'SubSectionHeading',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=12,
        textColor=primary_color,
        spaceBefore=10,
        spaceAfter=5
    )
    
    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=10,
        textColor=dark_neutral,
        leading=14,
        spaceAfter=8
    )
    
    label_style = ParagraphStyle(
        'LabelText',
        parent=body_style,
        fontName='Helvetica-Bold',
    )
    
    # Document Header
    story.append(Paragraph("Interview Practice Report Card", title_style))
    story.append(Paragraph("System Evaluation Report & Performance Feedback", body_style))
    story.append(Spacer(1, 15))
    
    # Info metadata box
    topic_name = dict(session.TOPIC_CHOICES).get(session.topic, session.topic)
    difficulty_name = dict(session.DIFFICULTY_CHOICES).get(session.difficulty, session.difficulty)
    mode_name = dict(session.ASSESSMENT_MODES).get(session.mode, session.mode)
    date_str = session.created_at.strftime('%Y-%m-%d %H:%M')
    
    info_data = [
        [Paragraph("Candidate:", label_style), Paragraph(request.user.username, body_style),
         Paragraph("Topic / Mode:", label_style), Paragraph(f"{topic_name} ({mode_name})", body_style)],
        [Paragraph("Difficulty:", label_style), Paragraph(difficulty_name, body_style),
         Paragraph("Date:", label_style), Paragraph(date_str, body_style)],
        [Paragraph("Overall Score:", label_style), Paragraph(f"{round(session.score, 1)} / 10.0", label_style),
         Paragraph("Status:", label_style), Paragraph("Completed", body_style)]
    ]
    
    info_table = Table(info_data, colWidths=[90, 160, 90, 164])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), light_neutral),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('BOX', (0,0), (-1,-1), 0.5, border_color),
        ('INNERGRID', (0,0), (-1,-1), 0.25, border_color),
    ]))
    
    story.append(info_table)
    story.append(Spacer(1, 20))
    
    # Question summary table
    story.append(Paragraph("Performance Summary", h2_style))
    summary_data = [[
        Paragraph("No.", label_style),
        Paragraph("Type", label_style),
        Paragraph("Question Text", label_style),
        Paragraph("Score", label_style)
    ]]
    
    for q in questions:
        # Shorten question text for table
        q_snippet = q.question_text
        if len(q_snippet) > 75:
            q_snippet = q_snippet[:72] + "..."
            
        summary_data.append([
            Paragraph(f"Q{q.order}", body_style),
            Paragraph(q.get_question_type_display(), body_style),
            Paragraph(q_snippet, body_style),
            Paragraph(f"{q.score}/10", label_style)
        ])
        
    summary_table = Table(summary_data, colWidths=[35, 80, 325, 64])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#EDE9FE")), # light violet
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('LINEBELOW', (0,0), (-1,-1), 0.5, border_color),
        ('BOX', (0,0), (-1,-1), 0.5, border_color),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 20))
    story.append(PageBreak()) # Shift details to next page
    
    # Detailed breakdown section
    story.append(Paragraph("Detailed Breakdown", h2_style))
    
    for q in questions:
        q_type_str = q.get_question_type_display()
        story.append(Paragraph(f"Question {q.order} [{q_type_str}] (Score: {q.score}/10)", h3_style))
        story.append(Paragraph(q.question_text, label_style))
        story.append(Spacer(1, 4))
        
        if q.question_type == 'mcq':
            # Render MCQ options and selections
            story.append(Paragraph("Options:", label_style))
            story.append(Paragraph(f"A) {q.option_a}", body_style))
            story.append(Paragraph(f"B) {q.option_b}", body_style))
            story.append(Paragraph(f"C) {q.option_c}", body_style))
            story.append(Paragraph(f"D) {q.option_d}", body_style))
            story.append(Spacer(1, 4))
            
            story.append(Paragraph(f"Your Selected Answer: {q.user_answer or '*No answer submitted*'}", label_style))
            story.append(Paragraph(f"Correct Answer: {q.correct_answer}", label_style))
            story.append(Spacer(1, 6))
            
            story.append(Paragraph("Explanation:", label_style))
            story.append(Paragraph(q.improved_answer or "N/A", body_style))
            
        elif q.question_type == 'coding':
            # Render Coding evaluation
            story.append(Paragraph("Your Submitted Code:", label_style))
            story.append(Paragraph(q.user_answer or "*No answer submitted*", body_style))
            story.append(Spacer(1, 6))
            
            story.append(Paragraph("Correct Approach:", label_style))
            story.append(Paragraph(q.strengths or "N/A", body_style))
            story.append(Spacer(1, 6))
            
            story.append(Paragraph("Identified Mistakes:", label_style))
            story.append(Paragraph(q.weaknesses or "N/A", body_style))
            story.append(Spacer(1, 6))
            
            story.append(Paragraph("Optimized Solution:", label_style))
            story.append(Paragraph(q.improved_answer or "N/A", body_style))
            story.append(Spacer(1, 6))
            
            story.append(Paragraph("Complexity & Tips:", label_style))
            story.append(Paragraph(q.tips or "N/A", body_style))
            
        else:
            # Render Written evaluation
            story.append(Paragraph("Your Answer:", label_style))
            story.append(Paragraph(q.user_answer or "*No answer submitted*", body_style))
            story.append(Spacer(1, 6))
            
            story.append(Paragraph("Strengths:", label_style))
            story.append(Paragraph(q.strengths or "N/A", body_style))
            story.append(Spacer(1, 6))
            
            story.append(Paragraph("Areas for Improvement:", label_style))
            story.append(Paragraph(q.weaknesses or "N/A", body_style))
            story.append(Spacer(1, 6))
            
            story.append(Paragraph("Model Answer Guide:", label_style))
            story.append(Paragraph(q.improved_answer or "N/A", body_style))
            story.append(Spacer(1, 6))
            
            story.append(Paragraph("Actionable Tips:", label_style))
            story.append(Paragraph(q.tips or "N/A", body_style))
        
        story.append(Spacer(1, 10))
        story.append(Paragraph("<hr color='#E5E7EB'/>", body_style)) # divider
        story.append(Spacer(1, 10))
        
    # Build the document
    doc.build(story)
    
    # Retrieve the PDF content from buffer
    pdf_content = buffer.getvalue()
    buffer.close()
    
    # Return as response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Interview_Report_Session_{session.id}.pdf"'
    response.write(pdf_content)
    return response


# -------------------------------------------------------------------------
# AI CHAT COACH VIEWS
# -------------------------------------------------------------------------

@login_required
def chat_start(request):
    if request.method == 'POST':
        resume_text = request.POST.get('resume_text', '').strip() or None
        # Create a new chat session
        chat_session = ChatSession.objects.create(
            user=request.user,
            resume_text=resume_text
        )
        # Add initial greeting message
        welcome_text = "Hello! I am your AI Interview Coach. "
        if resume_text:
            welcome_text += "I've reviewed your resume and I'm ready to grill you on your skills, experience, and projects. Let's get started! What position are you interviewing for?"
        else:
            welcome_text += "I can help you practice coding, system design, DSA, and behavioral interviews. To start, could you tell me what role you're preparing for, or share your resume context?"
            
        ChatMessage.objects.create(
            session=chat_session,
            sender='ai',
            text=welcome_text
        )
        return redirect('chat_room', chat_id=chat_session.id)
        
    return render(request, 'interview/chat_start.html')


@login_required
def chat_room(request, chat_id):
    chat_session = get_object_or_404(ChatSession, id=chat_id, user=request.user)
    messages = chat_session.messages.order_by('created_at')
    
    context = {
        'chat_session': chat_session,
        'chat_messages': messages,
    }
    return render(request, 'interview/chat_room.html', context)


@login_required
def chat_send(request, chat_id):
    if request.method != 'POST':
        return redirect('chat_room', chat_id=chat_id)
        
    chat_session = get_object_or_404(ChatSession, id=chat_id, user=request.user)
    user_text = request.POST.get('message', '').strip()
    
    if user_text:
        # Save user message
        ChatMessage.objects.create(
            session=chat_session,
            sender='user',
            text=user_text
        )
        
        # Generate and save AI reply using Gemini service
        ai_reply = generate_chat_reply(chat_session, user_text)
        
        ChatMessage.objects.create(
            session=chat_session,
            sender='ai',
            text=ai_reply
        )
        
    return redirect('chat_room', chat_id=chat_id)
