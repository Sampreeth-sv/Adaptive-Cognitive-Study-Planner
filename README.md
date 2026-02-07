# Adaptive-Cognitive-Study-Planner
## An AI-Inspired Adaptive Study Planning System that learns from student progress patterns to optimize cognitive workload.

Behavior-Aware Study Scheduling System for Engineering Students
Author: Sampreeth S V

1. Overview

Engineering students manage multiple technically demanding subjects with different difficulty levels, prerequisites, and cognitive load requirements. Static timetables and basic to-do apps fail because they do not adapt when:
* Some topics feel harder than expected
* Certain subjects require more focus
* Progress slows down
* Priorities change

This project introduces an AI-inspired Adaptive Cognitive Study Planner Planner that dynamically generates personalized weekly study schedules and evolves based on student learning behavior.
Instead of fixed planning, the system continuously adjusts workload using progress patterns, topic difficulty, and subject importance.

2. Problem Being Solved

Students often:
* Study hard but not smart
* Struggle to balance difficult and easy subjects
* Ignore weak areas until exams
* Overload themselves cognitively
* Fail to maintain consistency

Traditional planners cannot:
* Adapt to performance
* Reinforce weak topics
* Balance cognitive load
* Continue unfinished study flow

This system addresses these gaps through adaptive planning logic.


3. Proposed Solution

A smart study planning engine that:
* Generates weekly personalized study plans
* Tracks topic-level progress
* Detects difficult areas automatically
* Reinforces weak topics
* Balances workload using subject credits and intensity modes
* Adapts over time as the student progresses

This creates a structured yet flexible study system for engineering students.

4. Core Features (Phase-1 Implementation)
📅 Adaptive Weekly Study Planner
* Generates a structured weekly schedule
* Assigns topics based on study mode:
    i. Light
   ii.Balanced
  iii.Hardcore
* Continues unfinished topics automatically into the next week

🧩 Topic-Wise Progress Tracking
* Each subject is broken into individual topics
* Topics are tracked independently
* No need for manual rescheduling
* Ensures continuous learning flow

🧠 Cognitive Load Inspired Scheduling
* The system simulates mental workload balancing using:
* Study intensity modes
* Hard topic reinforcement
* Credit-weighted subject allocation
* Hard topics are repeated to ensure deeper learning.

🎯 Credit-Weighted Prioritization
* Subjects with higher credits receive:
* More weekly focus
* Higher topic allocation
* This mimics real academic importance.

🔁 Smart Revision Engine
* Once a subject is completed:
* The system automatically switches to revision mode
* Previously studied topics are reinforced

💻 Coding + Aptitude Integration
Always included in weekly planning

📊 Progress & Motivation Tracking
* Subject-wise progress bars
* Weekly completion percentage
* Study streak counter
* Encourages consistency.

🧘 Optional Commitments Support
Users can add non-academic workloads:
* Projects
* Internship preparation
* Courses 
These are scheduled like regular subjects to balance life and study.

🧠 Intelligent Weak/Strong Area Detection
* Instead of only relying on manual self-assessment, the planner identifies learning patterns automatically:
* Topics requiring multiple completions → treated as weak areas
* Topics frequently revised → given priority reinforcement
* Topics completed quickly → treated as strong areas
* Difficult topics repeated for retention
* This makes the system behavior-aware rather than input-dependent.

📊 Adaptive Signals Used by the System

* The planner dynamically adjusts study plans based on:
* Subject credits → priority weighting
* Topic difficulty → reinforcement cycles
* Completion behavior → weak area detection
* Revision frequency → concept reinforcement
* Study mode → cognitive load control
* Optional workload → life balance
These factors collectively guide schedule generation.

🏗️ Tech Stack
* Python
* Streamlit
* JSON (local persistent storage)
* PyPDF2 (syllabus topic extraction)

⚙️ How It Works
Step 1 — User Inputs
* Subjects
* Credits
* Topics (manual or PDF)
* Optional commitments

Step 2 — Plan Generation
* System creates:
* Adaptive weekly topic schedule

Step 3 — Progress Tracking
* User marks topics as completed:
* Planner updates progress
* Reinforces difficult topics
* Carries unfinished topics forward

Step 4 — Continuous Adaptation
Over time, the system:
* Detects weak areas
* Improves workload distribution
* Maintains study consistency

🧪 Innovation Highlights

* Behavior-driven weak area detection
* Hard topic reinforcement model
* Topic continuation engine
* Cognitive load-inspired scheduling
* Credit-weighted academic prioritization
* Adaptive weekly regeneration
Unlike static planners, this system evolves with user performance

📈 Future Scope (Roadmap)

* Planned intelligent extensions:
* Deadline-aware scheduling
* Confidence-level based prioritization
* Strong/weak topic tagging interface
* Prerequisite dependency mapping
* Learning pace modeling
* Daily calendar view generation
* Time-availability based scheduling
* AI-assisted adaptive recommendations

🖥️ How to Run

pip install -r requirements.txt
streamlit run app.py

📂 Project Structure

app.py – Main Streamlit application  
study_plan.json – Local progress storage  
requirements.txt – Dependencies  
README.md – Project documentation
