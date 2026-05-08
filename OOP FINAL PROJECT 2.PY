import json
import time

class QuizGame:
    def __init__(self, file_name):
        self.file_name = file_name
        self.questions = []
        self.leftover_questions = []
        self.correct_answers = 0
        self.time_limit = 30
        self.start_time = None

    def load_questions(self):
        with open(self.file_name, "r") as file:
            data = json.load(file)
            self.questions = data["questions"]
            self.leftover_questions = self.questions.copy()

    def start_timer(self):
        self.start_time = time.time()

    def remaining_time(self):
        time_left = self.time_limit - int(time.time() - self.start_time)
        return max(0, time_left)

    def start_quiz(self):
        self.start_timer()

        while self.leftover_questions and self.remaining_time() > 0:
            print("\n----------------------------")
            print("Time Left:", self.remaining_time(), "seconds")
            print("Questions Remaining:", len(self.leftover_questions))

            q = self.leftover_questions.pop(0)

            print("\nQuestion:", q["question"])
            for i, option in enumerate(q["options"], 1):
                print(f"{i}. {option}")

            user_answer = input("Choose option number: ")

            if self.remaining_time() == 0:
                print("\n⏰ Time Over!")
                break

            try:
                user_index = int(user_answer) - 1

                if user_index < 0 or user_index >= len(q["options"]):
                    raise IndexError

                if q["options"][user_index] == q["answer"]:
                    print(" Correct Answer")
                    self.correct_answers += 1
                else:
                    print(" Wrong Answer (will appear again)")
                    self.leftover_questions.append(q)

            except ValueError:
                print(" Enter a number only")
                self.leftover_questions.append(q)

            except IndexError:
                print(" Invalid option number")
                self.leftover_questions.append(q)

        self.show_result()

    def show_result(self):
        print("\n===== Quiz Completed =====")
        if self.correct_answers >= 2:
            print("Result: PASS ")
        else:
            print("Result: FAIL ")
        print("Good effort! Keep practicing.")


# Run Program
quiz = QuizGame("questions.json")
quiz.load_questions()
quiz.start_quiz()