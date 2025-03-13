import pandas as pd
import numpy as np
import random
from faker import Faker
import json
from datetime import datetime, timedelta
import re
from tqdm import tqdm

# Initialize Faker with Indian context
fake = Faker('en_IN')
Faker.seed(42)  # For reproducibility
random.seed(42)
np.random.seed(42)

# Define Indian tech job categories - Enhanced with more balanced categories
TECH_CATEGORIES = [
    "Software Development",
    "Data Science",
    "Machine Learning Engineering",
    "Full Stack Development",
    "DevOps Engineering",  # Increased representation
    "Cloud Architecture",  # Increased representation
    "Frontend Development",
    "Backend Development",
    "Mobile App Development",
    "UI/UX Design",
    "QA & Testing",
    "Cybersecurity",
    "Database Administration",  # Increased representation
    "Product Management",
    "Business Intelligence",
    "ERP/SAP Consultant",
    "Technical Support",
    "Systems Administration",
    "Network Engineering",
    "IT Project Management",
    "Data Engineering",  # Added new category
    "IoT Development",   # Added new category
    "Embedded Systems"   # Added new category
]

# Tech skills by category with Indian tech market relevance
TECH_SKILLS = {
    "Software Development": [
        "Java", "C++", "Python", "C#", ".NET", "Spring Boot", "Hibernate", "JSP",
        "Servlets", "REST API", "Microservices", "Git", "SVN", "Maven", "Gradle",
        "JUnit", "TestNG", "Design Patterns", "OOP", "SQL", "Data Structures", "Algorithms"
    ],
    "Data Science": [
        "Python", "R", "SQL", "Pandas", "NumPy", "SciPy", "Scikit-learn", "TensorFlow",
        "PyTorch", "Tableau", "Power BI", "Statistical Analysis", "Hypothesis Testing",
        "A/B Testing", "Machine Learning", "Data Mining", "Big Data", "Hadoop", "Spark",
        "Data Visualization", "SPSS", "SAS", "Excel", "Data Warehousing", "ETL"
    ],
    "Machine Learning Engineering": [
        "TensorFlow", "PyTorch", "Scikit-learn", "Keras", "Neural Networks", "Deep Learning",
        "Computer Vision", "NLP", "Reinforcement Learning", "MLOps", "Feature Engineering",
        "Model Deployment", "Python", "R", "Algorithm Design", "MLflow", "Kubeflow",
        "Data Preprocessing", "AWS SageMaker", "Azure ML", "Google AI Platform"
    ],
    "DevOps Engineering": [
        "Docker", "Kubernetes", "Jenkins", "GitLab CI", "GitHub Actions", "AWS", "Azure",
        "GCP", "Terraform", "Ansible", "Puppet", "Chef", "Infrastructure as Code",
        "Monitoring", "Prometheus", "Grafana", "ELK Stack", "Linux", "Shell Scripting",
        "CI/CD", "Nagios", "Zabbix", "Redis", "CloudFormation", "Nginx", "Apache"
    ],
    "Cloud Architecture": [
        "AWS", "Azure", "GCP", "Oracle Cloud", "Cloud Migration", "Serverless", "Lambda",
        "Azure Functions", "Cloud Security", "Kubernetes", "Docker", "Microservices",
        "API Gateway", "Load Balancing", "Auto Scaling", "Infrastructure as Code",
        "Terraform", "CloudFormation", "Cost Optimization", "Multi-cloud", "Hybrid Cloud"
    ],
    "Frontend Development": [
        "HTML", "CSS", "JavaScript", "TypeScript", "React", "Angular", "Vue.js", "Redux",
        "NextJS", "Bootstrap", "Material UI", "Tailwind CSS", "SASS", "LESS", "jQuery",
        "Responsive Design", "Web Accessibility", "Webpack", "Babel", "Jest", "Cypress"
    ],
    "Backend Development": [
        "Node.js", "Express.js", "Django", "Flask", "Spring Boot", "Laravel", "ASP.NET",
        "Ruby on Rails", "PHP", "RESTful APIs", "GraphQL", "Microservices", "SQL", "NoSQL",
        "MongoDB", "MySQL", "PostgreSQL", "Redis", "RabbitMQ", "Kafka", "JWT", "OAuth"
    ],
    "Full Stack Development": [
        "JavaScript", "TypeScript", "React", "Angular", "Node.js", "Express.js", "MongoDB",
        "MySQL", "PostgreSQL", "REST APIs", "GraphQL", "HTML", "CSS", "Git", "Docker",
        "AWS", "MERN Stack", "MEAN Stack", "Full Software Lifecycle", "Redux", "Agile"
    ],
    "Mobile App Development": [
        "Android", "Kotlin", "Java", "iOS", "Swift", "React Native", "Flutter", "Xamarin",
        "Mobile UI Design", "Firebase", "SQLite", "Room", "CoreData", "Push Notifications",
        "Offline Storage", "REST APIs", "JSON", "XML", "Play Store", "App Store", "Jetpack"
    ],
    "UI/UX Design": [
        "Figma", "Adobe XD", "Sketch", "InVision", "Prototyping", "Wireframing", "User Research",
        "Usability Testing", "Information Architecture", "Interaction Design", "Visual Design",
        "Responsive Design", "Design Systems", "Accessibility", "User Personas", "User Flows",
        "Photoshop", "Illustrator", "Zeplin", "Material Design", "Human Interface Guidelines"
    ],
    "QA & Testing": [
        "Manual Testing", "Automated Testing", "Selenium", "Cypress", "Appium", "JMeter", "Postman",
        "TestNG", "JUnit", "Test Planning", "Test Cases", "Bug Reporting", "JIRA", "QA Processes",
        "Performance Testing", "Security Testing", "Mobile Testing", "API Testing", "BDD", "Cucumber"
    ],
    "Cybersecurity": [
        "Network Security", "Penetration Testing", "Vulnerability Assessment", "Security Auditing",
        "SIEM", "Incident Response", "Security Architecture", "Risk Management", "Compliance",
        "Authentication", "Authorization", "Encryption", "Firewall Management", "OWASP", "Ethical Hacking",
        "SOC", "ISO 27001", "VAPT", "CISSP", "CEH", "CCNA Security", "CySA+"
    ],
    "Database Administration": [
        "SQL", "MySQL", "PostgreSQL", "Oracle", "SQL Server", "MongoDB", "Redis", "Cassandra",
        "Database Design", "Query Optimization", "Database Security", "Backup and Recovery",
        "High Availability", "Replication", "Sharding", "Data Modeling", "ETL", "OLAP",
        "Database Performance Tuning", "NoSQL", "PL/SQL", "T-SQL", "Database Monitoring"
    ],
    "Product Management": [
        "Product Strategy", "Roadmapping", "User Stories", "Agile", "Scrum", "Kanban",
        "Market Analysis", "Competitive Analysis", "A/B Testing", "Feature Prioritization",
        "Product Analytics", "User Research", "Customer Interviews", "Product Metrics",
        "JIRA", "Confluence", "Product Launch", "Go-To-Market Strategy", "Stakeholder Management"
    ],
    "Business Intelligence": [
        "SQL", "ETL", "Data Warehousing", "Tableau", "Power BI", "Data Modeling", "Reporting",
        "Dashboard Creation", "KPI Development", "Excel", "Data Analysis", "Business Analysis",
        "Data Visualization", "OLAP", "Data Mining", "Looker", "QlikView", "SSAS", "SSIS", "SSRS"
    ],
    "ERP/SAP Consultant": [
        "SAP", "SAP ABAP", "SAP FICO", "SAP MM", "SAP SD", "SAP HCM", "S/4 HANA", "Oracle ERP",
        "Microsoft Dynamics", "Odoo", "Tally", "ERP Implementation", "ERP Integration",
        "Business Process Mapping", "BPR", "System Analysis", "Business Analysis",
        "Process Optimization", "SAP Modules", "Change Management", "Training & Documentation"
    ],
    "Technical Support": [
        "Troubleshooting", "Help Desk", "Customer Service", "Technical Documentation",
        "System Monitoring", "Network Diagnostics", "Windows", "Linux", "macOS",
        "Active Directory", "Remote Support", "Ticketing Systems", "ServiceNow", "ITIL",
        "Hardware Support", "Software Support", "VPN", "RDP", "Desktop Support"
    ],
    "Systems Administration": [
        "Windows Server", "Linux Administration", "Active Directory", "Exchange Server",
        "VMware", "Hyper-V", "Virtualization", "Server Hardware", "Backup & Recovery",
        "Disaster Recovery", "Group Policy", "PowerShell", "Bash", "System Monitoring",
        "Patch Management", "Security Implementation", "DNS", "DHCP", "LDAP", "SSO"
    ],
    "Network Engineering": [
        "Cisco", "Juniper", "Routing", "Switching", "Firewalls", "VPN", "LAN", "WAN", "SD-WAN",
        "Network Security", "TCP/IP", "OSPF", "BGP", "VLANs", "Wireless Networks", "Network Monitoring",
        "Troubleshooting", "Load Balancers", "Proxies", "DNS", "DHCP", "QoS", "Network Design"
    ],
    "IT Project Management": [
        "Project Planning", "Agile", "Scrum", "Waterfall", "JIRA", "Confluence", "MS Project",
        "Risk Management", "Stakeholder Management", "Resource Planning", "Budgeting",
        "Software Development Lifecycle", "Team Leadership", "Project Tracking", "Reporting",
        "Process Improvement", "Release Management", "PMP", "PRINCE2", "Change Management"
    ],
    # New Categories
    "Data Engineering": [
        "Apache Spark", "Hadoop", "ETL", "Data Pipelines", "Kafka", "Airflow", 
        "AWS Glue", "Databricks", "Azure Data Factory", "Python", "SQL", "NoSQL", 
        "Data Warehousing", "Snowflake", "Big Data", "Data Modeling", "Redshift", 
        "BigQuery", "Data Lakes", "Hive", "Scala", "Parquet", "Avro"
    ],
    "IoT Development": [
        "Arduino", "Raspberry Pi", "MQTT", "IoT Protocols", "Embedded C", "Python",
        "Sensor Integration", "ESP32", "AWS IoT", "Azure IoT Hub", "Edge Computing",
        "Low Power WAN", "Zigbee", "Bluetooth LE", "Real-time OS", "CoAP", "OPC UA"
    ],
    "Embedded Systems": [
        "C", "C++", "Microcontrollers", "RTOS", "ARM", "Circuit Design", "PCB Layout",
        "Firmware", "Embedded Linux", "Device Drivers", "Digital Signal Processing",
        "Assembly Language", "SoC", "FPGA", "Hardware Interfacing", "Verilog", "VHDL"
    ]
}

# Define Indian tech degree programs
TECH_DEGREES = [
    "B.Tech", "B.E.", "M.Tech", "M.E.", "MCA", "BCA",
    "BSc Computer Science", "MSc Computer Science",
    "BSc IT", "MSc IT", "B.Tech ECE", "B.Tech CSE",
    "B.Tech IT", "B.Tech EEE", "MBA Tech", "MBA IT",
    "MS Computer Science", "PhD Computer Science",
    "BSc Electronics", "MSc Electronics", "Diploma in Computer Science",
    "BCA", "MCA", "B.Com (Computer Applications)"
]

