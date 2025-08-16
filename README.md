# 🎯 Attendance System

A comprehensive, real-time attendance management system with camera integration, built using modern web technologies and AI capabilities.

## ✨ Features

### 🎥 **Camera Integration**
- Live camera feed for attendance marking
- Real-time face scanning capabilities
- Integrated attendance marking interface

### 📊 **Real-time Analytics**
- Live attendance tracking
- Daily, weekly, and monthly reports
- Student-specific attendance statistics
- Department-wise analytics

### 🖥️ **Modern Web Interface**
- Responsive design using Tailwind CSS
- Tabbed interface for easy navigation
- Real-time data updates
- Professional-grade UI/UX

### 🔧 **Backend Features**
- Flask RESTful API
- MySQL database integration
- CORS-enabled for cross-origin requests
- Comprehensive error handling

## 🛠️ Technology Stack

- **Frontend**: HTML5, JavaScript, Tailwind CSS
- **Backend**: Python Flask
- **Database**: MySQL
- **Camera**: WebRTC API
- **Deployment**: Local development server

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- MySQL 8.0+
- Modern web browser with camera access

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Alaicharan/attendance-system.git
cd attendance-system
```

2. **Create virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure database**
```sql
CREATE DATABASE attendance_db;
USE attendance_db;

-- Create tables (see database_setup.sql)
```

5. **Update database credentials**
Edit `backend/app.py` with your MySQL credentials:
```python
app.config['MYSQL_USER'] = 'your_username'
app.config['MYSQL_PASSWORD'] = 'your_password'
```

### Running the Application

1. **Start Backend Server**
```bash
cd backend
python app.py
```

2. **Start Frontend Server** (in new terminal)
```bash
cd frontend
python -m http.server 3000
```

3. **Access the Application**
Open your browser and go to: `http://localhost:3000`

## 📱 How to Use

### **Marking Attendance**
1. Click "🚀 Start Camera" to activate camera
2. Enter student ID in the input field
3. Click "✅ Mark Attendance" to record attendance
4. View real-time updates in the attendance table

### **Viewing Reports**
1. Switch to "Reports & Analytics" tab
2. Use Daily Report for today's summary
3. Generate Student Reports for individual statistics
4. Create Date Range Reports for trend analysis

## 🗄️ Database Schema

### Students Table
- `idstudents` (Primary Key)
- `name`
- `department`
- `section`
- `batch`

### Attendance Table
- `id` (Primary Key)
- `student_id` (Foreign Key)
- `in_time`
- `out_time`

## 🔌 API Endpoints

- `GET /api/attendance` - Get all attendance records
- `POST /api/attendance` - Mark new attendance
- `GET /api/reports/daily` - Daily attendance summary
- `GET /api/reports/student/<id>` - Student-specific report
- `GET /api/reports/range` - Date range analytics

## 🎨 Screenshots

### Main Interface
![Main Interface](screenshots/main-interface.png)

### Camera Scanner
![Camera Scanner](screenshots/camera-scanner.png)

### Reports Dashboard
![Reports Dashboard](screenshots/reports-dashboard.png)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Alaicharan**
- GitHub: [@Alaicharan](https://github.com/Alaicharan)
- Project Link: [https://github.com/Alaicharan/attendance-system](https://github.com/Alaicharan/attendance-system)

## 🙏 Acknowledgments

- Flask framework for backend
- Tailwind CSS for styling
- WebRTC API for camera integration
- MySQL for data persistence

---

⭐ **Star this repository if you find it helpful!**
