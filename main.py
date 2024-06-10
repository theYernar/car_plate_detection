import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import pytesseract
import cv2

pytesseract.pytesseract.tesseract_cmd = r'PATH'

def open_img(img_path):
    carplate_img = cv2.imread(img_path)
    carplate_img = cv2.cvtColor(carplate_img, cv2.COLOR_BGR2RGB)
    return carplate_img

def carplate_extract(image, carplate_haar_cascade):
    carplate_rects = carplate_haar_cascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors=5)
    for x, y, w, h in carplate_rects:
        carplate_img = image[y+15:y+h-10, x+15:x+w-20]
    return carplate_img

def enlarge_img(image, scale_percent):
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized_image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    return resized_image

def process_image(img_path):
    try:
        carplate_img_rgb = open_img(img_path)
        carplate_haar_cascade = cv2.CascadeClassifier('PATH')
        
        carplate_extract_img = carplate_extract(carplate_img_rgb, carplate_haar_cascade)
        carplate_extract_img = enlarge_img(carplate_extract_img, 150)
        
        carplate_extract_img_gray = cv2.cvtColor(carplate_extract_img, cv2.COLOR_RGB2GRAY)
        
        plate_number = pytesseract.image_to_string(
            carplate_extract_img_gray,
            config='--psm 6 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        )

        display_image(carplate_extract_img)
        display_plate_number(plate_number)
    except Exception as e:
        messagebox.showerror("Ошибка", str(e))

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
    if file_path:
        process_image(file_path)

def display_image(image):
    image = Image.fromarray(image)
    image = ImageTk.PhotoImage(image)
    img_label.config(image=image)
    img_label.image = image

def display_plate_number(plate_number):
    plate_label.config(text="Распознанный номер авто: " + plate_number)

# Создание главного окна
root = tk.Tk()
root.title("Распознавание номеров авто")
root.geometry("700x600")

# Добавление кнопки для выбора файла
btn_select_file = tk.Button(root, text="Выбрать фото", command=select_file, font=("Arial", 14))
btn_select_file.pack(pady=20)

# Добавление метки для отображения изображения
img_label = tk.Label(root)
img_label.pack(pady=20)

# Добавление метки для отображения распознанного номерного знака
plate_label = tk.Label(root, text="", font=("Arial", 14))
plate_label.pack(pady=20)

# Запуск главного цикла
root.mainloop()