# Define Indian tech companies (large companies, startups, and MNCs with Indian offices)
TECH_COMPANIES = [
    # Major Indian IT Companies
    "TCS", "Infosys", "Wipro", "HCL Technologies", "Tech Mahindra",
    "LTI", "Mindtree", "Mphasis", "L&T Technology Services", "Cognizant India",
   
    # Indian Product Companies & Startups
    "Flipkart", "Swiggy", "Zomato", "Paytm", "BYJU's", "Ola", "OYO",
    "PhonePe", "Razorpay", "Freshworks", "Zoho", "Zerodha", "Cred", "Meesho",
    "Urban Company", "PolicyBazaar", "Nykaa", "Delhivery", "BigBasket", "Unacademy",
    "Vedantu", "ShareChat", "Dream11", "InMobi", "CarDekho", "MakeMyTrip",
    # Additional Indian startups for more diversity
    "CureFit", "Dunzo", "Grofers", "Lenskart", "Udaan", "UpGrad", "BookMyShow",
    "Rivigo", "Pine Labs", "BharatPe", "CARS24", "FirstCry", "Pepperfry", "Ecom Express",
   
    # MNCs with significant Indian presence
    "Amazon India", "Google India", "Microsoft India", "IBM India", "Accenture India",
    "Oracle India", "SAP India", "Dell India", "HP India", "Intel India", "Cisco India",
    "Adobe India", "Samsung India", "Capgemini India", "Deloitte India", "KPMG India",
    "PWC India", "EY India", "Morgan Stanley India", "Goldman Sachs India", "J.P. Morgan India",
    "Barclays India", "HSBC India", "Uber India", "LinkedIn India", "NetApp India",
    "Walmart Global Tech India", "PayPal India", "Intuit India", "Informatica India",
    "Atlassian India", "Mastercard India", "American Express India", "VMware India"
]

# Define top Indian educational institutions
INDIAN_UNIVERSITIES = [
    # IITs
    "Indian Institute of Technology, Delhi", "Indian Institute of Technology, Bombay",
    "Indian Institute of Technology, Madras", "Indian Institute of Technology, Kanpur",
    "Indian Institute of Technology, Kharagpur", "Indian Institute of Technology, Roorkee",
    "Indian Institute of Technology, Guwahati", "Indian Institute of Technology, Hyderabad",
    "Indian Institute of Technology, Gandhinagar", "Indian Institute of Technology, Bhubaneswar",
    "Indian Institute of Technology, Indore", "Indian Institute of Technology, Mandi",
    "Indian Institute of Technology, Patna", "Indian Institute of Technology, Ropar",
    "Indian Institute of Technology, Jodhpur", "Indian Institute of Technology, Tirupati",
    "Indian Institute of Technology, Dhanbad",
   
    # NITs
    "National Institute of Technology, Trichy", "National Institute of Technology, Warangal",
    "National Institute of Technology, Surathkal", "National Institute of Technology, Calicut",
    "National Institute of Technology, Rourkela", "National Institute of Technology, Durgapur",
    "National Institute of Technology, Silchar", "National Institute of Technology, Hamirpur",
    "National Institute of Technology, Jaipur", "National Institute of Technology, Kurukshetra",
    "National Institute of Technology, Patna", "National Institute of Technology, Srinagar",
   
    # IIITs
    "International Institute of Information Technology, Hyderabad",
    "International Institute of Information Technology, Bangalore",
    "Indraprastha Institute of Information Technology, Delhi",
    "Indian Institute of Information Technology, Allahabad",
    "Indian Institute of Information Technology, Gwalior",
    "Indian Institute of Information Technology, Sri City",
   
    # Northeastern Universities
    "North-Eastern Hill University, Shillong",
    "Indian Institute of Technology, Guwahati",
    "Tezpur University, Assam",
    "Assam University, Silchar",
    "National Institute of Technology, Silchar",
    "Gauhati University, Guwahati",
    "Manipur University, Imphal",
    "Mizoram University, Aizawl",
    "Sikkim Manipal University, Gangtok",
   
    # Other Top Universities
    "Birla Institute of Technology and Science, Pilani", "Delhi Technological University",
    "College of Engineering, Pune", "PES University, Bangalore", "VIT University, Vellore",
    "SRM University, Chennai", "Manipal Institute of Technology", "Jamia Millia Islamia, Delhi",
    "Netaji Subhas University of Technology, Delhi", "Anna University, Chennai",
    "Jadavpur University, Kolkata", "PSG College of Technology, Coimbatore",
    "Amity University", "Thapar University", "Lovely Professional University",
    "Chandigarh University", "University of Delhi", "Mumbai University", "Pune University",
   
    # Private Universities and Colleges
    "RV College of Engineering, Bangalore", "BMS College of Engineering, Bangalore",
    "MS Ramaiah Institute of Technology", "SSN College of Engineering, Chennai",
    "Vellore Institute of Technology", "Manipal Institute of Technology", "Amrita School of Engineering",
    "Symbiosis Institute of Technology", "Jaypee Institute of Information Technology",
    "BIT Mesra", "Kalinga Institute of Industrial Technology", "IIMT Engineering College"
]

# Enhanced list of Indian cities with more Northeastern representation and emerging tech hubs
INDIAN_CITIES = [
    # Major Tech Hubs
    "Bangalore, Karnataka", "Hyderabad, Telangana", "Pune, Maharashtra", "Mumbai, Maharashtra",
    "Delhi NCR", "Gurgaon, Haryana", "Noida, Uttar Pradesh", "Chennai, Tamil Nadu",
    
    # Other Major Cities
    "Kolkata, West Bengal", "Ahmedabad, Gujarat", "Coimbatore, Tamil Nadu", "Indore, Madhya Pradesh",
    "Thiruvananthapuram, Kerala", "Kochi, Kerala", "Chandigarh", "Jaipur, Rajasthan",
    "Bhubaneswar, Odisha", "Visakhapatnam, Andhra Pradesh", "Nagpur, Maharashtra",
    "Lucknow, Uttar Pradesh", "Gandhinagar, Gujarat", "Mysore, Karnataka",
    
    # Northeastern Cities (Added more representation)
    "Guwahati, Assam", "Shillong, Meghalaya", "Imphal, Manipur", "Aizawl, Mizoram",
    "Agartala, Tripura", "Itanagar, Arunachal Pradesh", "Gangtok, Sikkim", 
    "Dimapur, Nagaland", "Silchar, Assam", "Jorhat, Assam",
    
    # Emerging Tech Hubs
    "Bhopal, Madhya Pradesh", "Surat, Gujarat", "Dehradun, Uttarakhand", 
    "Vadodara, Gujarat", "Raipur, Chhattisgarh", "Ranchi, Jharkhand",
    "Mangalore, Karnataka", "Vijayawada, Andhra Pradesh", "Nashik, Maharashtra",
    "Patna, Bihar", "Trivandrum, Kerala", "Goa", "Pondicherry", "Shimla, Himachal Pradesh",
    "Aurangabad, Maharashtra", "Udaipur, Rajasthan"
]

# Function to normalize skill names for consistency
def normalize_skill_name(skill):
    """Normalize skill names to ensure consistency"""
    
    # Map of common variations to standardized names
    skill_mapping = {
        "Reactjs": "React",
        "React.js": "React",
        "ReactJS": "React",
        "AngularJS": "Angular",
        "Angular.js": "Angular",
        "Angular 2+": "Angular",
        "Vue.js": "Vue",
        "Vuejs": "Vue",
        "Node": "Node.js",
        "Nodejs": "Node.js",
        "JavaScript ES6": "JavaScript",
        "ES6": "JavaScript",
        "Typescript": "TypeScript",
        "Java Script": "JavaScript",
        "Type Script": "TypeScript",
        "Next.js": "NextJS",
        "Tailwind": "Tailwind CSS",
        "Material Design": "Material UI",
        "Express": "Express.js",
        "SQL Server": "Microsoft SQL Server",
        "MS SQL": "Microsoft SQL Server",
        "MSSQL": "Microsoft SQL Server",
        "Postgres": "PostgreSQL",
        "Mongo": "MongoDB",
        "Mongo DB": "MongoDB",
        "DevOps": "DevOps Engineering",
        "GitHub Actions": "GitHub CI/CD",
        "CI/CD Pipeline": "CI/CD",
        "Continuous Integration": "CI/CD",
        "Continuous Deployment": "CI/CD",
        "Amazon Web Services": "AWS",
        "Microsoft Azure": "Azure",
        "Google Cloud Platform": "GCP",
        "Terraform": "Terraform IaC",
        "Ansible": "Ansible IaC",
        "Kubernetes": "K8s",
        "K8": "K8s",
        "Hadoop": "Apache Hadoop",
        "Scikit": "Scikit-learn",
        "Scikit Learn": "Scikit-learn",
        "Tensorflow": "TensorFlow",
        "Pytorch": "PyTorch",
        "Power BI": "PowerBI",
        "Artificial Intelligence": "AI",
        "Machine Learning": "ML"
    }
    
    # Return the normalized skill name or the original if no mapping exists
    return skill_mapping.get(skill, skill)

