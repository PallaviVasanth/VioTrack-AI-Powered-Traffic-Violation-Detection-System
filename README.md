🚦 VioTrack — AI-Powered Traffic Violation Detection System

VioTrack is an AI-assisted traffic violation detection and management system built using Python, Flask, Computer Vision, YOLOv8, OCR, CSV-based data storage, automated email notifications, UPI QR demonstration payments, PDF receipt generation, and analytics.

The project demonstrates an end-to-end workflow for processing traffic images, identifying supported traffic violations, associating vehicle information, maintaining violation records, managing fine-payment workflows, generating proof and receipt documents, and presenting violation analytics through a web interface.

📌 Project Information
Item	Details
Project Name	VioTrack
Full Name	AI-Powered Traffic Violation Detection System
Project Type	MCA Academic / Final-Year Project
Domain	Artificial Intelligence & Full-Stack Development
Backend	Python + Flask
Frontend	HTML, CSS, JavaScript, Jinja Templates
Object Detection	YOLOv8
Computer Vision	OpenCV
OCR	EasyOCR / Tesseract
Data Storage	CSV
Data Processing	Pandas, NumPy
Visualization	Matplotlib
PDF Generation	ReportLab
QR Generation	qrcode
Email	Gmail SMTP
Containerization	Docker
⚠️ IMPORTANT — READ THIS BEFORE RUNNING THE PROJECT

Do not skip this section.

If you return to this project months or years later, start here.

Before running VioTrack, complete all of the following steps.

1. 🔐 Email Credentials — IMPORTANT

The application has an email-sending feature for:

Payment notification emails
Payment links
Payment receipts
PDF receipt delivery

The email system uses Gmail SMTP.

Never put your real email password directly inside app.py.

The application should obtain the credentials from environment variables.

Create a file named:

.env

in the project root.

Example:

EMAIL_SENDER=your-email@gmail.com
EMAIL_PASSWORD=your-google-app-password
2. 🔑 Use a Google App Password

For Gmail SMTP, use a Google App Password rather than your normal Gmail account password.

The App Password should be created from the Google account security settings for the account used to send project emails.

Important security rule

Never commit the following to GitHub:

.env

Never place these directly in source code:

EMAIL_PASSWORD
Gmail password
Google App Password
API keys
Access tokens
3. 🚨 Previously Exposed Email Credential

If an actual Gmail App Password was previously committed to this public repository, do not reuse it.

Before running the project:

Revoke the previously exposed Google App Password.
Generate a new Google App Password.
Store the new value only in .env.
Keep .env out of Git.
Do not paste the new password into app.py.

This step is required because removing a secret from the current source file does not automatically make an already-exposed credential safe.

4. 📄 Create .env

Create:

.env

in the same directory as app.py.

Example:

EMAIL_SENDER=your-email@gmail.com
EMAIL_PASSWORD=your-google-app-password
UPI_ID=your-demo-upi@bank
UPI_NAME=Demo User

Replace the example values with your own values where required.

5. 🚫 Add .env to .gitignore

Make sure .gitignore contains:

.env
.env.*
!.env.example

This prevents your real configuration from being uploaded to GitHub.

6. 📋 Create .env.example

Create:

.env.example

The file should contain dummy/example values only:

EMAIL_SENDER=your-email@gmail.com
EMAIL_PASSWORD=your-google-app-password
UPI_ID=your-demo-upi@bank
UPI_NAME=Demo User
Difference between .env and .env.example
File	Contains real values?	Upload to GitHub?
.env	Yes	❌ No
.env.example	No, only examples	✅ Yes
7. 💳 UPI Configuration

VioTrack contains a UPI QR-code payment demonstration workflow.

The UPI identifier:

pallavi@oksbi

is an example/demo value in the project and is not intended to represent a personal UPI credential.

For your own setup, configure a suitable demonstration/test UPI value.

Example:

UPI_ID=your-demo-upi@bank
UPI_NAME=Demo User
Important

The current payment workflow is a demonstration/simulated payment flow.

It does not connect to a production payment gateway.

Do not treat the payment implementation as a real financial transaction system.

8. 📧 Check the Demo Dataset

The project contains:

data/main_dataset.csv

Before publicly sharing the project, inspect the dataset for personal information.

