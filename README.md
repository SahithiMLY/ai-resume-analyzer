# 🤖 AI Resume Analyzer and Job Recommendation System

An AI-powered Resume Analyzer that extracts information from PDF/DOCX resumes, identifies candidate skills, recommends suitable job roles, analyzes skill gaps, and generates a personalized learning roadmap.

---

## 📌 Project Overview

The **AI Resume Analyzer and Job Recommendation System** is a web-based application developed using Python and Streamlit.

The system allows users to upload their resume in PDF or DOCX format. The application extracts the resume text, identifies relevant skills, compares the resume with multiple job roles using **TF-IDF and Cosine Similarity**, and provides personalized job recommendations.

The system also allows users to select a target job role and analyze:

- Target role match score
- Matched skills
- Missing skills
- Skill coverage
- Personalized learning roadmap
- Job-role similarity
- Downloadable analysis report

---

## 🎯 Objectives

The main objectives of this project are:

1. Extract text from PDF and DOCX resumes.
2. Identify technical and professional skills from resumes.
3. Compare resumes with multiple predefined job roles.
4. Recommend the top 3 suitable job roles.
5. Calculate resume-to-job similarity using TF-IDF and Cosine Similarity.
6. Analyze the skill gap for a selected target role.
7. Generate a personalized learning roadmap.
8. Provide an interactive web interface using Streamlit.
9. Generate a downloadable resume analysis report.

---

## ✨ Features

### 📄 Resume Upload

Users can upload resumes in:

- PDF format
- DOCX format

The application automatically extracts the resume content.

### 🔍 Resume Text Extraction

The system supports resume text extraction using:

- PyMuPDF
- python-docx
- Tesseract OCR for scanned or image-based PDF resumes

### 🧠 Skill Extraction

The system identifies skills from the extracted resume text using a predefined skill dictionary.

Examples include:

- Python
- SQL
- Oracle
- Analytics
- Digital Marketing
- Social Media
- SEO
- Machine Learning
- Docker
- AWS

### 💼 Job Recommendation

The resume is compared against multiple predefined job roles.

The system can recommend roles such as:

- Digital Marketing Specialist
- Brand Manager
- SEO Specialist
- Social Media Manager
- Content Strategist
- Marketing Analyst
- Public Relations Specialist
- Project Coordinator
- Business Analyst
- Data Analyst

The **Top 3 recommended job roles** are displayed based on similarity scores.

### 📊 TF-IDF and Cosine Similarity

The application uses **TF-IDF (Term Frequency-Inverse Document Frequency)** to convert text into numerical vectors.

**Cosine Similarity** is then used to measure the similarity between the resume and each job role.

The similarity score is displayed as a percentage.

### 🎯 Target Role Analysis

Users can select a target job role and view:

- Skill Match percentage
- TF-IDF similarity
- Required skills
- Matched skills
- Missing skills

### 🧩 Skill Gap Analysis

The system identifies skills required for the selected target role that are not detected in the resume.

This helps users understand which skills they can improve.

### 📚 Personalized Learning Roadmap

A personalized roadmap is generated based on the identified skill gaps.

The roadmap organizes missing skills into weekly learning topics.

### 📈 Data Visualization

The application provides visualizations such as:

- Resume-to-job similarity chart
- Target-role skill coverage chart

### 📥 Downloadable Analysis Report

Users can download a report containing the results of their resume analysis.

---

## 🏗️ System Architecture

```text
                 ┌──────────────────────┐
                 │      User Resume     │
                 │      PDF / DOCX      │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │   Resume Extraction  │
                 │ PyMuPDF / DOCX / OCR │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │     Text Cleaning    │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │   Skill Extraction   │
                 └──────────┬───────────┘
                            │
                ┌───────────┴───────────┐
                ▼                       ▼
       ┌─────────────────┐     ┌─────────────────┐
       │ Job Role Dataset│     │ Skill Dictionary│
       └────────┬────────┘     └────────┬────────┘
                │                       │
                └───────────┬───────────┘
                            ▼
                 ┌──────────────────────┐
                 │ TF-IDF + Cosine      │
                 │ Similarity            │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │ Job Recommendations  │
                 │       Top 3           │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │   Target Role        │
                 │     Analysis         │
                 └──────────┬───────────┘
                            │
                ┌───────────┴───────────┐
                ▼                       ▼
       ┌─────────────────┐     ┌─────────────────┐
       │   Skill Gap     │     │ Learning        │
       │    Analysis     │     │ Roadmap         │
       └─────────────────┘     └─────────────────┘
```