# Define job titles by category with Indian context
JOB_TITLES = {
    "Software Development": [
        "Software Engineer", "Senior Software Engineer", "Software Developer", "Technical Lead",
        "Lead Software Engineer", "Module Lead", "Principal Engineer", "Software Architect",
        "Technology Specialist", "Technical Architect", "Software Development Engineer"
    ],
    "Data Science": [
        "Data Scientist", "Senior Data Scientist", "Analytics Professional", "Data Science Engineer",
        "Analytics Manager", "Statistical Analyst", "Decision Scientist", "Applied Scientist",
        "Machine Learning Scientist", "Data Science Team Lead", "AI Consultant"
    ],
    "Machine Learning Engineering": [
        "Machine Learning Engineer", "ML Engineer", "AI Engineer", "ML Research Engineer",
        "Deep Learning Engineer", "ML Platform Engineer", "ML Ops Engineer", "Computer Vision Engineer",
        "NLP Engineer", "ML Solutions Architect", "Senior ML Engineer"
    ],
    "DevOps Engineering": [
        "DevOps Engineer", "Site Reliability Engineer", "Platform Engineer", "Infrastructure Engineer",
        "DevOps Architect", "CI/CD Engineer", "DevSecOps Engineer", "Cloud Operations Engineer",
        "System Administrator", "Release Engineer", "Configuration Manager"
    ],
    "Cloud Architecture": [
        "Cloud Architect", "Cloud Engineer", "AWS Architect", "Azure Specialist",
        "Cloud Infrastructure Engineer", "Multi-cloud Specialist", "Cloud Security Architect",
        "Cloud Migration Engineer", "Cloud Application Architect", "Cloud Solutions Architect"
    ],
    "Frontend Development": [
        "Frontend Developer", "Frontend Engineer", "UI Developer", "JavaScript Developer",
        "React Developer", "Angular Developer", "Senior Frontend Developer", "UI Engineer",
        "Web Developer", "Frontend Architect", "UI/UX Developer"
    ],
    "Backend Development": [
        "Backend Developer", "Backend Engineer", "API Developer", "Java Developer",
        "Python Developer", "Node.js Developer", ".NET Developer", "PHP Developer",
        "Ruby Developer", "Backend Architect", "Server-side Developer"
    ],
    "Full Stack Development": [
        "Full Stack Developer", "Full Stack Engineer", "MEAN Stack Developer", "MERN Stack Developer",
        "Web Application Developer", "Full Stack Architect", "Software Developer",
        "Web Developer", "Full Stack Team Lead", "Senior Full Stack Developer"
    ],
    "Mobile App Development": [
        "Mobile Developer", "Android Developer", "iOS Developer", "React Native Developer",
        "Flutter Developer", "Mobile App Engineer", "Cross-platform Mobile Developer",
        "Mobile Application Architect", "Senior Mobile Developer", "Mobile Team Lead"
    ],
    "UI/UX Design": [
        "UI/UX Designer", "Product Designer", "User Experience Designer", "User Interface Designer",
        "Interaction Designer", "UX Researcher", "Visual Designer", "Experience Designer",
        "UX Lead", "Creative Designer", "Senior UX Designer"
    ],
    "QA & Testing": [
        "QA Engineer", "Test Engineer", "Quality Assurance Analyst", "Test Automation Engineer",
        "QA Analyst", "Software Tester", "QA Lead", "SDET", "Test Manager",
        "Performance Test Engineer", "Quality Engineer"
    ],
    "Cybersecurity": [
        "Security Engineer", "Cybersecurity Analyst", "Information Security Specialist",
        "Security Consultant", "Penetration Tester", "Security Architect", "SOC Analyst",
        "Cyber Defense Analyst", "Vulnerability Assessment Engineer", "Network Security Engineer"
    ],
    "Database Administration": [
        "Database Administrator", "Database Engineer", "SQL Developer", "Data Engineer",
        "Database Architect", "NoSQL Specialist", "Database Reliability Engineer",
        "Database Developer", "Database Support Engineer", "Senior DBA"
    ],
    "Product Management": [
        "Product Manager", "Technical Product Manager", "Product Owner", "Senior Product Manager",
        "Associate Product Manager", "Director of Product", "Product Lead",
        "Program Manager", "Product Analyst", "Product Consultant"
    ],
    "Business Intelligence": [
        "Business Intelligence Analyst", "BI Developer", "Data Analyst", "BI Consultant",
        "BI Architect", "Analytics Engineer", "Reporting Specialist", "Data Warehouse Developer",
        "ETL Developer", "MIS Analyst", "Dashboard Developer"
    ],
    "ERP/SAP Consultant": [
        "SAP Consultant", "ERP Consultant", "SAP ABAP Developer", "SAP Functional Consultant",
        "SAP Technical Consultant", "Oracle ERP Consultant", "ERP Implementation Specialist",
        "SAP Project Manager", "SAP Solution Architect", "ERP Business Analyst"
    ],
    "Technical Support": [
        "Technical Support Engineer", "Support Specialist", "IT Support Engineer", "Desktop Support Engineer",
        "Help Desk Analyst", "Customer Support Engineer", "IT Helpdesk Engineer", "Systems Support Specialist",
        "Technical Support Specialist", "Service Desk Analyst"
    ],
    "Systems Administration": [
        "Systems Administrator", "Windows Administrator", "Linux Administrator", "Unix Administrator",
        "System Engineer", "IT Infrastructure Manager", "Server Administrator", "Network Administrator",
        "IT Operations Engineer", "Systems Engineer"
    ],
    "Network Engineering": [
        "Network Engineer", "Network Administrator", "Network Architect", "Network Support Engineer",
        "Cisco Network Engineer", "NOC Engineer", "WAN Engineer", "LAN Engineer",
        "Network Security Engineer", "Senior Network Engineer"
    ],
    "IT Project Management": [
        "IT Project Manager", "Technical Project Manager", "Project Lead", "Delivery Manager",
        "Scrum Master", "Agile Coach", "Project Management Officer", "Delivery Lead",
        "IT Program Manager", "Implementation Manager"
    ],
    "Data Engineering": [
        "Data Engineer", "Big Data Engineer", "ETL Developer", "Data Pipeline Engineer",
        "Data Architect", "Data Infrastructure Engineer", "Data Platform Engineer",
        "Hadoop Developer", "Spark Engineer", "Senior Data Engineer"
    ],
    "IoT Development": [
        "IoT Developer", "IoT Solutions Architect", "IoT Engineer", "Embedded IoT Developer",
        "IoT Systems Engineer", "IoT Product Developer", "IoT Application Developer",
        "IoT Cloud Engineer", "IoT Integration Specialist", "Senior IoT Developer"
    ],
    "Embedded Systems": [
        "Embedded Systems Engineer", "Firmware Engineer", "Embedded Software Developer", 
        "Embedded Hardware Engineer", "RTOS Developer", "Embedded Systems Architect",
        "Microcontroller Programmer", "FPGA Engineer", "SoC Designer", "Embedded Tech Lead"
    ]
}

# Career objectives by category with Indian context
CAREER_OBJECTIVES = {
    "Software Development": [
        "Dedicated software engineer with {experience} years of experience seeking to leverage expertise in {skills} to develop innovative software solutions.",
        "Results-oriented software developer with {experience} years in the IT industry looking to contribute technical skills in {skills} to a growing organization.",
        "Software professional with {experience}+ years of experience in product development and expertise in {skills} seeking challenging development opportunities.",
        "Experienced software engineer aiming to utilize my proficiency in {skills} to solve complex business problems through efficient coding and design."
    ],
    "Data Science": [
        "Analytical data scientist with {experience} years of experience using {skills} to extract actionable insights and drive business decisions.",
        "Passionate data professional with {experience}+ years of hands-on experience in {skills}, seeking to apply analytical expertise to business challenges.",
        "Results-driven data scientist with expertise in {skills}, looking to leverage statistical methods and machine learning to create value.",
        "Experienced analyst with strong skills in {skills} aiming to help organizations make data-driven decisions through advanced analytics."
    ],
    "Machine Learning Engineering": [
        "ML engineer with {experience} years of experience in designing and implementing ML systems using {skills}, seeking opportunities to develop AI solutions.",
        "AI specialist proficient in {skills} with {experience}+ years of experience, looking to build and deploy production-grade machine learning models.",
        "Machine learning professional with {experience} years of expertise in {skills}, aiming to join a forward-thinking team building innovative ML applications.",
        "Experienced ML engineer skilled in {skills}, passionate about translating research into production-ready machine learning solutions."
    ],
    "Full Stack Development": [
        "Full stack developer with {experience} years of experience developing end-to-end web applications using {skills} seeking new challenges.",
        "Versatile full-stack engineer with expertise in {skills} and {experience}+ years of experience, looking to build comprehensive web solutions.",
        "Skilled full stack developer with {experience} years of experience in MERN/MEAN stack and proficiency in {skills}, seeking challenging projects.",
        "Web development professional with {experience}+ years of experience in frontend and backend technologies including {skills}."
    ]
}

# Function to fill in more career objectives for other categories
def complete_career_objectives():
        # Continue the career objectives dictionary function
    template_objectives = [
        "Experienced {category} professional with {experience} years in the IT industry, seeking to leverage expertise in {skills} to drive innovation.",
        "Results-driven {category} specialist with {experience}+ years of experience, looking to apply knowledge of {skills} to solve complex challenges.",
        "Dedicated {category} expert with {experience} years and strong skills in {skills}, aiming to join a dynamic organization to deliver high-quality solutions.",
        "Detail-oriented {category} professional with {experience}+ years of hands-on experience in {skills}, seeking new challenges to grow expertise."
    ]
   
    for category in TECH_CATEGORIES:
        if category not in CAREER_OBJECTIVES:
            CAREER_OBJECTIVES[category] = [obj.replace("{category}", category) for obj in template_objectives]

# Complete the career objectives dictionary
complete_career_objectives()

# Function to generate a realistic career timeline with better experience distribution
def generate_career_timeline(category, experience_years, start_date=None):
    """Generate a realistic work history based on total years of experience"""
    if not start_date:
        # Start date is graduation date, roughly experience_years + few years ago from now
        total_years_ago = experience_years + random.randint(0, 3)  # Add some variability
        start_date = datetime.now() - timedelta(days=365 * total_years_ago)
       
    current_date = datetime.now()
    career = []
    remaining_years = experience_years
   
    # For very junior roles
    if experience_years < 1:
        # May have internships or be a fresher
        if random.random() > 0.5:  # 50% chance of having internship (increased from 30%)
            internship_duration = random.randint(3, 8) / 12  # 3-8 months (improved from 2-6)
            end_date = current_date
            start_date = end_date - timedelta(days=int(internship_duration * 365))
           
            company = random.choice(TECH_COMPANIES)
            job = {
                "company": company,
                "title": f"{category} Intern",
                "start_date": start_date.strftime("%Y-%m"),
                "end_date": end_date.strftime("%Y-%m") if end_date != current_date else "Present",
                "duration": f"{internship_duration:.1f} years",
                "is_internship": True
            }
            career.append(job)
        return career
   
    # Generate jobs to fill the experience years
    while remaining_years > 0:
        # Job duration more realistic for Indian tech market
        if remaining_years > 10:
            # Senior roles tend to be longer
            job_duration = random.randint(24, 60) / 12  # 2-5 years
        elif remaining_years > 5:
            # Mid-level roles
            job_duration = random.randint(18, 42) / 12  # 1.5-3.5 years
        else:
            # Junior roles have shorter tenures
            job_duration = min(remaining_years, random.randint(10, 30) / 12)  # 10 months to 2.5 years
           
        job_duration = max(job_duration, 0.5)  # Minimum 6 months
       
        end_date = current_date
        start_date = end_date - timedelta(days=int(job_duration * 365))
       
        # Select job title based on experience level
        experience_level = ""
        if remaining_years > 12:
            experience_level = random.choice(["Senior ", "Lead ", "Principal ", "Director of ", "Head of "])
        elif remaining_years > 8:
            experience_level = random.choice(["Senior ", "Lead ", "", ""])
        elif remaining_years > 4:
            experience_level = random.choice(["Senior ", "", "", ""])
       
        # Select job title and company
        job_titles = JOB_TITLES.get(category, ["Professional"])
        job_title = experience_level + random.choice(job_titles)
        company = random.choice(TECH_COMPANIES)
       
        # Create job entry
        job = {
            "company": company,
            "title": job_title,
            "start_date": start_date.strftime("%Y-%m"),
            "end_date": end_date.strftime("%Y-%m") if end_date != current_date else "Present",
            "duration": f"{job_duration:.1f} years",
            "is_internship": False
        }
       
        career.append(job)
        current_date = start_date
        remaining_years -= job_duration
   
    # Sort by date (newest first)
    career.sort(key=lambda x: x["start_date"], reverse=True)
    return career