If personal email addresses are present, replace them with dummy addresses such as:

demo@example.com

or remove them where they are not required.

Do not add real passwords, payment credentials, API keys, or other secrets to the dataset.

9. 🧹 Check the Repository for Secrets

Before pushing changes to GitHub, search the entire project for:

password
EMAIL_PASSWORD
EMAIL_SENDER
smtp
api_key
apikey
token
secret
UPI
gmail.com

Also inspect:

app.py
utils/
data/
configuration files
.env
.env.example
old backup files
notebooks
scripts

Make sure no real credentials remain in tracked files.

10. 🕐 Git History Consideration

If a real password, App Password, API key, or other secret was previously committed, simply deleting it from the current version is not enough.

Git history may still contain the previous value.

Therefore:

Revoke the exposed credential.
Generate a new credential.
Remove the secret from the current source.
If necessary, clean the Git history.
Force-push only after carefully checking the repository.

Never rely on GitHub being unable to see an old secret just because it was removed from the latest commit.

📖 Table of Contents
Project Overview
Features
System Architecture
Technology Stack
Project Structure
Prerequisites
Installation
Environment Configuration
YOLOv8 Model
Tesseract OCR
Running the Application
Application Workflow
Email Workflow
Payment Workflow
PDF Receipt Workflow
Analytics
Data Storage
Testing
Docker
Troubleshooting
Security
Limitations
Future Enhancements
Academic Objective
Disclaimer
Author
📌 Project Overview

Traffic violation monitoring can involve multiple steps, including:

Detecting traffic violations
Identifying vehicles
Recording violation details
Maintaining evidence
Calculating fines
Informing vehicle owners
Managing payments
Generating receipts
Analyzing violation statistics

VioTrack demonstrates how these steps can be combined into a single web application.

The application uses AI-assisted image processing and a Flask backend to create a complete academic demonstration workflow.

✨ Features
🤖 AI-Assisted Detection

The application uses YOLOv8 through Ultralytics for image processing and object detection.

Supported demonstration violation categories include:

Overspeeding
Mobile While Driving
No Parking
Triple Riding
Signal Jump
Helmet-related violations
Overloading
Wrong Lane

The current academic implementation includes predefined mappings for supported demonstration images and violation rules.

🔎 Vehicle Information / OCR

The project contains OCR-related functionality using:

EasyOCR
Tesseract

OCR functionality is used as part of the vehicle-information processing workflow.

The current prototype also contains predefined mappings for supported sample images.

Therefore, this project should be understood as an academic prototype, rather than a production-grade unrestricted number-plate recognition system.

📋 Violation Records

Violation records are stored in:

data/main_dataset.csv

Records can contain:

Vehicle number
Vehicle color
Violation type
Fine amount
Date
Time
Location
Status
Detection confidence
Image information
Email
Payment information
🖼️ Proof Images

The project stores proof images associated with detected violations.

The proof-image directory is:

data/proof_images/

These images can be displayed with violation information.

📧 Email Notifications

VioTrack uses Gmail SMTP for sending email notifications.

The email workflow can be used for:

Payment notifications
Payment links
Receipt notifications
PDF receipt delivery

SMTP configuration:

SMTP Server: smtp.gmail.com
Port: 587
Security: TLS

Credentials should come from environment variables.

Example:

EMAIL_SENDER=your-email@gmail.com
EMAIL_PASSWORD=your-google-app-password
💳 Payment Demonstration

The application contains a payment page and UPI QR-code generation.

The workflow is:

Violation
    ↓
Fine Details
    ↓
Payment Page
    ↓
UPI QR Code
    ↓
Simulated Payment
    ↓
Payment Success

The payment process is for demonstration purposes only.

No real payment gateway is connected.

📄 PDF Receipt

After the simulated payment workflow, VioTrack can generate a PDF receipt.

The receipt can include:

Receipt number
Vehicle number
Violation type
Fine amount
Payment information
Date/time
Other relevant information

PDF generation uses ReportLab.

📊 Analytics Dashboard

VioTrack provides analytics for violation records.

The application can analyze:

Total violations
Violations by type
Paid violations
Pending violations
Fine amounts
Monthly trends

Pandas is used for data processing.

Matplotlib is used for visualization.

