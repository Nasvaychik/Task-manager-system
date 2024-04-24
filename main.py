import sys
from PyQt5 import QtWidgets, QtGui, QtCore
import sqlite3

# Создание или подключение к базе данных
conn = sqlite3.connect('task_manager.db')
c = conn.cursor()

# Создание таблицы задач, если она не существует
c.execute('''CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY,
    name TEXT,
    description TEXT,
    priority INTEGER,
    completed BOOLEAN
)''')

# Главный класс приложения
class TaskManagerApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Диспетчер задач")
        self.layout = QtWidgets.QVBoxLayout()

        # Поле для ввода задачи
        self.task_name = QtWidgets.QLineEdit(self)
        self.task_name.setPlaceholderText("Название задачи")

        self.task_description = QtWidgets.QTextEdit(self)
        self.task_description.setPlaceholderText("Описание задачи")

        self.task_priority = QtWidgets.QSpinBox(self)
        self.task_priority.setRange(1, 5)
        self.task_priority.setValue(3)
        self.task_priority.setToolTip("1 - Low Priority, 5 - High Priority")

        # Кнопка для добавления задачи
        self.add_task_button = QtWidgets.QPushButton("Добавить задачу", self)
        self.add_task_button.clicked.connect(self.add_task)

        # Список задач
        self.task_list = QtWidgets.QListWidget(self)
        self.task_list.itemDoubleClicked.connect(self.mark_as_completed)

        self.layout.addWidget(self.task_name)
        self.layout.addWidget(self.task_description)
        self.layout.addWidget(self.task_priority)
        self.layout.addWidget(self.add_task_button)
        self.layout.addWidget(self.task_list)

        self.setLayout(self.layout)
        self.refresh_task_list()

    def add_task(self):
        name = self.task_name.text()
        description = self.task_description.toPlainText()
        priority = self.task_priority.value()

        if name.strip() == "":
            return

        c.execute("INSERT INTO tasks (name, description, priority, completed) VALUES (?, ?, ?, ?)", (name, description, priority, False))
        conn.commit()

        self.refresh_task_list()

    def mark_as_completed(self, item):
        task_id = item.data(QtCore.Qt.UserRole)
        c.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))
        conn.commit()

        self.refresh_task_list()

    def refresh_task_list(self):
        self.task_list.clear()

        # Получение всех задач и сортировка по приоритету
        c.execute("SELECT id, name, description, priority, completed FROM tasks WHERE completed = 0 ORDER BY priority DESC")
        tasks = c.fetchall()

        for task in tasks:
            item = QtWidgets.QListWidgetItem()
            item.setText(f"{task[1]} (Priority: {task[3]})")
            item.setData(QtCore.Qt.UserRole, task[0])
            self.task_list.addItem(item)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    task_manager = TaskManagerApp()
    task_manager.show()
    sys.exit(app.exec_())