# Enhanced function to generate education background
def generate_education(category, experience_years):
    """Generate educational background appropriate for the role with better distribution"""
   
    # Determine highest degree based on experience, category and probability
    # Adjust probabilities to create better distribution
    if experience_years > 12:
        phd_prob = 0.15
        masters_prob = 0.45
        bachelors_prob = 0.40
    elif experience_years > 7:
        phd_prob = 0.05
        masters_prob = 0.40
        bachelors_prob = 0.55
    elif experience_years > 3:
        phd_prob = 0.01
        masters_prob = 0.30
        bachelors_prob = 0.69
    else:
        phd_prob = 0.0
        masters_prob = 0.20
        bachelors_prob = 0.80
        
    # Adjust for certain categories
    if category in ["Data Science", "Machine Learning Engineering", "Research"]:
        phd_prob *= 2
        masters_prob *= 1.5
        
    # Determine degree level based on probability
    rand = random.random()
    if rand < phd_prob:
        degree_level = "PhD"
    elif rand < phd_prob + masters_prob:
        degree_level = "Master's"
    else:
        degree_level = "Bachelor's"
   
    # Select field of study relevant to category
    if category in ["Data Science", "Machine Learning Engineering", "Business Intelligence", "Data Engineering"]:
        fields = ["Computer Science", "Data Science", "Statistics", "Mathematics", "Analytics", "Information Systems"]
    elif category in ["UI/UX Design"]:
        fields = ["Design", "Human-Computer Interaction", "Digital Media", "Fine Arts", "Psychology", "Visual Communication"]
    elif category in ["Product Management", "IT Project Management"]:
        fields = ["Business Administration", "Engineering Management", "Information Systems", "Project Management", "Computer Applications"]
    elif category in ["IoT Development", "Embedded Systems"]:
        fields = ["Electronics", "Embedded Systems", "IoT", "Computer Engineering", "Electronics and Communication"]
    else:
        fields = ["Computer Science", "Information Technology", "Electronics and Communication", "Electrical Engineering", "Computer Engineering"]
       
    # Actual degree name (Indian context)
    if degree_level == "Bachelor's":
        degree = random.choice(["B.Tech", "B.E.", "B.Sc", "BCA"])
    elif degree_level == "Master's":
        degree = random.choice(["M.Tech", "M.E.", "M.Sc", "MCA"])
    else:  # PhD
        degree = "PhD"
       
    field = random.choice(fields)
    
    # For better university distribution
    if random.random() < 0.3:  # 30% chance of premier institute
        tier = "premier"
        if "IIT" in INDIAN_UNIVERSITIES[0]:  # This is checking if IITs are in the first few entries
            university_pool = [u for u in INDIAN_UNIVERSITIES if "IIT" in u or "NIT" in u or "IIIT" in u or "BITS" in u][:10]
        else:
            university_pool = INDIAN_UNIVERSITIES[:15]  # Top 15 universities
    else:
        tier = "standard"
        university_pool = INDIAN_UNIVERSITIES[15:] if len(INDIAN_UNIVERSITIES) > 15 else INDIAN_UNIVERSITIES
    
    university = random.choice(university_pool)
   
    # Calculate graduation year based on experience
    current_year = datetime.now().year
    years_since_highest_degree = experience_years + random.randint(0, 2)
    graduation_year = current_year - years_since_highest_degree
   
    # Generate education history
    education = [{
        "degree": f"{degree} in {field}",
        "university": university,
        "year": graduation_year,
        "location": university.split(",")[-1].strip() if "," in university else "India",
        "tier": tier
    }]
   
    # Add undergraduate degree if person has a graduate degree
    if degree_level in ["Master's", "PhD"]:
        undergrad_field = field
        if random.random() > 0.7:
            # Sometimes undergraduate degree is in a different field
            undergrad_field = random.choice(fields)
       
        undergrad_university = university
        if random.random() > 0.6:
            # Sometimes people attend different universities
            undergrad_university = random.choice(INDIAN_UNIVERSITIES)
           
        grad_years = 2 if degree_level == "Master's" else 5
        undergrad_year = graduation_year - grad_years
        undergrad_degree = random.choice(["B.Tech", "B.E.", "B.Sc", "BCA"])
       
        education.append({
            "degree": f"{undergrad_degree} in {undergrad_field}",
            "university": undergrad_university,
            "year": undergrad_year,
            "location": undergrad_university.split(",")[-1].strip() if "," in undergrad_university else "India",
            "tier": "standard"  # Default tier for older degrees
        })
   
    # Add 12th and 10th standard education (common in Indian resumes)
    if random.random() > 0.3:  # 70% include school education
        school_board = random.choice(["CBSE", "ICSE", "State Board"])
        twelfth_year = graduation_year - 4 if degree_level == "Bachelor's" else education[-1]["year"] - 4
        tenth_year = twelfth_year - 2
       
        school_name = f"{random.choice(['DAV', 'DPS', 'Kendriya Vidyalaya', 'St. Xavier\'s', 'Modern School', 'Delhi Public School', 'Army Public School'])} {random.choice(['Public School', 'Higher Secondary School', 'Senior Secondary School'])}"
       
        education.append({
            "degree": f"Class XII ({school_board})",
            "university": school_name,
            "year": twelfth_year,
            "location": random.choice(INDIAN_CITIES).split(",")[0],
            "tier": "school"
        })
       
        education.append({
            "degree": f"Class X ({school_board})",
            "university": school_name,
            "year": tenth_year,
            "location": random.choice(INDIAN_CITIES).split(",")[0],
            "tier": "school"
        })
   
    # Sort by year (most recent first)
    education.sort(key=lambda x: x["year"], reverse=True)
    return education

# Enhanced function to generate projects
def generate_projects(category, skills, experience_years):
    """Generate realistic projects based on the category and skills with Indian context"""
   
    # Number of projects based on experience - adjusted for better distribution
    if experience_years < 1:
        num_projects = random.randint(1, 3)  # Entry level needs more projects to show
    elif experience_years < 3:
        num_projects = random.randint(2, 4)
    elif experience_years < 7:
        num_projects = random.randint(2, 5)
    else:
        num_projects = random.randint(3, 6)
   
    # Project templates relevant to Indian tech industry
    project_templates = [
        {"name": "E-commerce Platform", "tech": ["JavaScript", "React", "Node.js", "MongoDB"],
         "description": "Built a full-stack e-commerce platform with user authentication, product catalog, shopping cart, and payment integration with Indian payment gateways."},
        {"name": "Inventory Management System", "tech": ["Java", "Spring Boot", "MySQL", "React"],
         "description": "Developed a web-based inventory management system for small and medium businesses with reporting, analytics, and GST compliance features."},
        {"name": "Mobile Banking App", "tech": ["React Native", "Firebase", "Redux", "Node.js"],
         "description": "Created a secure mobile banking application supporting UPI, IMPS, and NEFT transactions with dual-factor authentication and biometric security."},
        {"name": "Recommendation Engine", "tech": ["Python", "TensorFlow", "scikit-learn", "Flask"],
         "description": "Built a machine learning system that provides personalized product recommendations based on user browsing patterns and purchase history."},
        {"name": "Cloud Migration Project", "tech": ["AWS", "Docker", "Terraform", "Jenkins"],
         "description": "Led the migration of on-premises applications to AWS cloud infrastructure, implementing CI/CD pipelines and infrastructure as code."},
        {"name": "Healthcare Management System", "tech": ["Java", "Spring", "PostgreSQL", "Angular"],
         "description": "Developed a comprehensive healthcare management solution for hospitals, including patient records, appointment scheduling, and billing modules."},
        {"name": "Real Estate Portal", "tech": ["PHP", "Laravel", "MySQL", "jQuery", "Bootstrap"],
         "description": "Created a property listing and search platform with advanced filtering, map integration, and virtual tour capabilities for the Indian market."},
        {"name": "School Management System", "tech": ["Python", "Django", "PostgreSQL", "React"],
         "description": "Built a complete school management system with student information, attendance tracking, grades, and parent communication modules."},
        {"name": "Food Delivery Application", "tech": ["React Native", "Node.js", "MongoDB", "Express"],
         "description": "Developed a mobile app for food ordering and delivery with real-time tracking, online payment, and restaurant management features."},
        {"name": "Employee Management System", "tech": ["Java", "Hibernate", "MySQL", "JSP", "Servlets"],
         "description": "Created an HR management solution with attendance tracking, leave management, performance evaluations, and payroll processing."},
        {"name": "Supply Chain Management Solution", "tech": ["Java", "Spring Boot", "React", "PostgreSQL"],
         "description": "Built an end-to-end supply chain management solution with inventory tracking, order management, and logistics optimization for Indian manufacturers."},
        {"name": "AI-powered Customer Support", "tech": ["Python", "TensorFlow", "FastAPI", "React"],
         "description": "Created a chatbot solution for customer support with NLP capabilities, multi-lingual support for Indian languages, and integration with ticketing systems."},
        {"name": "Telemedicine Platform", "tech": ["Angular", "Node.js", "MongoDB", "WebRTC"],
         "description": "Built a secure telemedicine platform allowing patients to consult doctors remotely with video conferencing, prescription management, and payment integration."}
    ]
   
    # Specialized projects based on tech category
    category_projects = {
        "Software Development": ["Payment Gateway Integration", "Core Banking System", "Custom ERP Solution"],
        "Data Science": ["Customer Segmentation for Retail Chain", "Credit Risk Assessment Model", "Demand Forecasting System", "Churn Prediction Model", "Market Basket Analysis"],
        "Machine Learning Engineering": ["Image Recognition for Medical Diagnostics", "NLP for Indian Language Processing", "Fraud Detection System", "Sentiment Analysis Engine", "ML-based Recommendation System"],
        "DevOps Engineering": ["Microservices Deployment Pipeline", "Container Orchestration Platform", "Infrastructure Monitoring Suite", "CI/CD Automation Framework", "Kubernetes Management Platform"],
        "Cloud Architecture": ["Multi-Cloud Disaster Recovery", "Serverless Applications", "Cloud Cost Optimization", "Hybrid Cloud Solution", "Cloud Security Framework"],
        "Frontend Development": ["Progressive Web App", "Responsive Admin Dashboard", "Cross-Browser UI Framework", "Accessibility-focused Frontend", "Animation Library"],
        "Backend Development": ["High-Performance API Gateway", "Real-time Notification System", "Data Synchronization Service", "Authentication Microservice", "Payment Processing Backend"],
        "Full Stack Development": ["Enterprise Learning Management System", "CRM Software", "Booking and Reservation System", "Portfolio Management Platform", "Social Media Dashboard"],
        "Mobile App Development": ["UPI Payment App", "Fitness Tracking App", "Grocery Delivery Platform", "AR Shopping Experience", "Transport Booking App"],
        "UI/UX Design": ["Mobile Banking Interface", "E-learning Platform Design", "Government Service Portal UX", "Healthcare App Interface", "E-commerce UX Redesign"],
        "QA & Testing": ["Test Automation Framework", "Performance Testing Suite", "Mobile Testing Strategy", "API Testing Framework", "Security Testing Protocol"],
        "Cybersecurity": ["Banking Security System", "Vulnerability Assessment Tool", "Multi-factor Authentication System", "Security Monitoring Dashboard", "Compliance Automation Tool"],
        "Database Administration": ["Database Migration Project", "High-Availability Cluster", "Database Performance Optimization", "Automated Backup System", "Data Archival Solution"],
        "Product Management": ["Product Roadmap for FinTech App", "Feature Prioritization Framework", "User Feedback System", "Product Analytics Dashboard", "Go-to-Market Strategy"],
        "Business Intelligence": ["Sales Analytics Dashboard", "Customer Insights Platform", "KPI Tracking System", "Executive Decision Support System", "Market Analysis Tool"],
        "ERP/SAP Consultant": ["SAP Implementation for Manufacturing", "ERP Customization", "Business Process Optimization", "SAP-CRM Integration", "ERP Training Program"],
        "Technical Support": ["Remote Support Infrastructure", "Ticketing System Implementation", "Knowledge Base Creation", "IT Asset Management System", "Support Analytics Dashboard"],
        "Systems Administration": ["Data Center Migration", "Server Virtualization Project", "Disaster Recovery Plan", "System Monitoring Solution", "Automated Provisioning System"],
        "Network Engineering": ["Secure WAN Implementation", "Network Redesign Project", "SD-WAN Deployment", "Network Monitoring System", "Zero Trust Architecture"],
        "IT Project Management": ["Agile Transformation Initiative", "Core Banking System Implementation", "Enterprise Cloud Migration", "Digital Transformation Roadmap", "IT Governance Framework"],
        "Data Engineering": ["ETL Pipeline Optimization", "Data Lake Implementation", "Real-time Analytics Platform", "Big Data Architecture", "Data Quality Framework"],
        "IoT Development": ["Smart Home Automation", "Industrial IoT Monitoring", "Connected Vehicle Platform", "Smart Agriculture System", "IoT Security Framework"],
        "Embedded Systems": ["Automotive Control Systems", "Medical Device Firmware", "Industrial Automation Controller", "Smart Appliance Firmware", "Embedded Security Module"]
    }
   
    projects = []
   
    # Add category-specific projects
    if category in category_projects:
        specific_projects = category_projects[category]
        for i in range(min(len(specific_projects), num_projects)):
            if i >= len(specific_projects):
                break
                
            project_name = specific_projects[i]
            # Use skills relevant to the project
            relevant_skills = [skill for skill in skills if random.random() > 0.4][:4]
            if not relevant_skills:  # Ensure at least one skill
                relevant_skills = [random.choice(skills)] if skills else ["Java"]
               
            projects.append({
                "name": project_name,
                "tech": relevant_skills,
                "description": f"Implemented a {project_name.lower()} using {', '.join(relevant_skills[:-1])} and {relevant_skills[-1] if relevant_skills else 'various technologies'}."
            })
   
    # Add some generic projects if needed
    remaining_projects = num_projects - len(projects)
    for _ in range(remaining_projects):
        if not project_templates:
            break
            
        template = random.choice(project_templates)
        
        # Avoid duplicate projects
        project_templates.remove(template)
       
        # Customize tech stack based on candidate skills
        tech_stack = []
        for tech in template["tech"]:
            if tech in skills or random.random() > 0.7:
                tech_stack.append(tech)
            elif skills:
                tech_stack.append(random.choice(skills))
       
        if not tech_stack and skills:  # Ensure at least one technology
            tech_stack = random.sample(skills, min(3, len(skills)))
        elif not tech_stack:
            tech_stack = template["tech"][:2]
           
        projects.append({
            "name": template["name"],
            "tech": tech_stack,
            "description": template["description"]
        })
   
    return projects