🏗️ System Architecture

VioTrack follows a three-layer application architecture.

┌─────────────────────────────────────────┐
│                 FRONTEND                │
│                                         │
│ HTML + CSS + JavaScript + Jinja        │
│                                         │
│ Login                                   │
│ Home                                    │
│ Upload                                  │
│ Violation Details                       │
│ Payment                                 │
│ Analytics                               │
└───────────────────┬─────────────────────┘
                    │
                    │ HTTP Requests
                    ▼
┌─────────────────────────────────────────┐
│              BACKEND / API              │
│                                         │
│ Flask                                   │
│                                         │
│ Authentication                          │
│ Image Upload                            │
│ Detection                               │
│ OCR                                     │
│ Violation Processing                    │
│ CSV Operations                          │
│ Email                                   │
│ Payment Workflow                        │
│ PDF Generation                          │
│ Analytics                               │
└───────────────────┬─────────────────────┘
                    │
        ┌───────────┼───────────┐
        │           │           │
        ▼           ▼           ▼
┌─────────────┐ ┌─────────┐ ┌─────────────┐
│ CSV Storage │ │ AI/OCR  │ │ File Storage │
│             │ │         │ │             │
│ Violations  │ │ YOLOv8  │ │ Images      │
│ Payments    │ │ EasyOCR │ │ Proof       │
│ Status      │ │ Tesseract│ │ QR Codes   │
└─────────────┘ └─────────┘ │ Receipts    │
                            └─────────────┘
🧩 Three-Tier Explanation
1. Frontend

The frontend provides:

Login interface
Home page
Image upload
Violation search/view
Payment interface
Analytics interface

Technologies:

HTML
CSS
JavaScript
Jinja Templates
2. Backend / API Layer

The Flask backend manages:

Routing
Authentication
Image uploads
AI processing
OCR processing
Violation processing
CSV operations
Email
QR generation
PDF generation
Analytics
3. Data / AI Layer

The data and processing layer handles:

YOLOv8 inference
OCR
Image processing
Violation mappings
CSV records
Proof images
QR codes
PDF receipts
🛠️ Technology Stack
Category	Technology
Programming Language	Python
Backend Framework	Flask
Object Detection	YOLOv8
AI Framework	Ultralytics
Computer Vision	OpenCV
OCR	EasyOCR / Tesseract
Data Processing	Pandas
Numerical Processing	NumPy
Image Processing	Pillow
Visualization	Matplotlib
PDF	ReportLab
QR Code	qrcode
Email	Gmail SMTP
Storage	CSV
Server	Gunicorn
Containerization	Docker
📁 Project Structure
VioTrack-AI-Powered-Traffic-Violation-Detection-System/
│
├── app.py
│
├── data/
│   ├── main_dataset.csv
│   ├── images/
│   ├── images_data/
│   ├── proof_images/
│   ├── payment_qr/
│   └── receipts/
│
├── static/
│
├── templates/
│   ├── login.html
│   ├── home.html
│   ├── view_violation.html
│   ├── email_sent.html
│   ├── payment_page.html
│   ├── payment_success.html
│   ├── view_all.html
│   ├── analysis.html
│   ├── analysis_index.html
│   └── single_graph.html
│
├── utils/
│   ├── detection_utils.py
│   ├── ocr_utils.py
│   ├── csv_utils.py
│   └── overlay_utils.py
│
├── Dockerfile
├── Procfile
├── requirements.txt
├── .gitignore
├── .env.example
└── README.md
💻 Prerequisites

Before installing VioTrack, install:

Python 3.8 or newer
pip
Git
Tesseract OCR
Optional: Docker

A virtual environment is strongly recommended.

🚀 Installation
Step 1 — Clone the Repository
git clone https://github.com/PallaviVasanth/VioTrack-AI-Powered-Traffic-Violation-Detection-System.git

Move into the project:

cd VioTrack-AI-Powered-Traffic-Violation-Detection-System
Step 2 — Create a Virtual Environment
Windows
python -m venv venv

Activate:

venv\Scripts\activate
Linux / macOS
python3 -m venv venv

Activate:

source venv/bin/activate
Step 3 — Upgrade pip
python -m pip install --upgrade pip
Step 4 — Install Dependencies
pip install -r requirements.txt

