from canvasapi import Canvas
import db as db
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

def get_canvas_api(canvas_url, canvas_token):
    canvas = Canvas(canvas_url, canvas_token)
    return canvas


def get_assignments(canvas_url, canvas_token,):
    canvas = get_canvas_api(canvas_url, canvas_token)
    user = canvas.get_current_user()
    courses = user.get_courses(enrollment_state="active")
    assignments = []
    for course in courses:
        course_assignments = course.get_assignments(includes=["submission"])
        for assignment in course_assignments:

            
            if is_valid_assignment(assignment, user):
                #print(assignment.name)
                assignments.append([assignment.name, assignment.due_at])
    #print(assignments)
    return assignments

def is_valid_assignment(assignment, user):
    if assignment.due_at:
        due_date = datetime.strptime(assignment.due_at, "%Y-%m-%dT%H:%M:%SZ")
        now = datetime.utcnow()
        submission = assignment.get_submission(user)

        return (due_date > now) and (not submission or not submission.submitted_at)
    return False

def get_discission_posts(canvas_url, canvas_token):
    canvas = get_canvas_api(canvas_url, canvas_token)
    user = canvas.get_user(canvas_token)
    courses = user.get_courses(enrolment_state="active")
    discussions = []
    for course in courses:
        course_discussions = course.get_discussion_topics()
        for discussion in course_discussions:
            if discussion.unread_entries > 0:
                discussions.append(discussion)
    return discussions


if __name__ == "__main__":
    canvas_url = "https://csufullerton.instructure.com/"
    canvas_token = os.getenv("CANVAS_TOKEN")
    assignments = get_assignments(canvas_url, canvas_token)
    print(assignments)