# Enhanced Indian tech certifications by category
INDIAN_CERTIFICATIONS = {
    "Software Development": [
        "Oracle Certified Java Programmer", 
        "Microsoft Certified: Azure Developer Associate", 
        "AWS Certified Developer – Associate",
        "Certified Spring Professional",
        "Certified Kubernetes Application Developer (CKAD)"
    ],
    "Data Science": [
        "Certified Analytics Professional (CAP)", 
        "Microsoft Certified: Azure Data Scientist Associate", 
        "IBM Data Science Professional Certificate",
        "SAS Certified Data Scientist",
        "Cloudera Certified Data Scientist"
    ],
    "Machine Learning Engineering": [
        "TensorFlow Developer Certificate", 
        "AWS Certified Machine Learning – Specialty", 
        "Google Professional Machine Learning Engineer",
        "Microsoft Certified: Azure AI Engineer Associate",
        "IBM AI Engineering Professional Certificate"
    ],
    "DevOps Engineering": [
        "AWS Certified DevOps Engineer – Professional", 
        "Certified Kubernetes Administrator (CKA)", 
        "Microsoft Certified: DevOps Engineer Expert",
        "Docker Certified Associate",
        "GitLab Certified CI/CD Specialist"
    ],
    "Cloud Architecture": [
        "AWS Certified Solutions Architect – Professional", 
        "Google Professional Cloud Architect", 
        "Microsoft Certified: Azure Solutions Architect Expert",
        "IBM Certified Cloud Solution Architect",
        "Oracle Cloud Infrastructure Architect Professional"
    ],
    "Frontend Development": [
        "Microsoft Certified: JavaScript Developer",
        "React Developer Certification",
        "Angular Certification",
        "Adobe Certified Expert - Adobe Experience Manager Sites Developer",
        "Salesforce Frontend Developer Certification"
    ],
    "Backend Development": [
        "Oracle Certified Professional, Java SE Developer",
        "Microsoft Certified: .NET Developer Associate",
        "Node.js Certification",
        "Django Developer Certification",
        "Spring Framework Certification"
    ],
    "Full Stack Development": [
        "MongoDB Certified Developer Associate",
        "Full Stack Web Developer (FSWD) Certification",
        "IBM Full Stack Cloud Developer Certificate",
        "JavaScript Full Stack Developer Certification",
        "AWS Certified Developer – Associate"
    ],
    "Mobile App Development": [
        "Android Certified Application Developer",
        "Apple Certified iOS Developer",
        "React Native Developer Certification",
        "Flutter Developer Certification",
        "Xamarin Certified Mobile Developer"
    ],
    "UI/UX Design": [
        "Adobe Certified Expert in XD",
        "Certified User Experience Professional",
        "Interaction Design Certification",
        "Nielsen Norman Group UX Certification",
        "Certified Usability Analyst"
    ],
    "QA & Testing": [
        "ISTQB Certified Tester Foundation Level",
        "Selenium WebDriver with Java Certification",
        "Certified Test Engineer",
        "HP LoadRunner Certification",
        "Appium Mobile Testing Certification"
    ],
    "Cybersecurity": [
        "Certified Information Systems Security Professional (CISSP)",
        "Certified Ethical Hacker (CEH)",
        "CompTIA Security+",
        "Certified Information Security Manager (CISM)",
        "GIAC Security Essentials Certification"
    ],
    "Database Administration": [
        "Oracle Certified Professional, MySQL Database Administrator",
        "Microsoft Certified: Azure Database Administrator Associate",
        "MongoDB Certified DBA Associate",
        "PostgreSQL Administration Certification",
        "IBM Certified Database Administrator"
    ],
    "Product Management": [
        "Certified Scrum Product Owner (CSPO)",
        "Product Management Certification (PMC)",
        "Professional Scrum Product Owner",
        "Pragmatic Marketing Certified",
        "Certified Product Manager"
    ],
    "Business Intelligence": [
        "Microsoft Certified: Data Analyst Associate",
        "Tableau Desktop Certified Professional",
        "Power BI Certified Data Analyst",
        "QlikView Business Analyst Certification",
        "SAS Certified BI Content Developer"
    ],
    "ERP/SAP Consultant": [
        "SAP Certified Application Associate",
        "Oracle ERP Cloud Certification",
        "SAP S/4HANA Certification",
        "Microsoft Dynamics 365 Certification",
        "SAP ABAP Certification"
    ],
    "Technical Support": [
        "CompTIA A+",
        "ITIL Foundation",
        "Microsoft Certified: Modern Desktop Administrator Associate",
        "Apple Certified Support Professional",
        "Cisco Certified Technician"
    ],
    "Systems Administration": [
        "Red Hat Certified System Administrator (RHCSA)",
        "Microsoft Certified: Windows Server Administrator",
        "CompTIA Server+",
        "Linux Professional Institute Certification",
        "VMware Certified Professional – Data Center Virtualization"
    ],
    "Network Engineering": [
        "Cisco Certified Network Associate (CCNA)",
        "Juniper Networks Certified Internet Associate",
        "CompTIA Network+",
        "Certified Wireless Network Professional",
        "Palo Alto Networks Certified Network Security Engineer"
    ],
    "IT Project Management": [
        "Project Management Professional (PMP)",
        "PRINCE2 Foundation and Practitioner",
        "Certified ScrumMaster (CSM)",
        "PMI Agile Certified Practitioner (PMI-ACP)",
        "ITIL 4 Foundation"
    ],
    "Data Engineering": [
        "Cloudera Certified Data Engineer",
        "Google Cloud Professional Data Engineer",
        "AWS Certified Data Analytics - Specialty",
        "Azure Data Engineer Associate",
        "Databricks Certified Developer for Apache Spark"
    ],
    "IoT Development": [
        "Microsoft Certified: Azure IoT Developer Specialty",
        "AWS Certified IoT Specialty",
        "Certified IoT Security Practitioner",
        "Industrial IoT Professional Certification",
        "IoT Architect Certification"
    ],
    "Embedded Systems": [
        "Certified Embedded Systems Professional",
        "ARM Accredited MCU Engineer",
        "Certified FPGA Designer",
        "Embedded C Certification",
        "RTOS Professional Certification"
    ]
}

# Function to generate certifications with better distribution
def generate_certifications(category, experience_years):
    """Generate relevant certifications based on job category and experience"""
   
    # Number of certifications based on experience - adjusted for better distribution
    if experience_years < 2:
        max_certs = random.randint(0, 2)  # Even junior people could have certifications
    elif experience_years < 5:
        max_certs = random.randint(1, 2)
    elif experience_years < 10:
        max_certs = random.randint(1, 3)
    else:
        max_certs = random.randint(2, 4)
   
    # Get certifications for this category
    category_certs = INDIAN_CERTIFICATIONS.get(category, [])
   
    # If no certifications for category or random chance, add general certifications
    if not category_certs or random.random() > 0.7:
        general_certs = [
            "ITIL Foundation",
            "Certified Scrum Master (CSM)",
            "Project Management Professional (PMP)",
            "AWS Certified Cloud Practitioner",
            "Microsoft Certified: Azure Fundamentals",
            "Google Cloud Certified Associate Engineer",
            "CompTIA Security+",
            "Certified Agile Professional",
            "IBM Cloud Essentials"
        ]
        if not category_certs:
            category_certs = general_certs
        else:
            category_certs.extend(general_certs)
   
    # Select random certifications
    certifications = []
    if max_certs > 0:
        selected_certs = random.sample(category_certs, min(max_certs, len(category_certs)))
        current_year = datetime.now().year
       
        for cert in selected_certs:
            # More realistic certification timing
            if experience_years < 2:
                year = current_year - random.randint(0, 1)
            else:
                # More experienced people may have older certifications
                year = current_year - random.randint(0, min(int(experience_years), 5))
                
            certifications.append({
                "name": cert,
                "issuer": get_cert_issuer(cert),
                "year": year
            })
   
    return certifications

def get_cert_issuer(cert_name):
    """Determine the issuer based on certification name"""
    if "AWS" in cert_name:
        return "Amazon Web Services"
    elif "Azure" in cert_name or "Microsoft" in cert_name:
        return "Microsoft"
    elif "Google" in cert_name:
        return "Google Cloud"
    elif "Oracle" in cert_name:
        return "Oracle Corporation"
    elif "Certified Scrum" in cert_name or "Scrum" in cert_name:
        return "Scrum Alliance"
    elif "ITIL" in cert_name:
        return "Axelos"
    elif "Project Management" in cert_name or "PMP" in cert_name:
        return "Project Management Institute"
    elif "Cisco" in cert_name or "CCNA" in cert_name or "CCNP" in cert_name:
        return "Cisco Systems"
    elif "CompTIA" in cert_name:
        return "CompTIA"
    elif "SAP" in cert_name:
        return "SAP SE"
    elif "ISTQB" in cert_name:
        return "International Software Testing Qualifications Board"
    elif "Ethical Hacker" in cert_name or "CEH" in cert_name:
        return "EC-Council"
    elif "CISSP" in cert_name:
        return "ISC²"
    elif "Java" in cert_name:
        return "Oracle Corporation"
    elif "Docker" in cert_name:
        return "Docker, Inc."
    elif "Kubernetes" in cert_name:
        return "Cloud Native Computing Foundation"
    elif "TensorFlow" in cert_name:
        return "Google"
    elif "Red Hat" in cert_name:
        return "Red Hat, Inc."
    elif "IBM" in cert_name:
        return "IBM"
    elif "Tableau" in cert_name:
        return "Tableau Software"
    elif "Power BI" in cert_name or "PowerBI" in cert_name:
        return "Microsoft"
    elif "React" in cert_name:
        return "Facebook/Meta"
    else:
        return "Industry Standard Authority"