If EasyOCR is not installed by the requirements file:

pip install easyocr
Step 5 — Configure Environment Variables

Create:

.env

Example:

EMAIL_SENDER=your-email@gmail.com
EMAIL_PASSWORD=your-google-app-password
UPI_ID=your-demo-upi@bank
UPI_NAME=Demo User

Do not upload .env to GitHub.

🔐 Environment Configuration

The recommended configuration is:

Project Root
│
├── app.py
├── .env
├── .env.example
└── ...

Example .env:

EMAIL_SENDER=actual-sender-email@gmail.com
EMAIL_PASSWORD=actual-google-app-password
UPI_ID=demo-upi@bank
UPI_NAME=Demo User

Example .env.example:

EMAIL_SENDER=your-email@gmail.com
EMAIL_PASSWORD=your-google-app-password
UPI_ID=your-demo-upi@bank
UPI_NAME=Demo User
Remember

.env = private.

.env.example = public template.

🧠 YOLOv8 Model

VioTrack uses a YOLOv8 model through Ultralytics.

The project uses:

yolov8n.pt

Depending on the environment, Ultralytics may download the model when it is first required.

The model file should not be committed to GitHub unnecessarily.

🔎 Tesseract OCR

The project uses pytesseract for Tesseract integration.

Tesseract itself must be installed separately on the operating system.

After installation, ensure the executable can be located by the application.

If Tesseract is installed in a custom directory, the application may require the appropriate executable path configuration.

▶️ Running the Application

After completing all configuration:

python app.py

The application normally runs on:

http://127.0.0.1:5000

Open the URL in your browser.

🔄 Application Workflow
                     USER
                       │
                       ▼
                    LOGIN
                       │
                       ▼
                     HOME
                       │
                       ▼
                UPLOAD IMAGE
                       │
                       ▼
              YOLOv8 PROCESSING
                       │
                       ▼
            VIOLATION PROCESSING
                       │
                       ▼
            OCR / VEHICLE INFO
                       │
                       ▼
              CREATE RECORD
                       │
                       ▼
                CSV STORAGE
                       │
          ┌────────────┴────────────┐
          │                         │
          ▼                         ▼
   VIEW VIOLATION              ANALYTICS
          │
          ▼
    PAYMENT EMAIL
          │
          ▼
     PAYMENT PAGE
          │
          ▼
       UPI QR
          │
          ▼
   SIMULATED PAYMENT
          │
          ▼
    PAYMENT SUCCESS
          │
          ▼
     PDF RECEIPT
          │
          ▼
     EMAIL RECEIPT
🌐 Main Application Routes

The application includes routes for major workflows such as:

Route	Purpose
/	Login
/home	Home
/upload	Upload/process image
/view_violation/<id>	View violation
/send_payment_email/<id>	Send payment email
/email_sent_success/<id>	Email confirmation
/pay_fine/<id>	Payment page
/qr/<filename>	Serve QR code
/fake_pay_success/<id>	Simulated payment success
/view_all	View all violations
/analysis	Analytics

Route names can change as the application is modified. app.py is the final source of truth for the current route implementation.

📧 Email Workflow

The email workflow is:

Violation Record
       ↓
Recipient Email
       ↓
Flask Email Function
       ↓
Gmail SMTP
       ↓
Email Sent

SMTP:

Server: smtp.gmail.com
Port: 587
TLS: Enabled

Credentials:

EMAIL_SENDER=your-email@gmail.com
EMAIL_PASSWORD=your-google-app-password
💳 Payment Workflow

The payment workflow is:

Violation
    ↓
Fine Details
    ↓
Pay Fine
    ↓
Generate UPI QR
    ↓
Payment Demonstration
    ↓
Payment Success
    ↓
Generate Receipt

The payment flow is simulated for the project demonstration.

📄 Receipt Workflow

After payment demonstration:

Payment Success
      ↓
Receipt Information
      ↓
ReportLab
      ↓
PDF Receipt
      ↓
Receipt Storage
      ↓
Email Delivery

Receipts are stored under:

data/receipts/
📊 Analytics Workflow

Analytics use the CSV dataset.

main_dataset.csv
       ↓
     Pandas
       ↓
Data Processing
       ↓
Statistics
       ↓
