DIRECTION WISE

A modern career guidance platform built with Streamlit. It helps you discover the right career path using interactive tools, personalized insights, and real stories.

📋 Table of Contents

1.Project Overview

2.Development Process

3.Installation and Setup

4.Running the Application

5.Project Structure

6.Features

7.Technical Architecture

8.Usage Guide

9.Troubleshooting

10.Who It’s For

11.License

12.Contributing

13.Support

🎯 Project Overview

DIRECTION WISE is a career guidance platform. It combines AI analysis, interactive assessments, and real-world insights to help you choose and grow in a career. You get quizzes, skill analysis, career comparisons, mentorship stories, and market trends in one place.

🏗️ Development Process
Phase 1: Foundation and Core Setup

 Project initialization

Python environment with Streamlit

SQLAlchemy for database management

SQLite for data persistence

Database design

Models for User, Career, Skill, MarketTrend

User authentication system

Sample data seeding

Core backend

counselor_core.py with essential functions

Collaborative filtering setup

Career recommendation engine

Phase 2: User Interface

Authentication

Login and registration

Session management with Streamlit

User profiles

Main application structure

Ten tab navigation

Responsive layout with custom CSS

Interactive components and widgets

Phase 3: Features

Interactive quiz

Twelve personality and career questions

Dynamic results

Personalized recommendations

Collaborative filtering

User based recommendations

CSV and PDF export

Random career suggestions

Career analysis tools

Skill mapping and analysis

Comparison matrices

Market insights and trends

Advanced features

Resume analysis with AI

Mentorship stories

Live intelligence dashboard

Phase 4: Enhancements

UI and brand

Custom logo

Brand identity for DIRECTION WISE

Responsive polish

Data intelligence

Live data simulation

Dynamic content generation

Real time market insights

Export and downloads

PDF generation with ReportLab

CSV export

Rich visualizations

🚀 Installation and Setup
Prerequisites

Python 3.8 or higher

pip

Git

Step 1: Clone the repository
git clone <repository-url>
cd direction-wise
Step 2: Create a virtual environment
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS or Linux
source venv/bin/activate
Step 3: Install dependencies
pip install -r requirements.txt
Step 4: Download NLP models
python -m spacy download en_core_web_sm
Step 5: Initialize the database

The database is created on first run. Sample data seeds automatically.

🏃‍♂️ Running the Application
Development mode
streamlit run app.py
Production mode with custom port
streamlit run app.py --server.port 8501
Access the app

Open your browser.

Go to http://localhost:8501.

Create an account or log in.

Explore your options.

📁 Project Structure

direction-wise/

├── app.py                    # Main Streamlit application

├── counselor_core.py         # Core backend functions and models

├── career_counselor.db       # SQLite database generated at runtime

├── requirements.txt          # Python dependencies

├── README.md                 # Project documentation

└── __pycache__/              # Auto generated cache files

Key files

app.py

Authentication

Ten tab navigation

Quiz logic

Recommendation engine

Visualizations

Export features

counselor_core.py

Database models for User, Career, Skill, MarketTrend

Auth helpers

Recommendation algorithms

Data utilities

Sample data seeding

✨ Features
🧠 Interactive Quiz

Twelve questions on personality, interests, skills

Dynamic scoring

Personalized recommendations

Progress tracking

🤝 Collaborative Filtering

User based recommendations

Export to CSV or PDF

Random suggestions

Popular and trending careers

🗺️ Career Roadmaps

Step by step guides

Skill progression paths

Industry insights

Growth opportunities

🔍 Skill Analysis

Intelligent skill assessment

Skill gap analysis

Career to skill mapping

Improvement suggestions

⚖️ Career Comparison

Side by side comparisons

Salary and growth analysis

Skill overlap visuals

Market demand trends

📊 Market Insights

Real time job market signals

Industry trends and forecasts

Regional distribution

Emerging technologies

💡 Mentorship Stories

Real experiences from professionals

Career journey snapshots

Industry specific advice

Resource recommendations

📄 Resume Analysis

AI powered review

Keyword optimization

Format guidance

ATS compatibility checks

🚀 Live Intelligence

Real time data views

Salary intelligence

Geographic distribution

Technology trends

🔧 Technical Architecture
Frontend

Streamlit

Custom CSS with animations

Interactive widgets, forms, charts

Mobile and desktop ready

Backend

Python 3.8+

SQLAlchemy ORM

SQLite

Session based authentication

AI and Analytics

spaCy and NLTK for NLP

scikit learn for models

Plotly for charts

Pandas and NumPy for data

Export and Reports

ReportLab for PDF

CSV and JSON exports

Interactive Plotly charts

📱 Usage Guide
Get started

Create an account.

Take the quiz.

Review your results.

Compare careers.

Analyze your skills.

Export your findings.

Navigate the app

Use the top tabs to switch modules.

Each tab focuses on one task.

Your results stay in session.

Export options appear where relevant.

Best practices

Complete the full quiz for stronger matches.

Keep your skills profile current.

Compare several options before deciding.

Check market insights for demand signals.

Read mentorship stories for context.

🛠️ Troubleshooting
Common issues

Import errors

pip install -r requirements.txt
python -m spacy download en_core_web_sm

Database issues

rm career_counselor.db
# Then restart the app

Port conflicts

streamlit run app.py --server.port 8502

Memory issues

Close other heavy apps.

Restart the app.

Clear your browser cache.

Performance tips

Use Chrome or Firefox.

Keep fewer tabs open.

Restart the app if it slows down.

Clear cache regularly.

🎯 Who It’s For

Students exploring options

Professionals planning a shift

Career advisors and counselors

Anyone who wants structured guidance

📄 License

For educational and career guidance use.

🤝 Contributing

Fork the repository.

Create a feature branch.

Make changes.

Test thoroughly.

Open a pull request.

📞 Support

Read the troubleshooting section.

Review code comments and docs.

Open an issue in the repository.

Built to help you find a path that fits you.
