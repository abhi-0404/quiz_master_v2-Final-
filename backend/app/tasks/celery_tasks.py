from celery import Celery
from app import create_app, db, mail
from app.models.user import User
from app.models.quiz import Quiz
from app.models.score import Score
from flask_mail import Message
from datetime import datetime, timedelta
import csv
import io
import os

# Create Celery instance
celery = Celery('quiz_master')

# Configure Celery
celery.conf.update(
    broker_url=os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/1'),
    result_backend=os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/2'),
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    beat_schedule={
        'daily-reminder': {
            'task': 'app.tasks.celery_tasks.send_daily_reminders',
            'schedule': 86400.0,  # Run daily (24 hours in seconds)
        },
        'monthly-report': {
            'task': 'app.tasks.celery_tasks.send_monthly_reports',
            'schedule': 2592000.0,  # Run monthly (30 days in seconds)
        },
    }
)

@celery.task
def send_daily_reminders():
    """Send daily reminders to users about new quizzes"""
    app = create_app()
    
    with app.app_context():
        try:
            # Get users who haven't taken any quiz in the last 24 hours
            yesterday = datetime.utcnow() - timedelta(days=1)
            
            # Get all users
            users = User.query.filter_by(role='user').all()
            
            for user in users:
                # Check if user has taken any quiz in the last 24 hours
                recent_attempt = Score.query.filter(
                    Score.user_id == user.id,
                    Score.timestamp_of_attempt >= yesterday
                ).first()
                
                if not recent_attempt:
                    # Check if there are any new quizzes
                    new_quizzes = Quiz.query.filter(
                        Quiz.is_active == True,
                        Quiz.created_at >= yesterday
                    ).all()
                    
                    if new_quizzes or not Score.query.filter_by(user_id=user.id).first():
                        send_reminder_email.delay(user.id, len(new_quizzes))
            
            return "Daily reminders sent successfully"
            
        except Exception as e:
            return f"Error sending daily reminders: {str(e)}"

@celery.task
def send_reminder_email(user_id, new_quiz_count):
    """Send reminder email to a specific user"""
    app = create_app()
    
    with app.app_context():
        try:
            user = User.query.get(user_id)
            if not user:
                return f"User {user_id} not found"
            
            subject = "Quiz Master - Daily Reminder"
            
            if new_quiz_count > 0:
                body = f"""
                Hello {user.full_name},
                
                We have {new_quiz_count} new quiz(es) available on Quiz Master!
                
                Don't miss out on testing your knowledge. Visit our platform and take a quiz today.
                
                Best regards,
                Quiz Master Team
                """
            else:
                body = f"""
                Hello {user.full_name},
                
                It's been a while since your last quiz attempt. 
                
                Visit Quiz Master and challenge yourself with our available quizzes.
                
                Best regards,
                Quiz Master Team
                """
            
            msg = Message(
                subject=subject,
                recipients=[user.email],
                body=body
            )
            
            mail.send(msg)
            return f"Reminder email sent to {user.email}"
            
        except Exception as e:
            return f"Error sending email to user {user_id}: {str(e)}"

@celery.task
def send_monthly_reports():
    """Send monthly activity reports to all users"""
    app = create_app()
    
    with app.app_context():
        try:
            # Get all users
            users = User.query.filter_by(role='user').all()
            
            for user in users:
                generate_monthly_report.delay(user.id)
            
            return "Monthly reports generation initiated"
            
        except Exception as e:
            return f"Error initiating monthly reports: {str(e)}"

