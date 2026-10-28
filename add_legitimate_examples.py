
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data" / "spam_assassin.csv"
OUTPUT_PATH = ROOT / "data" / "legitimate_examples.csv"

examples = [
    """Subject: Interview Schedule Confirmation

Dear Harshad,
Thank you for applying for the Software Developer position.
We would like to invite you for an interview on Tuesday at 11 AM.
Please reply to confirm your availability.
Regards,
Recruitment Team""",

    """Subject: Application Received

Dear Applicant,
Thank you for submitting your application.
Our recruitment team will review your details and contact you
if your qualifications match the role.
Regards,
Talent Acquisition Team""",

    """Subject: Interview Availability

Hello,
We would like to arrange an interview to discuss your experience
and the responsibilities of the position.
Please share your availability for this week.
Regards,
Recruitment Team""",

    """Subject: Interview Confirmation

Dear Candidate,
This email confirms your interview appointment for the
Software Engineer position. Please reply if you need to
reschedule the meeting.
Regards,
Human Resources""",

    """Subject: Thank You for Attending the Interview

Dear Candidate,
Thank you for taking the time to meet our team.
We will review the interview feedback and contact you
regarding the next steps.
Regards,
Hiring Team""",

    """Subject: Technical Interview Details

Hello,
Your technical interview is scheduled for Wednesday at 10 AM.
Please join using the meeting details provided in your
application portal.
Regards,
Recruitment Coordinator""",

    """Subject: Job Application Update

Dear Applicant,
We are writing to provide an update on your application.
The selection process is ongoing, and we will share further
information when a decision has been made.
Regards,
HR Department""",

    """Subject: Request for Interview Availability

Dear Candidate,
We have reviewed your application and would like to discuss
your qualifications in a short interview.
Please let us know which days work best for you.
Regards,
Recruitment Team""",
]

new_df = pd.DataFrame({
    "text": examples,
    "label": ["Not Spam"] * len(examples),
})

# Remove exact duplicates from the additional examples.
new_df = new_df.drop_duplicates(subset=["text"])

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
new_df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8")

print("Created:", OUTPUT_PATH)
print("Legitimate examples:", len(new_df))
print("Original dataset unchanged:", DATA_PATH.exists())
