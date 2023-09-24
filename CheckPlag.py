import sys
import fitz  # PyMuPDF
import nltk
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon 
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QLabel, QFileDialog, QMessageBox

nltk.download('punkt')

class PlagiarismCheckerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 700, 400)
        self.setWindowTitle("Plagiarism Checker in Python")
        self.setWindowIcon(QIcon("logo.png"))

        self.file1_text = QTextEdit(self)
        self.file1_text.setGeometry(20, 20, 650, 100)

        self.file2_text = QTextEdit(self)
        self.file2_text.setGeometry(20, 140, 650, 100)

        self.load_file1_button = QPushButton("Load File 1", self)
        self.load_file1_button.setGeometry(50, 260, 100, 30)
        self.load_file1_button.clicked.connect(self.load_file1)
        self.load_file1_button.setStyleSheet("background-color: #4CAF50; color: white; border: 1px solid #45a049;")

        self.load_file2_button = QPushButton("Load File 2", self)
        self.load_file2_button.setGeometry(500, 260, 100, 30)
        self.load_file2_button.clicked.connect(self.load_file2)
        self.load_file2_button.setStyleSheet("background-color: #4CAF50; color: white; border: 1px solid #45a049;")

        self.check_button = QPushButton("Check Plagiarism", self)
        self.check_button.setGeometry(260, 260, 120, 30)
        self.check_button.clicked.connect(self.check_plagiarism)
        self.check_button.setStyleSheet("background-color: #008CBA; color: white; border: 1px solid #0077A6;")
        self.check_button.setCursor(Qt.PointingHandCursor)

        self.clear_button = QPushButton("Clear", self)
        self.clear_button.setGeometry(400, 320, 100, 30)
        self.clear_button.clicked.connect(self.clear_text)
        self.clear_button.setStyleSheet("background-color: #f44336; color: white; border: 1px solid #d32f2f;")
        self.clear_button.setCursor(Qt.PointingHandCursor)

        self.exit_button = QPushButton("Exit", self)
        self.exit_button.setGeometry(140, 320, 100, 30)
        self.exit_button.clicked.connect(self.close)
        self.exit_button.setStyleSheet("background-color: #607D8B; color: white; border: 1px solid #546E7A;")
        self.exit_button.setCursor(Qt.PointingHandCursor)

        self.result_label = QLabel(self)
        self.result_label.setGeometry(20, 340, 360, 30)

    def load_file1(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File 1", "", "Text Files (*.txt);;PDF Files (*.pdf)", options=options)
        if file_path:
            if file_path.endswith(".pdf"):
                text = self.extract_text_from_pdf(file_path)
            else:
                with open(file_path, 'r') as file:
                    text = file.read()
            self.file1_text.setPlainText(text)

    def load_file2(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File 2", "", "Text Files (*.txt);;PDF Files (*.pdf)", options=options)
        if file_path:
            if file_path.endswith(".pdf"):
                text = self.extract_text_from_pdf(file_path)
            else:
                with open(file_path, 'r') as file:
                    text = file.read()
            self.file2_text.setPlainText(text)

    def extract_text_from_pdf(self, pdf_file):
        pdf_text = ""
        doc = fitz.open(pdf_file)
        for page_num in range(len(doc)):
            page = doc[page_num]
            pdf_text += page.get_text()
        return pdf_text

    def check_plagiarism(self):
        text1 = self.file1_text.toPlainText()
        text2 = self.file2_text.toPlainText()

        if not text1 or not text2:
            QMessageBox.warning(self, "Warning", "Please load both files.")
            return

        # Tokenize the text
        words1 = text1.split()
        words2 = text2.split()

        # Calculate word overlap
        common_words = set(words1) & set(words2)
        similarity_percentage = (len(common_words) / len(set(words1))) * 100

        # Show the result in a popup
        QMessageBox.information(self, "Plagiarism Result", f"Similarity: {similarity_percentage:.2f}%")

    def clear_text(self):
        self.file1_text.clear()
        self.file2_text.clear()
        self.result_label.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PlagiarismCheckerApp()
    window.show()
    sys.exit(app.exec_())