Matplotlib
       ↓
Graphs
       ↓
Analytics Dashboard
🗃️ Data Storage

VioTrack currently uses CSV instead of a relational database.

Main dataset:

data/main_dataset.csv

This keeps the academic prototype lightweight and avoids requiring a separate database server.

🖼️ Generated Files

The application can generate files in directories such as:

data/images_data/
data/proof_images/
data/payment_qr/
data/receipts/

These directories may contain:

Uploaded images
Processed images
Proof images
QR codes
PDF receipts

Generated files should be reviewed before committing them to GitHub.

🧪 Testing the Project

After starting the application, use the project's supported demonstration images/data.

Recommended test sequence:

Test 1 — Login

Open:

http://127.0.0.1:5000

Test the login workflow.

Test 2 — Upload

Upload a supported traffic image.

Test 3 — Detection

Check that the image-processing/detection workflow executes.

Test 4 — Violation

Verify the violation type and fine information.

Test 5 — Vehicle Information

Verify the vehicle information generated by the current prototype workflow.

Test 6 — CSV

Check:

data/main_dataset.csv

and verify that the expected record is created/updated.

Test 7 — Proof

Check:

data/proof_images/

for generated proof images.

Test 8 — Email

If email is configured, test the email workflow using an appropriate test recipient.

Test 9 — Payment

Open the payment workflow and verify the generated demonstration QR code.

Test 10 — Receipt

Complete the simulated payment workflow and verify the generated PDF receipt.

Test 11 — Analytics

Open the analytics page and verify that the dataset is processed correctly.

🐳 Docker

The repository contains a Dockerfile.

Build:

docker build -t viotrack .

Run:

docker run -p 5000:5000 viotrack

For email and payment configuration, provide environment variables securely.

Do not permanently embed secrets inside the Docker image.

🔧 Troubleshooting
Problem: ModuleNotFoundError

Example:

ModuleNotFoundError: No module named 'flask'

Solution:

pip install -r requirements.txt

If a specific dependency is missing:

pip install <package-name>
Problem: EasyOCR is missing

Install:

pip install easyocr
Problem: Tesseract is not found

Install Tesseract OCR separately and ensure the executable is available to the application.

Problem: Email is not being sent

Check:

EMAIL_SENDER exists in .env.
EMAIL_PASSWORD contains a valid Google App Password.
The App Password has not been revoked.
The Gmail account allows the configured authentication method.
Port 587 is accessible.
The .env file is located in the project root.
The application is actually loading the environment variables.

Do not solve email problems by hard-coding your password into app.py.

Problem: EMAIL_SENDER is None

Check:

.env

Make sure it contains:

EMAIL_SENDER=your-email@gmail.com

Also make sure the application loads environment variables before accessing them.

Problem: YOLO model cannot be loaded

Check:

yolov8n.pt

and verify that Ultralytics is installed:

pip install ultralytics
Problem: Port 5000 is already in use

Another application may already be using port 5000.

Stop the other process or configure the Flask application to use another available port.

Problem: Images are not displayed

Check that the required directories exist:

data/images/
data/images_data/
data/proof_images/

Also verify that the generated file names match the paths used by the application.

Problem: CSV records are not updated

Check:

data/main_dataset.csv

Make sure:

The file exists.
The application has write permission.
The CSV structure matches what the utility functions expect.
🔐 Security Checklist

Before making the project public:

[ ] No Gmail password in source code
[ ] No Google App Password in source code
[ ] No API keys
[ ] No access tokens
[ ] No personal secrets
[ ] .env is ignored
[ ] .env.example contains dummy values
[ ] Personal emails removed from demo data where appropriate
[ ] Payment configuration reviewed
[ ] Demo UPI used instead of personal payment credentials
[ ] Generated private files reviewed
[ ] Git history checked for previously committed secrets
🛡️ Security Recommendations for Production

VioTrack is an academic prototype.

A production implementation would require additional controls such as:

Secure password hashing
Strong authentication
Role-based authorization
Secure sessions
CSRF protection
Input validation
File-upload validation
File-type restrictions
Rate limiting
Secure cookies
HTTPS
Audit logging
Database access controls
Secret management
Secure payment gateway integration
Privacy controls
Data retention policies
⚠️ Current Limitations

