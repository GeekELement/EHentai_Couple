import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QVBoxLayout, QWidget, QLabel, QProgressBar, QHBoxLayout
from PyQt5.QtCore import Qt
from reportlab.pdfgen import canvas
from PIL import Image
import os

class ImageToPdfConverter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.folder_path = ''

    def initUI(self):
        self.setWindowTitle('图片转PDF工具')
        self.setGeometry(300, 300, 500, 300)

        # 设置进度条样式
        self.setStyleSheet("""
            QProgressBar {
                border: 1px solid gray;
                border-radius: 5px;
                text-align: center;
                height: 25px;
            }
            QProgressBar::chunk {
                background-color: gray;
                border-radius: 3px;
            }
            QPushButton {
                border: 1px solid gray;
                padding: 8px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: lightgray;
            }
        """)

        # 创建中央部件和布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # 创建文件夹路径显示标签
        self.path_label = QLabel('未选择文件夹')
        self.path_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.path_label)

        # 创建选择文件夹按钮
        select_btn = QPushButton('选择文件夹', self)
        select_btn.clicked.connect(self.select_folder)
        layout.addWidget(select_btn)

        # 创建开始转换按钮
        convert_btn = QPushButton('开始转换', self)
        convert_btn.clicked.connect(self.convert_to_pdf)
        layout.addWidget(convert_btn)

        # 创建进度条
        self.progress_bar = QProgressBar(self)
        layout.addWidget(self.progress_bar)

        # 创建状态标签
        self.status_label = QLabel('')
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)

        # 创建底部布局用于放置作者署名
        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()
        
        # 添加作者署名到右下角
        author_label = QLabel('作者：耑木菌')
        bottom_layout.addWidget(author_label)
        layout.addLayout(bottom_layout)

    def select_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, '选择文件夹')
        if folder_path:
            self.folder_path = folder_path
            self.path_label.setText(f'已选择: {folder_path}')

    def convert_to_pdf(self):
        if not self.folder_path:
            self.status_label.setText('请先选择文件夹！')
            return

        # 获取所有图片文件
        image_files = [f for f in os.listdir(self.folder_path) 
                      if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
        
        if not image_files:
            self.status_label.setText('所选文件夹中没有图片文件！')
            return

        # 设置进度条
        self.progress_bar.setMaximum(len(image_files))
        self.progress_bar.setValue(0)

        # 创建PDF文件
        output_path = os.path.join(self.folder_path, 'output.pdf')
        c = canvas.Canvas(output_path)

        for i, image_file in enumerate(image_files):
            img_path = os.path.join(self.folder_path, image_file)
            img = Image.open(img_path)
            
            # 设置PDF页面大小为图片大小
            img_width, img_height = img.size
            c.setPageSize((img_width, img_height))
            
            # 绘制图片
            c.drawImage(img_path, 0, 0, width=img_width, height=img_height)
            c.showPage()
            
            # 更新进度条
            self.progress_bar.setValue(i + 1)

        c.save()
        self.status_label.setText('转换完成！PDF文件已保存在选择的文件夹中。')

def main():
    app = QApplication(sys.argv)
    converter = ImageToPdfConverter()
    converter.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()