@celery.task
def generate_monthly_report(user_id):
    """Generate and send monthly report for a specific user"""
    app = create_app()
    
    with app.app_context():
        try:
            user = User.query.get(user_id)
            if not user:
                return f"User {user_id} not found"
            
            # Get user's scores from the last month
            last_month = datetime.utcnow() - timedelta(days=30)
            monthly_scores = Score.query.filter(
                Score.user_id == user_id,
                Score.timestamp_of_attempt >= last_month
            ).all()
            
            if not monthly_scores:
                return f"No quiz attempts in the last month for user {user.email}"
            
            # Calculate statistics
            total_quizzes = len(monthly_scores)
            total_questions = sum(score.total_questions for score in monthly_scores)
            total_correct = sum(score.total_scored for score in monthly_scores)
            average_score = (total_correct / total_questions * 100) if total_questions > 0 else 0
            
            # Generate HTML report
            html_content = f"""
            <html>
            <head>
                <title>Monthly Quiz Report - {user.full_name}</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 20px; }}
                    .header {{ background-color: #007bff; color: white; padding: 20px; text-align: center; }}
                    .content {{ padding: 20px; }}
                    .stats {{ background-color: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 5px; }}
                    .quiz-item {{ border-bottom: 1px solid #dee2e6; padding: 10px 0; }}
                    table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
                    th, td {{ border: 1px solid #dee2e6; padding: 8px; text-align: left; }}
                    th {{ background-color: #e9ecef; }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>Monthly Quiz Report</h1>
                    <p>Report for {user.full_name}</p>
                    <p>Period: {last_month.strftime('%B %d, %Y')} - {datetime.utcnow().strftime('%B %d, %Y')}</p>
                </div>
                
                <div class="content">
                    <div class="stats">
                        <h2>Summary Statistics</h2>
                        <p><strong>Total Quizzes Attempted:</strong> {total_quizzes}</p>
                        <p><strong>Total Questions Answered:</strong> {total_questions}</p>
                        <p><strong>Total Correct Answers:</strong> {total_correct}</p>
                        <p><strong>Average Score:</strong> {average_score:.2f}%</p>
                    </div>
                    
                    <h2>Quiz Details</h2>
                    <table>
                        <thead>
                            <tr>
                                <th>Quiz Title</th>
                                <th>Date Attempted</th>
                                <th>Score</th>
                                <th>Percentage</th>
                                <th>Time Taken</th>
                            </tr>
                        </thead>
                        <tbody>
            """
            
            for score in monthly_scores:
                percentage = (score.total_scored / score.total_questions * 100) if score.total_questions > 0 else 0
                time_taken = f"{score.time_taken // 60}:{score.time_taken % 60:02d}" if score.time_taken else "N/A"
                
                html_content += f"""
                            <tr>
                                <td>{score.quiz.title if score.quiz else 'Unknown Quiz'}</td>
                                <td>{score.timestamp_of_attempt.strftime('%Y-%m-%d %H:%M')}</td>
                                <td>{score.total_scored}/{score.total_questions}</td>
                                <td>{percentage:.2f}%</td>
                                <td>{time_taken}</td>
                            </tr>
                """
            
            html_content += """
                        </tbody>
                    </table>
                </div>
            </body>
            </html>
            """
            
            # Send email with HTML report
            subject = f"Monthly Quiz Report - {datetime.utcnow().strftime('%B %Y')}"
            
            msg = Message(
                subject=subject,
                recipients=[user.email],
                html=html_content
            )
            
            mail.send(msg)
            return f"Monthly report sent to {user.email}"
            
        except Exception as e:
            return f"Error generating monthly report for user {user_id}: {str(e)}"

@celery.task
def export_user_quiz_data(user_id):
    """Export user's quiz data as CSV"""
    app = create_app()
    
    with app.app_context():
        try:
            user = User.query.get(user_id)
            if not user:
                return {"error": f"User {user_id} not found"}
            
            # Get all user's quiz attempts
            scores = Score.query.filter_by(user_id=user_id).order_by(Score.timestamp_of_attempt.desc()).all()
            
            if not scores:
                return {"error": "No quiz attempts found for this user"}
            
            # Create CSV content
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Write header
            writer.writerow([
                'Quiz ID',
                'Quiz Title',
                'Chapter',
                'Subject',
                'Date Attempted',
                'Score',
                'Total Questions',
                'Percentage',
                'Time Taken (seconds)',
                'Remarks'
            ])
            
            # Write data
            for score in scores:
                quiz = score.quiz
                chapter_name = quiz.chapter.name if quiz and quiz.chapter else 'Unknown'
                subject_name = quiz.chapter.subject.name if quiz and quiz.chapter and quiz.chapter.subject else 'Unknown'
                percentage = (score.total_scored / score.total_questions * 100) if score.total_questions > 0 else 0
                
                remarks = ""
                if percentage >= 90:
                    remarks = "Excellent"
                elif percentage >= 75:
                    remarks = "Good"
                elif percentage >= 60:
                    remarks = "Average"
                else:
                    remarks = "Needs Improvement"
                
                writer.writerow([
                    score.quiz_id,
                    quiz.title if quiz else 'Unknown Quiz',
                    chapter_name,
                    subject_name,
                    score.timestamp_of_attempt.strftime('%Y-%m-%d %H:%M:%S'),
                    score.total_scored,
                    score.total_questions,
                    f"{percentage:.2f}%",
                    score.time_taken or 0,
                    remarks
                ])
            
            csv_content = output.getvalue()
            output.close()
            
            # Send email with CSV attachment
            subject = f"Quiz Data Export - {user.full_name}"
            body = f"""
            Hello {user.full_name},
            
            Your quiz data export has been completed. Please find the CSV file attached.
            
            The file contains details of all your quiz attempts including scores, dates, and performance remarks.
            
            Best regards,
            Quiz Master Team
            """
            
            msg = Message(
                subject=subject,
                recipients=[user.email],
                body=body
            )
            
            # Attach CSV file
            msg.attach(
                filename=f"quiz_data_{user.full_name.replace(' ', '_')}_{datetime.utcnow().strftime('%Y%m%d')}.csv",
                content_type="text/csv",
                data=csv_content
            )
            
            mail.send(msg)
            
            return {
                "success": True,
                "message": f"Quiz data exported and sent to {user.email}",
                "total_records": len(scores)
            }
            
        except Exception as e:
            return {"error": f"Error exporting quiz data for user {user_id}: {str(e)}"}