VioTrack is an academic prototype.

Current limitations include:

CSV is used instead of a production database.
The current detection workflow includes predefined mappings for supported demonstration images.
OCR functionality includes predefined sample-image mappings in the current prototype.
The payment system is simulated.
No production payment gateway is integrated.
Gmail SMTP requires user-provided credentials.
Detection performance depends on image quality and model capabilities.
The system has not been validated for real-world traffic enforcement.
Production deployment would require additional security and privacy controls.
The application should not be treated as an official traffic-enforcement platform.
🔮 Future Enhancements

Potential future improvements include:

Real-time CCTV integration
RTSP camera support
Real-time video processing
Improved license-plate recognition
Custom-trained traffic-violation models
PostgreSQL/MySQL integration
REST API separation
Advanced authentication
Role-based access control
Production payment gateway integration
Cloud deployment
Mobile application
Improved Docker deployment
Automated testing
Advanced analytics
Real-time notifications
Location-based traffic monitoring
Model performance monitoring
🧑‍💻 Development Architecture
Frontend Responsibilities

The frontend handles:

User interface
Login
Forms
Image upload
Violation display
Payment interface
Analytics pages
Backend Responsibilities

Flask handles:

HTTP routing
Authentication
Image uploads
Detection workflow
OCR workflow
Violation processing
CSV operations
Email notifications
Payment workflow
QR generation
PDF generation
Analytics
Utility Modules
detection_utils.py

Responsible for detection-related processing.

ocr_utils.py

Responsible for OCR/vehicle-information processing.

csv_utils.py

Responsible for CSV data operations.

overlay_utils.py

Responsible for image overlays/proof-image processing.

📚 Academic Objective

The main objective of VioTrack is to demonstrate how Artificial Intelligence and Full-Stack Web Development can be combined to build an application for traffic-violation management.

The project demonstrates:

Computer Vision
Object Detection
OCR
Python programming
Flask development
Frontend development
CSV data processing
Image processing
Email automation
QR-code generation
PDF generation
Analytics
Full-stack application workflow
🧠 What This Project Demonstrates

From a full-stack engineering perspective, VioTrack demonstrates the integration of multiple application components:

Frontend
   ↓
Flask Backend
   ↓
AI Processing
   ↓
OCR
   ↓
Data Storage
   ↓
Email / Payment Workflow
   ↓
Receipt Generation
   ↓
Analytics

This makes the project a practical demonstration of connecting AI functionality with a complete web application.

📦 Deployment Considerations

Before deploying VioTrack to a public environment:

Environment

Configure:

EMAIL_SENDER
EMAIL_PASSWORD
UPI_ID
UPI_NAME

through secure environment variables.

Storage

The current project uses local files and CSV.

A production deployment should use persistent storage.

Database

A relational database should replace CSV for multi-user production workloads.

Security

HTTPS, authentication hardening, secure file uploads and secret management should be implemented.

AI Model

The model should be evaluated using a representative real-world dataset before any production use.

🔄 Re-running the Project After a Long Time

If you return to this project after months or years, use this checklist.

Step 1

Clone or open the repository.

Step 2

Read this README from the Before Running section.

Step 3

Create a virtual environment.

Step 4

Install:

pip install -r requirements.txt
Step 5

Install/configure Tesseract OCR.

Step 6

Create:

.env
Step 7

Configure:

EMAIL_SENDER=your-email@gmail.com
EMAIL_PASSWORD=your-google-app-password
UPI_ID=your-demo-upi@bank
UPI_NAME=Demo User
Step 8

Make sure .env is ignored by Git.

Step 9

Check that no real credentials exist in the source code.

Step 10

If an old App Password was ever exposed, revoke it and create a new one.

Step 11

Check:

data/main_dataset.csv

for personal information.

Step 12

Make sure the YOLO model is available/downloadable.

Step 13

Run:

python app.py
Step 14

Open:

http://127.0.0.1:5000
Step 15

Test login → upload → detection → violation → payment demo → receipt → analytics.

📝 Before Every GitHub Push

Run through this checklist:

