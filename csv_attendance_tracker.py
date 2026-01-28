import csv
import os
from datetime import datetime


class CSVAttendanceTracker:
    """Attendance tracker using CSV files"""
    
    def __init__(self, students_file="students.csv", attendance_file="attendance.csv"):
        self.students_file = students_file
        self.attendance_file = attendance_file
        self.ensure_files_exist()
    
    def ensure_files_exist(self):
        """Create CSV files if they don't exist"""
        if not os.path.exists(self.students_file):
            with open(self.students_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Student ID', 'Name', 'Date Added'])
        
        if not os.path.exists(self.attendance_file):
            with open(self.attendance_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Student ID', 'Date', 'Status'])
    
    def add_student(self, student_id, name):
        """Add a new student"""
        # Check if student already exists
        with open(self.students_file, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            for row in reader:
                if row[0] == student_id:
                    print(f"Student {student_id} already exists!")
                    return False
        
        # Add new student
        with open(self.students_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([student_id, name, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
        
        print(f"Student {name} (ID: {student_id}) added successfully!")
        return True
    
    def mark_attendance(self, student_id, date=None, status="Present"):
        """Mark attendance for a student"""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        # Check if student exists
        student_exists = False
        student_name = ""
        with open(self.students_file, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            for row in reader:
                if row[0] == student_id:
                    student_exists = True
                    student_name = row[1]
                    break
        
        if not student_exists:
            print(f"Student {student_id} not found!")
            return False
        
        # Remove existing attendance for this date if any
        with open(self.attendance_file, 'r') as f:
            rows = list(csv.reader(f))
        
        with open(self.attendance_file, 'w', newline='') as f:
            writer = csv.writer(f)
            for row in rows:
                if not (row[0] == student_id and row[1] == date):
                    writer.writerow(row)
        
        # Add new attendance
        with open(self.attendance_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([student_id, date, status])
        
        print(f"Attendance marked for {student_name} on {date}: {status}")
        return True
    
    def get_student_attendance(self, student_id):
        """Get attendance records for a student"""
        # Find student name
        student_name = None
        with open(self.students_file, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            for row in reader:
                if row[0] == student_id:
                    student_name = row[1]
                    break
        
        if student_name is None:
            print(f"Student {student_id} not found!")
            return None
        
        attendance = []
        with open(self.attendance_file, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            for row in reader:
                if row[0] == student_id:
                    attendance.append((row[1], row[2]))  # (date, status)
        
        return {
            "name": student_name,
            "attendance": sorted(attendance)
        }
    
    def get_attendance_summary(self, student_id):
        """Get attendance summary for a student"""
        record = self.get_student_attendance(student_id)
        if not record:
            return None
        
        attendance = record["attendance"]
        total_days = len(attendance)
        present_days = sum(1 for _, status in attendance if status == "Present")
        absent_days = sum(1 for _, status in attendance if status == "Absent")
        
        percentage = (present_days / total_days * 100) if total_days > 0 else 0
        
        return {
            "name": record["name"],
            "total_days": total_days,
            "present": present_days,
            "absent": absent_days,
            "percentage": round(percentage, 2)
        }
    
    def list_all_students(self):
        """List all students"""
        students = []
        with open(self.students_file, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            for row in reader:
                students.append({
                    "id": row[0],
                    "name": row[1]
                })
        return students
    
    def display_all_students(self):
        """Display all students in formatted table"""
        students = self.list_all_students()
        if not students:
            print("No students found!")
            return
        
        print("\n" + "="*50)
        print(f"{'Student ID':<15} {'Name':<30}")
        print("="*50)
        for student in students:
            print(f"{student['id']:<15} {student['name']:<30}")
        print("="*50 + "\n")
    
    def display_student_attendance(self, student_id):
        """Display attendance record for a student"""
        record = self.get_student_attendance(student_id)
        if not record:
            return
        
        print(f"\n{'='*50}")
        print(f"Attendance Record: {record['name']}")
        print(f"{'='*50}")
        print(f"{'Date':<15} {'Status':<15}")
        print(f"{'-'*30}")
        
        for date, status in record['attendance']:
            print(f"{date:<15} {status:<15}")
        print(f"{'='*50}\n")
    
    def display_attendance_summary(self, student_id):
        """Display attendance summary for a student"""
        summary = self.get_attendance_summary(student_id)
        if not summary:
            return
        
        print(f"\n{'='*50}")
        print(f"Attendance Summary: {summary['name']}")
        print(f"{'='*50}")
        print(f"Total Days:        {summary['total_days']}")
        print(f"Present:           {summary['present']}")
        print(f"Absent:            {summary['absent']}")
        print(f"Attendance %:      {summary['percentage']}%")
        print(f"{'='*50}\n")
    
    def delete_student(self, student_id):
        """Delete a student and their attendance records"""
        # Find and remove from students
        student_name = None
        with open(self.students_file, 'r') as f:
            rows = list(csv.reader(f))
        
        with open(self.students_file, 'w', newline='') as f:
            writer = csv.writer(f)
            for row in rows:
                if row[0] == student_id:
                    student_name = row[1]
                else:
                    writer.writerow(row)
        
        if student_name is None:
            print(f"Student {student_id} not found!")
            return False
        
        # Remove attendance records
        with open(self.attendance_file, 'r') as f:
            rows = list(csv.reader(f))
        
        with open(self.attendance_file, 'w', newline='') as f:
            writer = csv.writer(f)
            for row in rows:
                if row[0] != student_id:
                    writer.writerow(row)
        
        print(f"Student {student_name} (ID: {student_id}) deleted successfully!")
        return True


def main():
    """Main function with CLI menu"""
    tracker = CSVAttendanceTracker()
    
    while True:
        print("\n" + "="*50)
        print("   CSV ATTENDANCE TRACKER SYSTEM")
        print("="*50)
        print("1. Add Student")
        print("2. Mark Attendance")
        print("3. View Student Attendance")
        print("4. View Attendance Summary")
        print("5. List All Students")
        print("6. Delete Student")
        print("7. Exit")
        print("="*50)
        
        choice = input("Enter your choice (1-7): ").strip()
        
        if choice == "1":
            student_id = input("Enter Student ID: ").strip()
            name = input("Enter Student Name: ").strip()
            tracker.add_student(student_id, name)
        
        elif choice == "2":
            student_id = input("Enter Student ID: ").strip()
            date = input("Enter Date (YYYY-MM-DD) or press Enter for today: ").strip()
            if not date:
                date = datetime.now().strftime("%Y-%m-%d")
            status = input("Enter Status (Present/Absent): ").strip().capitalize()
            if status in ["Present", "Absent"]:
                tracker.mark_attendance(student_id, date, status)
            else:
                print("Invalid status! Please enter 'Present' or 'Absent'.")
        
        elif choice == "3":
            student_id = input("Enter Student ID: ").strip()
            tracker.display_student_attendance(student_id)
        
        elif choice == "4":
            student_id = input("Enter Student ID: ").strip()
            tracker.display_attendance_summary(student_id)
        
        elif choice == "5":
            tracker.display_all_students()
        
        elif choice == "6":
            student_id = input("Enter Student ID to delete: ").strip()
            confirm = input(f"Are you sure you want to delete {student_id}? (yes/no): ").strip().lower()
            if confirm == "yes":
                tracker.delete_student(student_id)
        
        elif choice == "7":
            print("Thank you for using Attendance Tracker. Goodbye!")
            break
        
        else:
            print("Invalid choice! Please try again.")


if __name__ == "__main__":
    main()
