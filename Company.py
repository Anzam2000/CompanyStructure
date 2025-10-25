import tkinter as tk
from tkinter import messagebox, scrolledtext


class Employee:
    """Класс сотрудника"""

    def __init__(self, name, position):
        self.name = name
        self.position = position
        self.left = None
        self.right = None


class CompanyStructure:
    """Организационная структура компании"""

    def __init__(self):
        self.root = None

    def add_employee(self, name, position, boss_name=None, is_left=True):
        """
        Добавление сотрудника

        Args:
            name: имя сотрудника
            position: должность
            boss_name: имя начальника (None для CEO)
            is_left: True - левый подчиненный, False - правый
        """
        new_employee = Employee(name, position)

        if self.root is None:
            self.root = new_employee
            return f"Добавлен CEO: {name} - {position}"

        boss = self._find_employee(self.root, boss_name)
        if boss is None:
            return f"Ошибка: Начальник {boss_name} не найден"

        if is_left:
            if boss.left is None:
                boss.left = new_employee
                return f"Добавлен левый подчиненный: {name} - {position} (начальник: {boss_name})"
            else:
                return f"Ошибка: Левый слот у {boss_name} уже занят"
        else:
            if boss.right is None:
                boss.right = new_employee
                return f"Добавлен правый подчиненный: {name} - {position} (начальник: {boss_name})"
            else:
                return f"Ошибка: Правый слот у {boss_name} уже занят"

    def _find_employee(self, current, name):
        """Поиск сотрудника по имени"""
        if current is None:
            return None

        if current.name == name:
            return current

        left_result = self._find_employee(current.left, name)
        if left_result is not None:
            return left_result

        right_result = self._find_employee(current.right, name)
        return right_result

    def show_structure(self, employee=None, level=0):
        """Показать организационную структуру"""
        if employee is None:
            employee = self.root
        if employee is None:
            return "Структура пуста"

        result = []

        def _build_structure(emp, lvl):
            indent = "  " * lvl
            result.append(f"{indent}└─ {emp.name} - {emp.position}")

            if emp.left:
                _build_structure(emp.left, lvl + 1)
            if emp.right:
                _build_structure(emp.right, lvl + 1)

        _build_structure(employee, level)
        return "\n".join(result)

    def get_subordinates(self, boss_name):
        """Получить список подчиненных"""
        boss = self._find_employee(self.root, boss_name)
        if boss is None:
            return []

        subordinates = []
        if boss.left:
            subordinates.append(boss.left.name)
        if boss.right:
            subordinates.append(boss.right.name)

        return subordinates


company = CompanyStructure()
company.add_employee("Иван Петров", "CEO")
company.add_employee("Мария Сидорова", "CTO", "Иван Петров", is_left=True)
company.add_employee("Алексей Козлов", "CFO", "Иван Петров", is_left=False)

root = tk.Tk()
root.title("Организационная структура компании")
root.geometry("500x300")

is_left_var = tk.BooleanVar(value=True)


def add_employee():
    name = entry_name.get().strip()
    position = entry_position.get().strip()
    boss = entry_boss.get().strip()
    is_left = is_left_var.get()

    if not name or not position:
        messagebox.showerror("Ошибка", "Введите имя и должность сотрудника!")
        return
    if not boss and company.root is not None:
        messagebox.showerror("Ошибка", "Для не-CEO сотрудника укажите начальника!")
        return

    result = company.add_employee(name, position, boss if boss else None, is_left)
    messagebox.showinfo("Результат", result)

    # Очищаем поля ввода
    entry_name.delete(0, tk.END)
    entry_position.delete(0, tk.END)
    if company.root is not None:
        entry_boss.delete(0, tk.END)


def show_structure():
    structure_text = company.show_structure()
    structure_window = tk.Toplevel(root)
    structure_window.title("Организационная структура")
    structure_window.geometry("400x300")

    text_area = scrolledtext.ScrolledText(structure_window, width=45, height=25, font=("Courier New", 10))
    text_area.pack(padx=10, pady=10)
    text_area.insert(tk.END, structure_text)
    text_area.config(state=tk.DISABLED)


def show_subordinates():
    boss_name = entry_boss.get().strip()
    if not boss_name:
        messagebox.showerror("Ошибка", "Введите имя начальника!")
        return

    subordinates = company.get_subordinates(boss_name)
    if subordinates:
        messagebox.showinfo(f"Подчиненные {boss_name}", "\n".join(subordinates) if subordinates else "Нет подчиненных")
    else:
        messagebox.showwarning("Внимание", f"Сотрудник {boss_name} не найден или не имеет подчиненных")


frame_input = tk.Frame(root)
frame_input.pack(pady=10)

tk.Label(frame_input, text="Имя сотрудника:", font=("Arial", 12)).grid(row=0, column=0, sticky="w", pady=5)
entry_name = tk.Entry(frame_input, width=30, font=("Arial", 12))
entry_name.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_input, text="Должность:", font=("Arial", 12)).grid(row=1, column=0, sticky="w", pady=5)
entry_position = tk.Entry(frame_input, width=30, font=("Arial", 12))
entry_position.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_input, text="Начальник:", font=("Arial", 12)).grid(row=2, column=0, sticky="w", pady=5)
entry_boss = tk.Entry(frame_input, width=30, font=("Arial", 12))
entry_boss.grid(row=2, column=1, padx=5, pady=5)

tk.Label(frame_input, text="Позиция:", font=("Arial", 12)).grid(row=3, column=0, sticky="w", pady=5)
frame_radio = tk.Frame(frame_input)
frame_radio.grid(row=3, column=1, padx=5, pady=5)

tk.Radiobutton(frame_radio, text="Левый подчиненный", variable=is_left_var, value=True).pack(side=tk.LEFT)
tk.Radiobutton(frame_radio, text="Правый подчиненный", variable=is_left_var, value=False).pack(side=tk.LEFT)

# Кнопки
frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=20)

btn_add = tk.Button(
    frame_buttons,
    text="Добавить сотрудника",
    command=add_employee,
    bg="lightgreen",
    width=20,
    height=2
)
btn_add.pack(side=tk.LEFT, padx=5)

btn_show_structure = tk.Button(
    frame_buttons,
    text="Показать структуру",
    command=show_structure,
    bg="lightblue",
    width=20,
    height=2
)
btn_show_structure.pack(side=tk.LEFT, padx=5)

btn_show_subordinates = tk.Button(
    frame_buttons,
    text="Показать подчиненных",
    command=show_subordinates,
    bg="lightyellow",
    width=20,
    height=2
)
btn_show_subordinates.pack(side=tk.LEFT, padx=5)

help_label = tk.Label(root, text="Примечание: для CEO оставьте поле 'Начальник' пустым",
                      font=("Arial", 10), fg="gray")
help_label.pack(pady=10)

root.mainloop()