[ ] Code works locally
[ ] No .env committed
[ ] No passwords committed
[ ] No Google App Password committed
[ ] No API keys committed
[ ] No tokens committed
[ ] No personal UPI credentials committed
[ ] Demo UPI configuration checked
[ ] Demo CSV checked
[ ] Personal email addresses reviewed
[ ] Generated files reviewed
[ ] README updated if setup changed
[ ] requirements.txt updated if dependencies changed
⚖️ Disclaimer

VioTrack is developed for academic, educational and demonstration purposes.

It is not intended to function as an actual government or law-enforcement traffic-enforcement system.

The violation records, vehicle information, fine amounts, payment workflow and other generated information are demonstration data.

A production system would require appropriate:

Legal authorization
Security controls
Data protection
Privacy controls
Model validation
Infrastructure testing
Payment compliance
Regulatory approval
Operational monitoring
👩‍💻 Author
Pallavi Vasanth

GitHub:

https://github.com/PallaviVasanth

Project Repository:

https://github.com/PallaviVasanth/VioTrack-AI-Powered-Traffic-Violation-Detection-System

⭐ Open-Source Technologies

VioTrack uses open-source technologies and libraries including:

Flask
Ultralytics YOLO
OpenCV
EasyOCR
Tesseract
Pandas
NumPy
Matplotlib
Pillow
ReportLab
qrcode
Gunicorn
📄 License

If this project is distributed as open source, add an appropriate license file to the repository.

Examples include:

MIT License
Apache License 2.0
GNU GPL

Choose a license based on how you want others to use, modify and distribute the project.

🚀 Quick Start

For someone who already knows the project:

git clone https://github.com/PallaviVasanth/VioTrack-AI-Powered-Traffic-Violation-Detection-System.git

cd VioTrack-AI-Powered-Traffic-Violation-Detection-System

python -m venv venv
Windows
venv\Scripts\activate
Linux/macOS
source venv/bin/activate

Install:

pip install -r requirements.txt

Create .env:

EMAIL_SENDER=your-email@gmail.com
EMAIL_PASSWORD=your-google-app-password
UPI_ID=your-demo-upi@bank
UPI_NAME=Demo User

Then:

python app.py

Open:

http://127.0.0.1:5000
✅ Final Pre-Run Checklist

Before running VioTrack, make sure:

╔══════════════════════════════════════════════════╗
║              VIOTRACK PRE-RUN CHECK              ║
╠══════════════════════════════════════════════════╣
║ [ ] Python installed                             ║
║ [ ] Virtual environment activated                ║
║ [ ] requirements.txt installed                   ║
║ [ ] Tesseract OCR installed                      ║
║ [ ] YOLOv8 model available                       ║
║ [ ] .env created                                 ║
║ [ ] Gmail address configured                     ║
║ [ ] NEW Google App Password configured           ║
║ [ ] OLD exposed App Password revoked             ║
║ [ ] .env added to .gitignore                     ║
║ [ ] .env.example created                         ║
║ [ ] Demo UPI configuration checked               ║
║ [ ] main_dataset.csv reviewed                    ║
║ [ ] Personal emails removed if required          ║
║ [ ] No secrets remain in source code             ║
║ [ ] Git history checked for exposed secrets      ║
║ [ ] Generated files reviewed                     ║
╠══════════════════════════════════════════════════╣
║                  THEN RUN:                       ║
║                                                  ║
║                 python app.py                    ║
╚══════════════════════════════════════════════════╝
🎯 Project Workflow at a Glance
                    VIOTRACK
                       │
                       ▼
                   Web Login
                       │
                       ▼
                Upload Traffic Image
                       │
                       ▼
                  YOLOv8 AI
                       │
                       ▼
              Violation Processing
                       │
                       ▼
               Vehicle Information
                       │
                       ▼
                CSV Data Storage
                       │
          ┌────────────┼────────────┐
          │            │            │
          ▼            ▼            ▼
       Proof        Analytics     Details
       Image
          │
          ▼
      Payment Email
          │
          ▼
       Payment Page
          │
          ▼
        UPI QR
          │
          ▼
   Simulated Payment
          │
          ▼
     PDF Receipt
          │
          ▼
     Email Receipt
⭐ VioTrack

AI + Computer Vision + OCR + Flask + Data Processing + Payment Workflow + Analytics

Built as an academic demonstration of integrating AI functionality with a full-stack web application.
