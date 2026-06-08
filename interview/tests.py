from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import InterviewSession, InterviewQuestion
from .services import get_fallback_questions, FALLBACK_QUESTIONS

class FallbackQuestionsTests(TestCase):
    def test_all_16_topics_configured(self):
        """Verify that all 16 topics have fallback questions configured."""
        topics = [t[0] for t in InterviewSession.TOPIC_CHOICES]
        for topic in topics:
            self.assertIn(topic, FALLBACK_QUESTIONS, f"Topic '{topic}' is missing from FALLBACK_QUESTIONS!")

    def test_mixed_mode_generates_five_questions(self):
        """Verify that mixed mode returns exactly 5 questions of mixed types."""
        for topic in ['python', 'system_design', 'behavioral']:
            questions = get_fallback_questions(topic, 'medium', 'mixed')
            self.assertEqual(len(questions), 5)
            # Mixed mode should contain at least some different types if possible
            types = {q['type'] for q in questions}
            self.assertTrue(len(types) > 0)

    def test_mcq_mode_generates_only_mcq(self):
        """Verify that MCQ mode generates 5 MCQ questions with options and correct answers."""
        for topic in ['python', 'system_design']:
            questions = get_fallback_questions(topic, 'medium', 'mcq')
            self.assertEqual(len(questions), 5)
            for q in questions:
                self.assertEqual(q['type'], 'mcq')
                self.assertTrue(q['options']['A'])
                self.assertTrue(q['correct_answer'])

    def test_coding_mode_generates_only_coding(self):
        """Verify that coding mode generates 5 coding questions."""
        for topic in ['python', 'data_structures', 'c_prog']:
            questions = get_fallback_questions(topic, 'medium', 'coding')
            self.assertEqual(len(questions), 5)
            for q in questions:
                self.assertEqual(q['type'], 'coding')


class ViewFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')

    def test_dashboard_renders_with_stats(self):
        """Verify dashboard renders and computes stats without VariableDoesNotExist crashes."""
        # Create some sessions
        InterviewSession.objects.create(user=self.user, topic='python', difficulty='easy', mode='mixed', completed=True, score=8.0)
        InterviewSession.objects.create(user=self.user, topic='system_design', difficulty='medium', mode='mcq', completed=True, score=6.0)

        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'interview/dashboard.html')
        
        # Check context keys are passed correctly
        self.assertEqual(response.context['total_attempts'], 2)
        self.assertEqual(response.context['avg_score'], 70.0)  # average of 8.0 and 6.0 is 7.0, scaled is 70.0%
        self.assertEqual(response.context['prog_count'], 1)
        self.assertEqual(response.context['sys_count'], 1)
        self.assertEqual(response.context['core_count'], 0)

    def test_session_start_post(self):
        """Verify starting a session via POST creates models and redirects."""
        url = reverse('session_start')
        data = {
            'topic': 'python',
            'difficulty': 'easy',
            'mode': 'mixed'
        }
        response = self.client.post(url, data)
        # Verify redirect to first question
        session = InterviewSession.objects.filter(user=self.user).first()
        self.assertIsNotNone(session)
        self.assertEqual(session.questions.count(), 5)
        self.assertRedirects(response, reverse('question_view', args=[session.id, 1]))

