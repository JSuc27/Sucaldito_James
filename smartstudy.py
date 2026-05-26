import json
import random
import os
from datetime import datetime

class Question:
    def __init__(self, q, options, answer, difficulty="Medium"):
        self.question = q
        self.options = options
        self.answer = answer
        self.difficulty = difficulty

class Subject:
    def __init__(self, name):
        self.name = name
        self.questions = []

    def add_question(self, q, options, answer, difficulty="Medium"):
        self.questions.append(Question(q, options, answer, difficulty))

class SmartStudyPro:
    def __init__(self):
        self.subjects = {}
        self.history = []
        self.load_data()

    def load_data(self):
        if os.path.exists("study_pro.json"):
            with open("study_pro.json", "r") as f:
                data = json.load(f)
                for sub_name, qlist in data.get("subjects", {}).items():
                    self.subjects[sub_name] = Subject(sub_name)
                    for q in qlist:
                        self.subjects[sub_name].add_question(q["q"], q["options"], q["answer"], q.get("difficulty", "Medium"))
                self.history = data.get("history", [])

    def save_data(self):
        data = {
            "subjects": {name: [{"q": q.question, "options": q.options, 
                               "answer": q.answer, "difficulty": q.difficulty} 
                               for q in sub.questions] 
                        for name, sub in self.subjects.items()},
            "history": self.history
        }
        with open("study_pro.json", "w") as f:
            json.dump(data, f, indent=4)

    def add_subject(self):
        name = input("Enter subject name: ")
        self.subjects[name] = Subject(name)
        print(f"✅ {name} added!")

    def add_question(self):
        sub = input("Enter subject: ")
        if sub not in self.subjects:
            print("Subject not found! Creating new...")
            self.subjects[sub] = Subject(sub)
        q = input("Question: ")
        options = [input(f"Option {chr(65+i)}: ") for i in range(4)]
        ans = input("Correct option (A/B/C/D): ").upper()
        diff = input("Difficulty (Easy/Medium/Hard): ") or "Medium"
        self.subjects[sub].add_question(q, options, ans, diff)
        print("✅ Question added!")

    def take_quiz(self):
        if not self.subjects:
            print("No subjects yet!")
            return
        sub_name = input("Choose subject: ")
        if sub_name not in self.subjects or not self.subjects[sub_name].questions:
            print("No questions in this subject!")
            return

        num = int(input("How many questions? (max 10): ") or 5)
        questions = random.sample(self.subjects[sub_name].questions, min(num, len(self.subjects[sub_name].questions)))
        
        score = 0
        print(f"\n🚀 {sub_name} Quiz Started!\n")
        
        for i, q in enumerate(questions, 1):
            print(f"Q{i}: {q.question}")
            for idx, opt in enumerate(q.options):
                print(f"   {chr(65+idx)}. {opt}")
            ans = input("Answer: ").upper()
            if ans == q.answer:
                score += 1
                print("✅ Correct!\n")
            else:
                print(f"❌ Wrong. Correct: {q.answer}\n")

        percentage = (score / len(questions)) * 100
        print(f"🎯 Final Score: {score}/{len(questions)} ({percentage:.1f}%)")

        self.history.append({
            "date": str(datetime.now().date()),
            "subject": sub_name,
            "score": percentage,
            "questions": len(questions)
        })
        self.save_data()

    def show_progress(self):
        if not self.history:
            print("No history yet.")
            return
        print("\n Your Study Progress:")
        for entry in self.history[-10:]:
            print(f"{entry['date']} | {entry['subject']} | {entry['score']:.1f}% ({entry['questions']} Qs)")

        if self.history:
            avg = sum(h['score'] for h in self.history) / len(self.history)
            print(f"\n Average Score: {avg:.1f}%")

    def menu(self):
        while True:
            print("\n" + "="*55)
            print("📚 SMARTSTUDY PRO - Intelligent Study Assistant")
            print("="*55)
            print("1. Add Subject")
            print("2. Add Question")
            print("3. Take Quiz")
            print("4. View Progress & Statistics")
            print("5. Exit")
            choice = input("\nEnter choice: ")
            
            if choice == "1": self.add_subject()
            elif choice == "2": self.add_question()
            elif choice == "3": self.take_quiz()
            elif choice == "4": self.show_progress()
            elif choice == "5":
                self.save_data()
                print("Thank you for using SmartStudy Pro! Keep Safe and Study Hard!")
                break

if __name__ == "__main__":
    app = SmartStudyPro()
    app.menu()