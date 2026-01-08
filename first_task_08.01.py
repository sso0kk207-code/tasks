import json # json подключил

class Student:
    _id = 0 # счетчик, который помнит последний выданный номер id

    def __init__(self, name: str, student_id: int | None = None):
        # если id не передали (новый студент), берем следующий по порядку
        if student_id is None:
            Student._id += 1
            self.id = Student._id
        # если id пришел из файла, используем его и подтягиваем счетчик
        else:
            self.id = student_id
            Student._id = max(Student._id, student_id)
        
        self.name = name # имя
        self.subjects = {} # предметы со списками оценок

    def add_subject(self, subject: str):
        # проверяю, чтобы один и тот же предмет не добавили дважды
        if subject in self.subjects:
            raise ValueError("Already exists")
        self.subjects[subject] = [] # создаю пустой список под будущие оценки

    def remove_subject(self, subject: str):
        # если предмета нет, ошибка
        if subject not in self.subjects:
            raise KeyError("Subject not found")
        del self.subjects[subject] # удаляю предмет и все его оценки

    def add_grade(self, subject: str, grade: int):
        # если предмета нет, ошибка
        if subject not in self.subjects:
            raise KeyError("Subject not found")
        # проверяю, что оценка — целое число
        if not isinstance(grade, int):
            raise TypeError("Grade must be an integer type")
        # слежу, чтобы оценка была в школьном диапазоне от 1 до 5
        if grade < 1 or grade > 5:
            raise ValueError("Grade must be in a range from 1 to 5")
        self.subjects[subject].append(grade) # добавляю оценку в список к предмету

    def get_gpa(self) -> float:
        sum_grades = 0 # сумма всех оценок
        count_grades = 0 # количество всех оценок
        for grades in self.subjects.values():
            sum_grades += sum(grades)
            count_grades += len(grades)
        # если оценок еще нет, возвращаем 0, чтобы не делить на ноль
        if count_grades == 0:
            return 0.0
        return round(sum_grades / count_grades, 2)

    def __str__(self):
        # собираю всю инфу о студенте в одну красивую многострочную __str__
        lines = []
        lines.append(f"Имя: {self.name}")
        lines.append(f"ID: {self.id}")
        lines.append("Предметы и оценки:")
        for subject, grades in self.subjects.items():
            lines.append(f"  {subject}: {grades}")
        lines.append(f"Средний балл: {self.get_gpa()}")
        return "\n".join(lines)

def save_to_json(students: list[Student], filename: str):
    data = [] # готовлю список простых словарей
    for student in students:
        data.append({
            "name": student.name,
            "id": student.id,
            "subjects": student.subjects
        })
    # записывю всё это дело в файл с отступами и поддержкой кириллицы
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_from_json(filename: str) -> list:
    students = []
    with open(filename, "r", encoding="utf-8") as f: # обязатлеьно в utf-8, некоторое время не мог понять ошибку
        data = json.load(f) # прочитываю файл
        for item in data:
            # создал объект студента из данных файла
            student = Student(item["name"], item["id"])
            student.subjects = item["subjects"] # восстанавливаются его предметы
            students.append(student)
    return students

def main():
    # Создал студентов
    student1 = Student("Иван Иванов", 1)
    student2 = Student("Анна Петрова", 2)
    student3 = Student("Сергей Смирнов", 3)

    # Добавил предметы
    student1.add_subject("Математика")
    student1.add_subject("Физика")

    student2.add_subject("История")
    student2.add_subject("Литература")

    student3.add_subject("Информатика")
    student3.add_subject("Математика")

    # Добавил оценки
    student1.add_grade("Математика", 5)
    student1.add_grade("Математика", 4)
    student1.add_grade("Физика", 3)

    student2.add_grade("История", 5)
    student2.add_grade("История", 5)
    student2.add_grade("Литература", 4)

    student3.add_grade("Информатика", 5)
    student3.add_grade("Информатика", 5)
    student3.add_grade("Математика", 4)

    # Проверка обработки ошибок
    try:
        student1.add_grade("Химия", 5)          # Несуществующий предмет
    except KeyError as e:
        print("Ошибка:", e)

    try:
        student1.add_grade("Математика", 10)    # Некорректная оценка
    except ValueError as e:
        print("Ошибка:", e)

    try:
        student1.remove_subject("Биология")     # Удаление несуществующего предмета
    except KeyError as e:
        print("Ошибка:", e)

    # все в список сохраняю
    students = [student1, student2, student3]
    save_to_json(students, "students.json")

    # загружаю обратно, чтобы проверить что всё сохранилось корректно
    loaded_students = load_from_json("students.json")
    for student in loaded_students:
        print(student)

if __name__ == "__main__":
    main() 