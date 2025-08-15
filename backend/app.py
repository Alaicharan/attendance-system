from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_mysqldb import MySQL
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'alaicharan12345'
app.config['MYSQL_DB'] = 'attendance_db'

mysql = MySQL(app)

@app.route('/api/attendance', methods=['GET', 'POST'])
def attendance():
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        query = """
        SELECT 
            s.idstudents AS id,
            s.name,
            s.department,
            s.section,
            s.batch,
            a.in_time,
            DATE(a.in_time) AS in_date,
            a.out_time,
            DATE(a.out_time) AS out_date
        FROM students s
        LEFT JOIN attendance a ON s.idstudents = a.student_id
        ORDER BY a.in_time DESC
        """
        cur.execute(query)
        rows = cur.fetchall()
        data = []
        for r in rows:
            data.append({
                'id': r[0],
                'name': r[1],
                'department': r[2],
                'section': r[3],
                'batch': r[4],
                'in_time': str(r[5]) if r[5] else None,
                'in_date': str(r[6]) if r[6] else None,
                'out_time': str(r[7]) if r[7] else None,
                'out_date': str(r[8]) if r[8] else None
            })
        cur.close()
        return jsonify(data)
    
    elif request.method == 'POST':
        try:
            data = request.get_json()
            student_id = data.get('student_id')
            in_time = data.get('in_time')
            
            if not student_id or not in_time:
                return jsonify({'error': 'Missing student_id or in_time'}), 400
            
            cur = mysql.connection.cursor()
            
            # Check if student exists
            cur.execute("SELECT idstudents FROM students WHERE idstudents = %s", (student_id,))
            if not cur.fetchone():
                cur.close()
                return jsonify({'error': 'Student not found'}), 404
            
            # Insert attendance record
            cur.execute("""
                INSERT INTO attendance (student_id, in_time) 
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE in_time = VALUES(in_time)
            """, (student_id, in_time))
            
            mysql.connection.commit()
            cur.close()
            
            return jsonify({'message': f'Attendance marked for student {student_id}', 'in_time': in_time}), 201
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@app.route('/test_db')
def test_db():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT 1")
        result = cur.fetchone()
        cur.close()
        if result:
            return "Database connection successful!"
        return "Failed to connect"
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/api/reports/daily', methods=['GET'])
def daily_report():
    """Get daily attendance summary"""
    try:
        date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
        
        cur = mysql.connection.cursor()
        
        # Get total students
        cur.execute("SELECT COUNT(*) FROM students")
        total_students = cur.fetchone()[0]
        
        # Get present students for the date
        cur.execute("""
            SELECT COUNT(DISTINCT student_id) 
            FROM attendance 
            WHERE DATE(in_time) = %s
        """, (date,))
        present_students = cur.fetchone()[0]
        
        # Get absent students
        absent_students = total_students - present_students
        
        # Get attendance percentage
        attendance_percentage = round((present_students / total_students * 100), 2) if total_students > 0 else 0
        
        # Get detailed attendance for the date
        cur.execute("""
            SELECT 
                s.idstudents,
                s.name,
                s.department,
                s.section,
                s.batch,
                a.in_time,
                a.out_time,
                CASE 
                    WHEN a.in_time IS NOT NULL THEN 'Present'
                    ELSE 'Absent'
                END as status
            FROM students s
            LEFT JOIN attendance a ON s.idstudents = a.student_id AND DATE(a.in_time) = %s
            ORDER BY s.name
        """, (date,))
        
        attendance_details = []
        for row in cur.fetchall():
            attendance_details.append({
                'id': row[0],
                'name': row[1],
                'department': row[2],
                'section': row[3],
                'batch': row[4],
                'in_time': str(row[5]) if row[5] else None,
                'out_time': str(row[6]) if row[6] else None,
                'status': row[7]
            })
        
        cur.close()
        
        return jsonify({
            'date': date,
            'summary': {
                'total_students': total_students,
                'present_students': present_students,
                'absent_students': absent_students,
                'attendance_percentage': attendance_percentage
            },
            'details': attendance_details
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/reports/student/<int:student_id>', methods=['GET'])
def student_report(student_id):
    """Get attendance report for a specific student"""
    try:
        cur = mysql.connection.cursor()
        
        # Get student info
        cur.execute("""
            SELECT name, department, section, batch 
            FROM students 
            WHERE idstudents = %s
        """, (student_id,))
        
        student_info = cur.fetchone()
        if not student_info:
            return jsonify({'error': 'Student not found'}), 404
        
        # Get attendance records
        cur.execute("""
            SELECT 
                DATE(in_time) as date,
                in_time,
                out_time,
                TIMESTAMPDIFF(MINUTE, in_time, out_time) as duration_minutes
            FROM attendance 
            WHERE student_id = %s 
            ORDER BY in_time DESC
        """, (student_id,))
        
        attendance_records = []
        for row in cur.fetchall():
            attendance_records.append({
                'date': str(row[0]),
                'in_time': str(row[1]) if row[1] else None,
                'out_time': str(row[2]) if row[2] else None,
                'duration_minutes': row[3] if row[3] else 0
            })
        
        # Calculate statistics
        total_days = len(attendance_records)
        total_hours = sum(record['duration_minutes'] for record in attendance_records) / 60
        
        cur.close()
        
        return jsonify({
            'student': {
                'id': student_id,
                'name': student_info[0],
                'department': student_info[1],
                'section': student_info[2],
                'batch': student_info[3]
            },
            'statistics': {
                'total_days': total_days,
                'total_hours': round(total_hours, 2),
                'average_hours_per_day': round(total_hours / total_days, 2) if total_days > 0 else 0
            },
            'attendance_records': attendance_records
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/reports/range', methods=['GET'])
def date_range_report():
    """Get attendance report for a date range"""
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        if not start_date or not end_date:
            return jsonify({'error': 'Start date and end date are required'}), 400
        
        cur = mysql.connection.cursor()
        
        # Get attendance summary for the date range
        cur.execute("""
            SELECT 
                DATE(in_time) as date,
                COUNT(DISTINCT student_id) as present_count
            FROM attendance 
            WHERE DATE(in_time) BETWEEN %s AND %s
            GROUP BY DATE(in_time)
            ORDER BY date
        """, (start_date, end_date))
        
        daily_summary = []
        for row in cur.fetchall():
            daily_summary.append({
                'date': str(row[0]),
                'present_count': row[1]
            })
        
        # Get department-wise summary
        cur.execute("""
            SELECT 
                s.department,
                COUNT(DISTINCT s.idstudents) as total_students,
                COUNT(DISTINCT a.student_id) as present_students
            FROM students s
            LEFT JOIN attendance a ON s.idstudents = a.student_id 
                AND DATE(a.in_time) BETWEEN %s AND %s
            GROUP BY s.department
        """, (start_date, end_date))
        
        department_summary = []
        for row in cur.fetchall():
            department_summary.append({
                'department': row[0],
                'total_students': row[1],
                'present_students': row[2],
                'attendance_percentage': round((row[2] / row[1] * 100), 2) if row[1] > 0 else 0
            })
        
        cur.close()
        
        return jsonify({
            'date_range': {
                'start_date': start_date,
                'end_date': end_date
            },
            'daily_summary': daily_summary,
            'department_summary': department_summary
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