# Enhanced function to generate key achievements
def generate_key_achievements(category, experience_years):
    """Generate realistic achievements based on job category and experience"""
   
    # Base achievements that could fit most tech roles
    base_achievements = [
        "Led a team of {team_size} developers to deliver project {ahead_behind} schedule",
        "Improved system performance by {percentage}% through optimization of {component}",
        "Successfully migrated {data_system} with zero downtime",
        "Reduced {process} time by {percentage}% by implementing {solution}",
                "Automated {process} resulting in {time_saved} hours saved per {period}",
        "Received {award_name} for exceptional contribution to {project_aspect}",
        "Implemented {technology} that reduced costs by ₹{amount} annually",
        "Developed {feature} that increased {metric} by {percentage}%",
        "Mentored {number} junior team members in {skill_area}",
        "Resolved critical production issues with average resolution time of {time_period}"
    ]
   
    # Category-specific achievements
    category_achievements = {
        "Software Development": [
            "Refactored legacy codebase reducing technical debt by {percentage}%",
            "Architected and implemented microservices architecture resulting in {benefit}",
            "Reduced build time from {time_before} to {time_after} through CI/CD pipeline improvements"
        ],
        "Data Science": [
            "Built predictive model with {accuracy}% accuracy, increasing business revenue by {percentage}%",
            "Developed clustering algorithm that improved customer targeting by {percentage}%",
            "Created analytics dashboard resulting in data-driven decisions that saved ₹{amount} annually"
        ],
        "Machine Learning Engineering": [
            "Deployed ML model that improved prediction accuracy from {accuracy_before}% to {accuracy_after}%",
            "Optimized ML pipeline reducing inference time by {percentage}%",
            "Implemented {algorithm} that outperformed baseline by {percentage}% on key metrics"
        ],
        "DevOps Engineering": [
            "Reduced deployment time from {time_before} to {time_after} through automation",
            "Improved infrastructure reliability achieving {percentage}% uptime",
            "Implemented container orchestration reducing resource costs by {percentage}%"
        ],
        "Data Engineering": [
            "Optimized ETL pipeline reducing processing time by {percentage}%",
            "Built real-time data streaming solution processing {volume} events per second",
            "Designed data lake architecture that reduced storage costs by {percentage}%"
        ],
        "Cloud Architecture": [
            "Architected cloud migration strategy saving ₹{amount} in infrastructure costs",
            "Implemented serverless architecture reducing operational overhead by {percentage}%",
            "Designed multi-region failover system with {percentage}% availability"
        ],
        "Mobile App Development": [
            "Reduced app size by {percentage}% while maintaining feature parity",
            "Improved app store rating from {rating_before} to {rating_after} stars through UX enhancements",
            "Implemented offline capabilities increasing user engagement by {percentage}%"
        ],
        "Cybersecurity": [
            "Implemented security measures reducing vulnerabilities by {percentage}%",
            "Led security assessment identifying and remediating {number} critical weaknesses",
            "Designed zero-trust architecture improving security posture by {percentage}%"
        ]
    }
   
    # Number of achievements based on experience - improved distribution
    if experience_years < 2:
        num_achievements = random.randint(1, 2)
    elif experience_years < 5:
        num_achievements = random.randint(2, 3)
    elif experience_years < 10:
        num_achievements = random.randint(2, 4)
    else:
        num_achievements = random.randint(3, 5)
   
    # Get category-specific achievements or default to base achievements
    specific_achievements = category_achievements.get(category, [])
    all_achievement_templates = base_achievements + specific_achievements
   
    # Select random achievement templates
    selected_templates = random.sample(all_achievement_templates, min(num_achievements, len(all_achievement_templates)))
   
    # Fill in the templates with realistic data
    achievements = []
    for template in selected_templates:
        achievement = template
       
        # Replace placeholders with realistic values
        if "{team_size}" in achievement:
            achievement = achievement.replace("{team_size}", str(random.randint(2, 12)))
       
        if "{ahead_behind}" in achievement:
            achievement = achievement.replace("{ahead_behind}", random.choice(["ahead of", "on", "under"]))
           
        if "{percentage}" in achievement:
            achievement = achievement.replace("{percentage}", str(random.randint(10, 60)))
           
        if "{component}" in achievement:
            components = ["database queries", "algorithm", "caching strategy", "API endpoints", "front-end rendering", "backend services", "data pipeline"]
            achievement = achievement.replace("{component}", random.choice(components))
           
        if "{data_system}" in achievement:
            systems = ["database from MySQL to PostgreSQL", "monolith to microservices", "on-prem infrastructure to AWS cloud", "legacy system to modern stack", "data warehouse to cloud platform"]
            achievement = achievement.replace("{data_system}", random.choice(systems))
           
        if "{process}" in achievement:
            processes = ["development", "deployment", "testing", "data processing", "reporting", "build", "release", "integration", "analysis"]
            achievement = achievement.replace("{process}", random.choice(processes))
           
        if "{solution}" in achievement:
            solutions = ["automated pipelines", "optimized algorithms", "parallel processing", "caching mechanisms", "better tooling", "cloud services", "container orchestration"]
            achievement = achievement.replace("{solution}", random.choice(solutions))
           
        if "{time_saved}" in achievement:
            achievement = achievement.replace("{time_saved}", str(random.randint(5, 40)))
           
        if "{period}" in achievement:
            achievement = achievement.replace("{period}", random.choice(["week", "month", "sprint", "quarter", "deployment"]))
           
        if "{award_name}" in achievement:
            awards = ["Star Performer Award", "Excellence Award", "Innovation Recognition", "Employee of the Quarter", "Best Team Player", "Technical Excellence Award"]
            achievement = achievement.replace("{award_name}", random.choice(awards))
           
        if "{project_aspect}" in achievement:
            aspects = ["project delivery", "innovation", "client satisfaction", "problem-solving", "technical leadership", "code quality", "mentoring"]
            achievement = achievement.replace("{project_aspect}", random.choice(aspects))
           
        if "{technology}" in achievement:
            technologies = ["CI/CD pipeline", "cloud migration strategy", "containerization", "automated testing framework", "new architecture", "microservices", "serverless computing"]
            achievement = achievement.replace("{technology}", random.choice(technologies))
           
        if "{amount}" in achievement:
            achievement = achievement.replace("{amount}", f"{random.randint(1, 50)},{random.randint(10, 99)},000")
           
        if "{feature}" in achievement:
            features = ["authentication system", "reporting module", "analytics dashboard", "API gateway", "mobile application", "recommendation engine", "search functionality"]
            achievement = achievement.replace("{feature}", random.choice(features))
           
        if "{metric}" in achievement:
            metrics = ["user engagement", "conversion rate", "customer retention", "application performance", "system reliability", "response time", "throughput"]
            achievement = achievement.replace("{metric}", random.choice(metrics))
           
        if "{number}" in achievement:
            achievement = achievement.replace("{number}", str(random.randint(2, 10)))
           
        if "{skill_area}" in achievement:
            areas = ["software development practices", "testing methodologies", "cloud technologies", "data structures and algorithms", "system design", "DevOps practices", "agile methodologies"]
            achievement = achievement.replace("{skill_area}", random.choice(areas))
           
        if "{time_period}" in achievement:
            achievement = achievement.replace("{time_period}", f"{random.randint(1, 24)} hours")
           
        if "{accuracy_before}" in achievement:
            before = random.randint(50, 80)
            after = before + random.randint(5, 20)
            achievement = achievement.replace("{accuracy_before}", str(before))
            achievement = achievement.replace("{accuracy_after}", str(min(after, 99)))
           
        if "{time_before}" in achievement:
            time_units = ["minutes", "hours", "days"]
            unit = random.choice(time_units)
            before = random.randint(5, 60) if unit == "minutes" else random.randint(1, 12)
            after = max(1, int(before / random.uniform(2, 5)))
            achievement = achievement.replace("{time_before}", f"{before} {unit}")
            achievement = achievement.replace("{time_after}", f"{after} {unit}")
           
        if "{benefit}" in achievement:
            benefits = ["improved scalability", "50% faster deployment", "reduced system coupling", "better fault isolation", "improved maintainability", "enhanced security"]
            achievement = achievement.replace("{benefit}", random.choice(benefits))
           
        if "{algorithm}" in achievement:
            algorithms = ["XGBoost algorithm", "custom neural network", "ensemble method", "transfer learning approach", "reinforcement learning model", "transformer-based model"]
            achievement = achievement.replace("{algorithm}", random.choice(algorithms))
           
        if "{accuracy}" in achievement:
            achievement = achievement.replace("{accuracy}", str(random.randint(85, 99)))
            
        if "{volume}" in achievement:
            volumes = [f"{random.randint(1, 50)}K", f"{random.randint(1, 10)}M", f"{random.randint(100, 999)}K"]
            achievement = achievement.replace("{volume}", random.choice(volumes))
            
        if "{rating_before}" in achievement:
            before = random.randint(2, 4)
            after = before + random.randint(1, 5 - before)
            achievement = achievement.replace("{rating_before}", str(before))
            achievement = achievement.replace("{rating_after}", str(after))
       
        achievements.append(achievement)
   
    return achievements

# Enhanced function to generate languages
def generate_languages():
    """Generate programming and human languages known with better distribution"""
   
    # Indian languages commonly found on resumes - geographical balance
    north_indian = ["Hindi", "Punjabi", "Urdu"]
    south_indian = ["Tamil", "Telugu", "Malayalam", "Kannada"]
    east_indian = ["Bengali", "Odia", "Assamese"]
    west_indian = ["Marathi", "Gujarati"]
    common = ["English"]
    
    indian_languages = north_indian + south_indian + east_indian + west_indian + common
   
    # Programming languages pool with realistic distributions
    programming_languages = {
        "common": ["Python", "Java", "JavaScript", "C++"],
        "backend": ["PHP", "C#", "Go", "Ruby"],
        "frontend": ["TypeScript", "Swift", "Kotlin"],
        "data": ["R", "Scala", "Shell", "Perl"]
    }
   
    # Select random languages - more realistic distribution
    # Most people in India know 2-3 languages
    num_indian = random.randint(2, 3)
    
    # Region-focused selection (people tend to know languages from their region)
    region = random.choice(["north", "south", "east", "west"])
    region_languages = {
        "north": north_indian,
        "south": south_indian,
        "east": east_indian,
        "west": west_indian
    }
    
    # Always include English and 1-2 regional languages
    spoken_languages = ["English"]  
    regional_choices = random.sample(region_languages[region], min(2, len(region_languages[region])))
    spoken_languages.extend(regional_choices)
    
    # Maybe add one more random Indian language
    if len(spoken_languages) < num_indian and random.random() > 0.5:
        other_languages = [lang for lang in indian_languages if lang not in spoken_languages]
        if other_languages:
            spoken_languages.append(random.choice(other_languages))
    
    # Programming languages - most developers know 3-5 languages
    num_programming = random.randint(3, 5)
    
    # Always include at least one common language
    prog_languages = [random.choice(programming_languages["common"])]
    
    # Add languages from different categories based on random selection
    remaining = num_programming - len(prog_languages)
    all_programming = [lang for category in programming_languages.values() for lang in category]
    additional_langs = random.sample([lang for lang in all_programming if lang not in prog_languages], 
                                     min(remaining, len(all_programming) - 1))
    prog_languages.extend(additional_langs)
   
    return {
        "spoken": spoken_languages,
        "programming": prog_languages
    }