@celery.task
def export_admin_user_data():
    """Export all user performance data for admin"""
    app = create_app()
    
    with app.app_context():
        try:
            # Get admin user
            admin = User.query.filter_by(role='admin').first()
            if not admin:
                return {"error": "Admin user not found"}
            
            # Get all users with their performance data
            users = User.query.filter_by(role='user').all()
            
            if not users:
                return {"error": "No users found"}
            
            # Create CSV content
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Write header
            writer.writerow([
                'User ID',
                'Full Name',
                'Email',
                'Qualification',
                'Date of Birth',
                'Registration Date',
                'Total Quizzes Taken',
                'Average Score (%)',
                'Best Score (%)',
                'Last Quiz Date',
                'Performance Level'
            ])
            
            # Write data
            for user in users:
                scores = Score.query.filter_by(user_id=user.id).all()
                total_quizzes = len(scores)
                
                if total_quizzes > 0:
                    percentages = [(score.total_scored / score.total_questions * 100) for score in scores if score.total_questions > 0]
                    avg_score = sum(percentages) / len(percentages) if percentages else 0
                    best_score = max(percentages) if percentages else 0
                    last_quiz_date = max(score.timestamp_of_attempt for score in scores).strftime('%Y-%m-%d')
                    
                    # Determine performance level
                    if avg_score >= 85:
                        performance = "Excellent"
                    elif avg_score >= 70:
                        performance = "Good"
                    elif avg_score >= 55:
                        performance = "Average"
                    else:
                        performance = "Below Average"
                else:
                    avg_score = 0
                    best_score = 0
                    last_quiz_date = "Never"
                    performance = "No Attempts"
                
                writer.writerow([
                    user.id,
                    user.full_name,
                    user.email,
                    user.qualification,
                    user.dob.strftime('%Y-%m-%d'),
                    user.created_at.strftime('%Y-%m-%d'),
                    total_quizzes,
                    f"{avg_score:.2f}",
                    f"{best_score:.2f}",
                    last_quiz_date,
                    performance
                ])
            
            csv_content = output.getvalue()
            output.close()
            
            # Send email with CSV attachment
            subject = "User Performance Data Export"
            body = """
            Hello Administrator,
            
            The user performance data export has been completed. Please find the CSV file attached.
            
            The file contains comprehensive performance data for all registered users including quiz statistics and performance levels.
            
            Best regards,
            Quiz Master System
            """
            
            msg = Message(
                subject=subject,
                recipients=[admin.email],
                body=body
            )
            
            # Attach CSV file
            msg.attach(
                filename=f"user_performance_data_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.csv",
                content_type="text/csv",
                data=csv_content
            )
            
            mail.send(msg)
            
            return {
                "success": True,
                "message": f"User performance data exported and sent to {admin.email}",
                "total_users": len(users)
            }
            
        except Exception as e:
            return {"error": f"Error exporting user performance data: {str(e)}"}
