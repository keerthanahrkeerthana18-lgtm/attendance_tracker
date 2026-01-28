import json
import os
from datetime import datetime
from pathlib import Path


class AttendanceTracker:
    def __init__(self, data_file="attendance_data.json"):
        self.data_file = data_file
        self.data = self.load_data()

    def load_data(self):
        """Load attendance data from JSON file"""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                return json.load(f)
        return {}

    def save_data(self):
        """Save attendance data to JSON file"""
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=2)

    def add_student(self, student_id, name):
        """Add a new student"""
        if student_id in self.data:
            print(f"Student {student_id} already exists!")
            return False
        
        self.data[student_id] = {
            "name": name,
            "attendance": {}
        }
        self.save_data()
        print(f"Student {name} (ID: {student_id}) added successfully!")
        return True

    def mark_attendance(self, student_id, date=None, status="Present"):
        """Mark attendance for a student"""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        if student_id not in self.data:
            print(f"Student {student_id} not found!")
            return False
        
        self.data[student_id]["attendance"][date] = status
        self.save_data()
        print(f"Attendance marked for {self.data[student_id]['name']} on {date}: {status}")
        return True

    def get_student_attendance(self, student_id):
        """Get attendance record for a student"""
        if student_id not in self.data:
            print(f"Student {student_id} not found!")
            return None
        
        student = self.data[student_id]
        return {
            "name": student["name"],
            "attendance": student["attendance"]
        }

    def get_attendance_summary(self, student_id):
        """Get attendance summary for a student"""
        if student_id not in self.data:
            print(f"Student {student_id} not found!")
            return None
        
        student = self.data[student_id]
        attendance = student["attendance"]
        
        total_days = len(attendance)
        present_days = sum(1 for status in attendance.values() if status == "Present")
        absent_days = sum(1 for status in attendance.values() if status == "Absent")
        
        percentage = (present_days / total_days * 100) if total_days > 0 else 0
        
        return {
            "name": student["name"],
            "total_days": total_days,
            "present": present_days,
            "absent": absent_days,
            "percentage": round(percentage, 2)
        }

    def list_all_students(self):
        """List all students"""
        if not self.data:
            print("No students found!")
            return []
        
        students = []
        for student_id, info in self.data.items():
            students.append({
                "id": student_id,
                "name": info["name"],
                "total_records": len(info["attendance"])
            })
        return students

    def display_all_students(self):
        """Display all students in formatted table"""
        students = self.list_all_students()
        if not students:
            return
        
        print("\n" + "="*50)
        print(f"{'Student ID':<15} {'Name':<20} {'Records':<10}")
        print("="*50)
        for student in students:
            print(f"{student['id']:<15} {student['name']:<20} {student['total_records']:<10}")
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
        
        for date, status in sorted(record['attendance'].items()):
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
        """Delete a student"""
        if student_id not in self.data:
            print(f"Student {student_id} not found!")
            return False
        
        name = self.data[student_id]["name"]
        del self.data[student_id]
        self.save_data()
        print(f"Student {name} (ID: {student_id}) deleted successfully!")
        return True


def main():
    """Main function with CLI menu"""
    tracker = AttendanceTracker()
    
    while True:
        print("\n" + "="*50)
        print("       ATTENDANCE TRACKER SYSTEM")
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