# Function to generate a realistic resume with enhanced balancing
def generate_resume(id):
    """Generate a single synthetic resume with Indian tech industry focus"""
   
    # Select random category using a more balanced distribution
    # Adjusted weights to ensure more representation for underrepresented categories
    weights = [
        12,  # Software Development
        10,  # Data Science
        9,   # Machine Learning Engineering
        10,  # Full Stack Development
        9,   # DevOps Engineering (increased)
        8,   # Cloud Architecture (increased)
        8,   # Frontend Development
        8,   # Backend Development
        8,   # Mobile App Development
        7,   # UI/UX Design
        7,   # QA & Testing
        7,   # Cybersecurity
        7,   # Database Administration (increased)
        6,   # Product Management
        6,   # Business Intelligence
        5,   # ERP/SAP Consultant
        5,   # Technical Support
        5,   # Systems Administration
        5,   # Network Engineering
        6,   # IT Project Management
        7,   # Data Engineering (new)
        5,   # IoT Development (new)
        5    # Embedded Systems (new)
    ]
    
    category = random.choices(TECH_CATEGORIES, weights=weights, k=1)[0]
   
    # Determine experience level with a better distribution
    # Modified to have more mid-level candidates (5-8 years) which was underrepresented
    exp_weights = [
        15,  # 0 years
        18,  # 1 year
        17,  # 2 years
        16,  # 3 years
        15,  # 4 years
        14,  # 5 years - increased
        13,  # 6 years - increased
        12,  # 7 years - increased
        11,  # 8 years - increased
        9,   # 9 years
        8,   # 10 years
        6,   # 11 years
        6,   # 12 years
        5,   # 13 years
        4,   # 14 years
        4,   # 15 years
        3,   # 16 years
        3,   # 17 years
        2,   # 18 years
        2,   # 19 years
        2    # 20 years
    ]
    
    experience_years = random.choices(range(21), weights=exp_weights, k=1)[0]
   
    # Select skills for this category with better normalization
    category_skills = TECH_SKILLS.get(category, [])
    num_skills = random.randint(5, min(15, len(category_skills)))
    raw_skills = random.sample(category_skills, num_skills)
    
    # Normalize skill names for consistency
    skills = [normalize_skill_name(skill) for skill in raw_skills]
   
    # Add some general tech skills - normalized to avoid duplicates
    general_skills = ["Git", "GitHub", "Agile", "Scrum", "JIRA", "Communication", "Problem Solving", "Team Collaboration", "English Proficiency"]
    normalized_general = [normalize_skill_name(skill) for skill in general_skills]
    skills.extend(random.sample(normalized_general, random.randint(2, 5)))
    skills = list(set(skills))  # Remove duplicates
   
    # Generate name with Indian context - better geographical distribution
    indian_first_names = [
        # North Indian names
        "Aarav", "Arjun", "Aditya", "Anand", "Aryan", "Arnav", "Abhishek", "Akshay", "Ajay", "Amit",
        "Aanya", "Aadhya", "Ananya", "Avni", "Aisha", "Amara", "Anaya", "Anika", "Anjali", "Aditi",
        # South Indian names
        "Aadhavan", "Karthik", "Vijay", "Harish", "Surya", "Aravind", "Sundar", "Dhanush", "Arjun", "Karthikeyan",
        "Kavya", "Divya", "Keerthi", "Lakshmi", "Aishwarya", "Thara", "Meena", "Priya", "Deepa", "Shreya",
        # East Indian names
        "Rajiv", "Rahul", "Rohit", "Arnab", "Debashish", "Saurav", "Pritam", "Soumya", "Anirban", "Ashoke",
        "Mohua", "Payel", "Ankita", "Suchitra", "Tanushree", "Mitra", "Poulami", "Shreya", "Ritika", "Jaya",
        # West Indian names
        "Rohan", "Raj", "Rishi", "Nikhil", "Siddharth", "Mihir", "Vivek", "Samir", "Amar", "Jay",
        "Neha", "Nisha", "Natasha", "Nandini", "Navya", "Naina", "Niharika", "Noor", "Neela", "Nitya"
    ]
   
    indian_last_names = [
        # North Indian surnames
        "Sharma", "Singh", "Kumar", "Gupta", "Verma", "Mishra", "Agarwal", "Khanna", "Chopra", "Malhotra",
        # South Indian surnames
        "Reddy", "Rao", "Nair", "Menon", "Pillai", "Iyer", "Iyengar", "Subramaniam", "Krishnan", "Venkatesh",
        # East Indian surnames
        "Banerjee", "Chatterjee", "Mukherjee", "Das", "Bose", "Sen", "Ghosh", "Dutta", "Roy", "Dasgupta",
        # West Indian surnames
        "Patel", "Shah", "Joshi", "Desai", "Mehta", "Kulkarni", "Deshmukh", "Deshpande", "Patil", "Jain"
    ]
   
    first_name = random.choice(indian_first_names)
    last_name = random.choice(indian_last_names)
    name = f"{first_name} {last_name}"
   
    # Generate location (Indian cities with tech hubs) - better geographical balance
    location = random.choice(INDIAN_CITIES)
   
    # Generate career objective
    objective_templates = CAREER_OBJECTIVES.get(category, CAREER_OBJECTIVES["Software Development"])
    objective = random.choice(objective_templates)
    skill_sample = random.sample(skills, min(3, len(skills)))
    objective = objective.replace("{skills}", ", ".join(skill_sample))
    objective = objective.replace("{experience}", str(experience_years))
   
    # Generate career timeline
    career = generate_career_timeline(category, experience_years)
   
    # Generate education
    education = generate_education(category, experience_years)
   
    # Generate projects
    projects = generate_projects(category, skills, experience_years)
   
    # Generate certifications
    certifications = generate_certifications(category, experience_years)
   
    # Generate key achievements
    achievements = generate_key_achievements(category, experience_years)
   
    # Generate languages
    languages = generate_languages()
   
    # Generate contact information (with Indian context)
    email = f"{first_name.lower()}.{last_name.lower()}{random.choice(['', random.randint(1, 99)])}{random.choice(['@gmail.com', '@yahoo.com', '@outlook.com', '@hotmail.com'])}"
   
    # Indian mobile numbers start with formats like +91 98xxx xxxxx or similar
    phone = f"+91 {random.choice(['9', '8', '7'])}{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)} {random.randint(100, 999)} {random.randint(100, 999)}"
   
    # Generate match score for the job (for training/testing the model)
    # More realistic matching algorithm
    base_score = 0.50 + random.uniform(0, 0.15)  # Base score between 0.5 and 0.65
    experience_boost = min(0.2, experience_years * 0.015)  # Experience boost up to 0.2
    
    # Skills match - more weight to this factor
    skills_match = random.uniform(0, 0.15)  # Skills match boost up to 0.15
    
    # Education quality boost
    education_boost = 0
    for edu in education:
        if edu.get("tier") == "premier" and "degree" in edu and any(x in edu["degree"] for x in ["B.Tech", "M.Tech", "PhD"]):
            education_boost = 0.05
            break
    
    # Certification boost
    cert_boost = min(0.05, len(certifications) * 0.01)  # Up to 0.05 boost for certifications
    
    # Calculate final score with some randomization
    match_score = min(0.98, base_score + experience_boost + skills_match + education_boost + cert_boost)
    match_score = round(match_score, 2)
   
    # LinkedIn URL
    linkedin = f"linkedin.com/in/{first_name.lower()}-{last_name.lower()}-{random.randint(10000, 99999)}"
   
    # Generate resume text content
    resume_content = f"""
{name}
{location} | {phone} | {email} | {linkedin}

CAREER OBJECTIVE:
{objective}

SKILLS:
{', '.join(skills)}

EXPERIENCE:
{
    ''.join(f"""
{job['title']} at {job['company']}
{job['start_date']} to {job['end_date']} ({job['duration']})
- {'Led and mentored a team of junior developers, improving team productivity by 20%' if random.random() > 0.7 and not job.get('is_internship', False) else 'Collaborated with cross-functional teams to deliver high-quality solutions'}
- {'Developed and maintained scalable applications using ' + ', '.join(random.sample(skills, min(3, len(skills))))}
- {'Implemented best practices and optimized processes for greater efficiency' if random.random() > 0.5 else 'Participated in code reviews and ensured code quality standards were met'}
""" for job in career)
}

EDUCATION:
{
    ''.join(f"""
{edu['degree']} - {edu['university']} ({edu['year']})
""" for edu in education)
}

PROJECTS:
{
    ''.join(f"""
{project['name']}
Technologies: {', '.join(project['tech'])}
{project['description']}
""" for project in projects)
}

{
    "" if not certifications else "CERTIFICATIONS:\n" + ''.join(f"{cert['name']} - {cert['issuer']} ({cert['year']})\n" for cert in certifications)
}

{
    "" if not achievements else "KEY ACHIEVEMENTS:\n" + ''.join(f"• {achievement}\n" for achievement in achievements)
}

LANGUAGES:
Programming: {', '.join(languages['programming'])}
Spoken: {', '.join(languages['spoken'])}
"""

    # Create the final resume object with all fields required for high accuracy
    resume = {
        "candidate_id": f"IND-TECH-{id:05d}",
        "name": name,
        "location": location,
        "contact": phone,
        "email": email,
        "linkedin_url": linkedin,
        "Resume": resume_content,
        "skills": skills,
        "technical_skills": [skill for skill in skills if skill not in general_skills],
        "soft_skills": [skill for skill in skills if skill in general_skills],
        "experience_years": experience_years,
        "job_titles": [job["title"] for job in career],
        "companies": [job["company"] for job in career],
        "education_degree": education[0]["degree"] if education else "",
        "education_institution": education[0]["university"] if education else "",
        "education_year": education[0]["year"] if education else "",
        "major_field": education[0]["degree"].split("in")[-1].strip() if education and "in" in education[0]["degree"] else "",
        "Category": category,
        "match_score": match_score,
        "keywords": extract_keywords(resume_content, category),
        "domain": determine_domain(career, category),
        "career_objective": objective,
        "certifications": [cert["name"] for cert in certifications],
        "languages_spoken": languages["spoken"],
        "languages_programming": languages["programming"],
        "projects": [p["name"] for p in projects],
        "key_achievements": achievements,
        "submission_date": f"{fake.date_between(start_date='-1y', end_date='today')} {fake.time()}",
        "last_updated": f"{fake.date_between(start_date='-6m', end_date='today')} {fake.time()}",
        "is_synthetic": True,
        "source": "synthetic_indian_tech"
    }
   
    return resume

def extract_keywords(text, category):
    """Extract relevant keywords from resume text based on category"""
    # Enhanced keyword extraction based on category and common technical terms
    keywords = []
   
    # Add category-specific keywords
    category_keywords = {
        "Software Development": ["development", "coding", "programming", "software", "developer", "architecture"],
        "Data Science": ["data", "analytics", "statistics", "prediction", "model", "machine learning", "insights"],
        "Machine Learning Engineering": ["machine learning", "ai", "models", "algorithms", "neural networks", "deep learning"],
        "DevOps Engineering": ["devops", "ci/cd", "automation", "deployment", "infrastructure", "pipeline"],
        "Cloud Architecture": ["cloud", "aws", "azure", "gcp", "infrastructure", "serverless", "microservices"],
        "Frontend Development": ["frontend", "ui", "user interface", "react", "angular", "javascript", "web"],
        "Backend Development": ["backend", "api", "server", "database", "microservices", "services"],
        "Full Stack Development": ["fullstack", "frontend", "backend", "web", "development", "javascript"],
        "Mobile App Development": ["mobile", "app", "android", "ios", "react native", "flutter", "native"],
        "UI/UX Design": ["design", "user experience", "interface", "wireframe", "prototype", "usability"],
        "QA & Testing": ["testing", "quality", "automation", "test cases", "bug", "qa", "quality assurance"],
        "Cybersecurity": ["security", "cyber", "encryption", "firewall", "vulnerability", "protection"],
        "Database Administration": ["database", "sql", "nosql", "data", "admin", "management", "storage"],
        "Data Engineering": ["data pipeline", "etl", "data warehouse", "big data", "processing", "streaming"],
        "IoT Development": ["iot", "embedded", "sensors", "connected devices", "edge computing"],
        "Embedded Systems": ["embedded", "firmware", "hardware", "microcontroller", "real-time"]
    }
    
    if category in category_keywords:
        keywords.extend(category_keywords[category])
    else:
        keywords.extend(["technology", "IT", "technical", "professional"])
   
    # Extract technical terms using simple regex
    tech_terms_pattern = r'\b(AWS|Azure|GCP|SQL|API|REST|cloud|Java|Python|React|Angular|Node\.js|Docker|Kubernetes|Git|Agile|Scrum|ML|AI|IoT|DevOps|CI/CD|Testing|QA|Security)\b'
    import re
    tech_terms = re.findall(tech_terms_pattern, text)
   
    # Extract years of experience
    exp_pattern = r'(\d+)\+?\s*(?:years|year)(?:\s*of\s*experience)?'
    exp_matches = re.findall(exp_pattern, text)
    if exp_matches:
        keywords.append(f"{exp_matches[0]} years experience")
    
    # Extract education level
    edu_pattern = r'\b(B\.Tech|M\.Tech|MBA|MCA|BCA|PhD|Bachelor|Master)\b'
    edu_matches = re.findall(edu_pattern, text)
    if edu_matches:
        keywords.append(edu_matches[0])
    
    keywords.extend(tech_terms)
   
    # Remove duplicates and return
    return list(set(keywords))