---

## 📁 Project Structure

```text
ai_resume_analyzer/
│
├── data/
│   ├── job_roles.csv
│   └── skill_dictionary.csv
│
├── app.py
├── resume_parser.py
├── text_cleaner.py
├── skill_extractor.py
├── job_matcher.py
├── skill_gap.py
├── roadmap_generator.py
│
├── test_parser.py
├── test_analyzer.py
│
├── sample_resume.pdf
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application development |
| Streamlit | Web application interface |
| PyMuPDF | PDF text extraction |
| python-docx | DOCX text extraction |
| Tesseract OCR | OCR for scanned/image-based PDFs |
| Pandas | Dataset handling |
| NumPy | Numerical processing |
| Scikit-learn | TF-IDF and Cosine Similarity |
| Plotly | Data visualization |
| ReportLab | Analysis report generation |

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
```

### 2. Open the project folder

```bash
cd ai_resume_analyzer
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

For Windows PowerShell:

```bash
venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Application

Run the Streamlit application:

```bash
streamlit run app.py
```

The application will open in your browser.

Usually the local address is:

```text
http://localhost:8501
```

---

## 🔬 How the System Works

### Step 1: Resume Upload

The user uploads a PDF or DOCX resume.

### Step 2: Resume Text Extraction

The application extracts text from the uploaded resume.

If the PDF does not contain an accessible text layer, OCR is used to recognize the text from the document image.

### Step 3: Text Cleaning

The extracted text is cleaned and normalized before further processing.

### Step 4: Skill Extraction

The system compares the resume text against the predefined skill dictionary and identifies detected skills.

### Step 5: Job Matching

The resume is compared with the available job-role dataset.

### Step 6: Similarity Calculation

TF-IDF represents the resume and job-role text as numerical vectors.

Cosine Similarity calculates their similarity.

### Step 7: Job Recommendations

The job roles are ranked according to their similarity scores.

The top 3 roles are displayed as recommendations.

### Step 8: Target Role Analysis

The user selects a target job role.

The system calculates the candidate's skill coverage for that role.

### Step 9: Skill Gap Analysis

Required skills that are not detected in the resume are displayed as missing skills.

### Step 10: Learning Roadmap

The system generates a personalized learning roadmap based on the identified skill gaps.

### Step 11: Report Generation

The user can download an analysis report containing the results.

---

## 📊 Example Output

For a resume containing skills such as:

```text
Oracle
Analytics
Digital Marketing
Social Media
Content Strategy
SEO
Public Relations
Leadership
```

the system can recommend roles such as:

```text
1. Digital Marketing Specialist
2. Brand Manager
3. SEO Specialist
```

The application also displays:

- Match scores
- Job similarity visualization
- Target-role analysis
- Matched skills
- Missing skills
- Skill coverage chart
- Personalized learning roadmap
- Downloadable report

---

## 🧪 Testing

The project includes testing scripts to verify the major components of the system.

Testing includes:

- Resume text extraction
- OCR-based extraction
- Skill extraction
- Job recommendation
- Similarity calculation
- Target-role analysis

Example:

```bash
python test_analyzer.py
```

---

## ⚠️ Limitations

The current version has some limitations:

- Skill extraction is based on a predefined skill dictionary.
- Job-role information comes from a predefined dataset.
- TF-IDF is a text-based similarity technique and does not fully understand semantic meaning.
- Skills expressed using uncommon synonyms may not always be detected.
- Job recommendations should be treated as guidance rather than guaranteed employment predictions.

---

## 🔐 Responsible AI

This application is designed as an assistive career-planning tool.

The recommendations should not be treated as final hiring decisions.

The system does not determine whether a candidate should be hired or rejected.

Users should consider additional factors such as:

- Education
- Work experience
- Career interests
- Professional goals
- Additional skills

before making career decisions.

---

## 🚀 Future Enhancements

Possible future improvements include:

- Advanced NLP-based skill extraction
- Semantic embeddings
- Transformer-based resume analysis
- Larger job-role datasets
- Real-time job listings
- ATS compatibility analysis
- Resume improvement suggestions
- Education and experience extraction
- Multilingual resume support
- More detailed learning resources
- Cloud deployment
- User authentication
- Saved analysis history

---

## 👩‍💻 Author

**Srujana Reddy**

AI Resume Analyzer and Job Recommendation System

---

## 📜 License

This project is developed for educational and academic purposes.