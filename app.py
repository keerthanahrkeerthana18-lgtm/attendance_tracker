from flask import Flask, jsonify, request
from attendance_tracker import AttendanceTracker

app = Flask(__name__)
tracker = AttendanceTracker()

@app.route('/')
def index():
    return jsonify({"status": "ok", "message": "Attendance Tracker API"})

@app.route('/students', methods=['GET'])
def list_students():
    return jsonify(tracker.list_all_students())

@app.route('/students', methods=['POST'])
def add_student():
    data = request.get_json(force=True)
    student_id = data.get('student_id')
    name = data.get('name')
    if not student_id or not name:
        return jsonify({'error': 'student_id and name required'}), 400
    ok = tracker.add_student(student_id, name)
    if not ok:
        return jsonify({'error': 'student already exists'}), 400
    return jsonify({'message': 'student added'}), 201

@app.route('/students/<student_id>', methods=['GET'])
def get_student(student_id):
    record = tracker.get_student_attendance(student_id)
    if record is None:
        return jsonify({'error': 'student not found'}), 404
    return jsonify(record)

@app.route('/students/<student_id>/summary', methods=['GET'])
def get_summary(student_id):
    summary = tracker.get_attendance_summary(student_id)
    if summary is None:
        return jsonify({'error': 'student not found'}), 404
    return jsonify(summary)

@app.route('/attendance', methods=['POST'])
def mark_attendance():
    data = request.get_json(force=True)
    student_id = data.get('student_id')
    status = data.get('status', 'Present')
    date = data.get('date')
    if not student_id:
        return jsonify({'error': 'student_id required'}), 400
    ok = tracker.mark_attendance(student_id, date, status)
    if not ok:
        return jsonify({'error': 'student not found'}), 404
    return jsonify({'message': 'attendance recorded'}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