def determine_domain(career, category):
    """Determine industry domain based on career and category - enhanced for better domain determination"""
    # Map companies to potential domains
    company_domain_map = {
        # IT Services
        "TCS": "IT Services",
        "Infosys": "IT Services",
        "Wipro": "IT Services",
        "HCL Technologies": "IT Services",
        "Tech Mahindra": "IT Services",
        "Cognizant India": "IT Services",
        "LTI": "IT Services",
        "Mindtree": "IT Services",
        "Capgemini India": "IT Services",
        
        # E-commerce & Consumer Tech
        "Flipkart": "E-commerce",
        "Amazon India": "E-commerce",
        "Myntra": "E-commerce",
        "Swiggy": "Food Tech",
        "Zomato": "Food Tech",
        "Grofers": "Retail Tech",
        "BigBasket": "Retail Tech",
        "Meesho": "E-commerce",
        "Nykaa": "E-commerce",
        "MakeMyTrip": "Travel Tech",
        
        # FinTech
        "Paytm": "FinTech",
        "PhonePe": "FinTech",
        "Razorpay": "FinTech",
        "PolicyBazaar": "FinTech",
        "CRED": "FinTech",
        "BharatPe": "FinTech",
        "Pine Labs": "FinTech",
        
        # EdTech
        "BYJU's": "EdTech",
        "Unacademy": "EdTech",
        "UpGrad": "EdTech",
        "Vedantu": "EdTech",
        
        # Transportation
        "Ola": "Transportation",
        "Uber India": "Transportation",
        "Delhivery": "Logistics",
        "Rivigo": "Logistics",
        "Ecom Express": "Logistics",
        
        # Global Tech Companies
        "Google India": "Technology",
        "Microsoft India": "Technology",
        "IBM India": "Technology",
        "Oracle India": "Technology",
        "SAP India": "Technology",
        "Adobe India": "Technology",
        "Cisco India": "Technology",
        "Dell India": "Technology",
        "HP India": "Technology",
        "Intel India": "Technology",
        
        # Financial Services
        "HSBC India": "Banking",
        "J.P. Morgan India": "Banking",
        "Morgan Stanley India": "Banking",
        "Goldman Sachs India": "Banking",
        "Barclays India": "Banking",
        "American Express India": "Banking",
        "Mastercard India": "Payments",
        
        # Consulting
                "Accenture India": "Consulting",
        "Deloitte India": "Consulting",
        "KPMG India": "Consulting",
        "PWC India": "Consulting",
        "EY India": "Consulting"
    }
   
    # Default domains based on category - enhanced mapping
    category_domain_map = {
        "Software Development": "Information Technology",
        "Data Science": "Analytics",
        "Machine Learning Engineering": "Artificial Intelligence",
        "DevOps Engineering": "Cloud Infrastructure",
        "Cloud Architecture": "Cloud Infrastructure",
        "Frontend Development": "Web Development",
        "Backend Development": "Web Development",
        "Full Stack Development": "Web Development",
        "Mobile App Development": "Mobile Technology",
        "UI/UX Design": "Design",
        "QA & Testing": "Quality Assurance",
        "Cybersecurity": "Security",
        "Database Administration": "Data Management",
        "Product Management": "Product Development",
        "Business Intelligence": "Business Analytics",
        "ERP/SAP Consultant": "Enterprise Solutions",
        "Technical Support": "IT Support",
        "Systems Administration": "IT Operations",
        "Network Engineering": "Networking",
        "IT Project Management": "Project Management",
        "Data Engineering": "Data Infrastructure",
        "IoT Development": "Internet of Things",
        "Embedded Systems": "Embedded Technology"
    }
   
    domains = []
   
    # Check if companies worked for map to known domains
    for job in career:
        company = job["company"]
        if company in company_domain_map:
            domains.append(company_domain_map[company])
   
    # Add domain based on category
    if category in category_domain_map:
        domains.append(category_domain_map[category])
   
    # If no domains found, add a default
    if not domains:
        domains.append("Information Technology")
   
    # Return the most common domain or the first one if all are equally common
    from collections import Counter
    domain_counts = Counter(domains)
    most_common = domain_counts.most_common(1)
    return most_common[0][0]

# Function to generate multiple resumes and save to CSV with better balance
def generate_resume_dataset(num_resumes=10000, output_file="synthetic_indian_tech_resumes.csv"):
    """Generate a dataset of synthetic tech resumes with Indian context and improved balance"""
   
    print(f"Generating {num_resumes} synthetic Indian tech resumes with enhanced balance...")
    resumes = []
   
    # Track categories to ensure better balance
    category_counts = {category: 0 for category in TECH_CATEGORIES}
    experience_distribution = {
        "entry": 0,      # 0-2 years
        "junior": 0,     # 3-5 years
        "mid": 0,        # 6-8 years
        "senior": 0,     # 9-12 years
        "lead": 0        # 13+ years
    }
    
    location_regions = {
        "north": 0,
        "south": 0,
        "east": 0,
        "west": 0,
        "northeast": 0,
        "central": 0
    }
   
    for i in tqdm(range(num_resumes), desc="Generating Resumes"):
        # Use adaptive generation to ensure balance
        if i > num_resumes * 0.2:  # After 20% of generation, start balancing
            # Find underrepresented categories
            min_category = min(category_counts, key=category_counts.get)
            
            # Generate resume with guidance toward underrepresented areas
            resume = generate_resume(i + 1)
            
            # If we need to balance categories and this isn't helping, regenerate
            attempts = 0
            while attempts < 3 and category_counts[resume["Category"]] > category_counts[min_category] * 1.5:
                resume = generate_resume(i + 1)
                attempts += 1
        else:
            # For first 20%, generate normally to assess natural distribution
            resume = generate_resume(i + 1)
        
        # Update tracking counts
        category_counts[resume["Category"]] += 1
        
        # Track experience distribution
        exp_years = resume["experience_years"]
        if exp_years <= 2:
            experience_distribution["entry"] += 1
        elif exp_years <= 5:
            experience_distribution["junior"] += 1
        elif exp_years <= 8:
            experience_distribution["mid"] += 1
        elif exp_years <= 12:
            experience_distribution["senior"] += 1
        else:
            experience_distribution["lead"] += 1
            
        # Track location distribution
        location = resume["location"]
        if any(city in location for city in ["Delhi", "Chandigarh", "Jaipur", "Lucknow"]):
            location_regions["north"] += 1
        elif any(city in location for city in ["Mumbai", "Pune", "Ahmedabad", "Surat"]):
            location_regions["west"] += 1
        elif any(city in location for city in ["Bangalore", "Chennai", "Hyderabad", "Kochi"]):
            location_regions["south"] += 1
        elif any(city in location for city in ["Kolkata", "Bhubaneswar"]):
            location_regions["east"] += 1
        elif any(city in location for city in ["Guwahati", "Shillong", "Imphal", "Agartala"]):
            location_regions["northeast"] += 1
        else:
            location_regions["central"] += 1
            
        resumes.append(resume)
   
    # Convert to DataFrame
    print("Converting to DataFrame...")
    resume_df = pd.DataFrame()
    resume_df["candidate_id"] = [r["candidate_id"] for r in resumes]
    resume_df["name"] = [r["name"] for r in resumes]
    resume_df["location"] = [r["location"] for r in resumes]
    resume_df["Category"] = [r["Category"] for r in resumes]
    resume_df["Resume"] = [r["Resume"] for r in resumes]
    resume_df["skills"] = [json.dumps(r["skills"]) for r in resumes]
    resume_df["experience_years"] = [r["experience_years"] for r in resumes]
    resume_df["job_titles"] = [json.dumps(r["job_titles"]) for r in resumes]
    resume_df["companies"] = [json.dumps(r["companies"]) for r in resumes]
    resume_df["education_degree"] = [r["education_degree"] for r in resumes]
    resume_df["education_institution"] = [r["education_institution"] for r in resumes]
    resume_df["match_score"] = [r["match_score"] for r in resumes]
    resume_df["domain"] = [r["domain"] for r in resumes]
    resume_df["keywords"] = [json.dumps(r["keywords"]) for r in resumes]
    resume_df["certifications"] = [json.dumps(r["certifications"]) for r in resumes]
    resume_df["languages_spoken"] = [json.dumps(r["languages_spoken"]) for r in resumes]
    resume_df["languages_programming"] = [json.dumps(r["languages_programming"]) for r in resumes]
    resume_df["is_synthetic"] = True
   
    # Save to CSV
    print(f"Saving dataset to {output_file}...")
    resume_df.to_csv(output_file, index=False)
    print(f"Successfully generated {num_resumes} synthetic Indian tech resumes and saved to {output_file}")
   
    # Return statistics
    category_counts = resume_df["Category"].value_counts().to_dict()
    experience_stats = {
        "min": resume_df["experience_years"].min(),
        "max": resume_df["experience_years"].max(),
        "mean": resume_df["experience_years"].mean(),
        "median": resume_df["experience_years"].median()
    }
   
    return {
        "total_resumes": len(resume_df),
        "category_distribution": category_counts,
        "experience_stats": experience_stats,
        "experience_distribution": experience_distribution,
        "location_distribution": location_regions,
        "file_path": output_file
    }

if __name__ == "__main__":
    print("Starting enhanced synthetic Indian tech resume dataset generation...")
   
    # Generate resumes with increased count for better category coverage
    resume_stats = generate_resume_dataset(num_resumes=10000, output_file="enhanced_synthetic_indian_tech_resumes.csv")
   
    # Print statistics
    print("\n--- Enhanced Dataset Generation Complete ---")
    print("\nResume Dataset Statistics:")
    print(f"- Total Resumes: {resume_stats['total_resumes']}")
   
    print("\nCategory Distribution:")
    for category, count in sorted(resume_stats['category_distribution'].items(), key=lambda x: x[1], reverse=True):
        print(f"- {category}: {count} resumes ({count/resume_stats['total_resumes']*100:.1f}%)")
   
    print("\nExperience Level Distribution:")
    for level, count in resume_stats['experience_distribution'].items():
        print(f"- {level}: {count} resumes ({count/resume_stats['total_resumes']*100:.1f}%)")
        
    print("\nLocation Distribution:")
    for region, count in resume_stats['location_distribution'].items():
        print(f"- {region}: {count} resumes ({count/resume_stats['total_resumes']*100:.1f}%)")
   
    print("\nExperience Distribution:")
    for key, value in resume_stats['experience_stats'].items():
        print(f"- {key}: {value}")
   
    print(f"\nDataset saved to: {resume_stats['file_path']}")
