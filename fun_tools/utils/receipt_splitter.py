import pytesseract
from PIL import Image
import re
import tkinter as tk
from tkinter import messagebox

class ReceiptSplitter:
    """
    영수증 이미지에서 금액을 추출하고, 인원수로 나누어 금액을 계산하는 GUI 프로그램 클래스.
    """
    def __init__(self):
        # Tesseract 경로 설정
        self.tesseract_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        pytesseract.pytesseract.tesseract_cmd = self.tesseract_path

        # Tkinter 메인 창 생성
        self.root = tk.Tk()
        self.root.title("영수증 나누기 계산기")

        # GUI 구성
        self.setup_gui()

    def setup_gui(self):
        """GUI 요소를 설정하는 메서드"""
        # 이미지 경로 입력
        tk.Label(self.root, text="이미지 경로:").grid(row=0, column=0, padx=10, pady=10)
        self.image_path_entry = tk.Entry(self.root, width=30)
        self.image_path_entry.grid(row=0, column=1, padx=10, pady=10)

        # 인원 수 입력
        tk.Label(self.root, text="인원 수:").grid(row=1, column=0, padx=10, pady=10)
        self.num_people_entry = tk.Entry(self.root, width=10)
        self.num_people_entry.grid(row=1, column=1, padx=10, pady=10)

        # 실행 버튼
        calculate_button = tk.Button(self.root, text="계산하기", command=self.calculate)
        calculate_button.grid(row=2, column=0, columnspan=2, pady=20)

    def extract_total_amount_from_image(self, image_path):
        """
        이미지에서 금액을 추출하여 반환하는 메서드.
        이미지에서 쉼표가 포함된 금액을 찾고 가장 큰 값을 반환합니다.
        """
        try:
            # 이미지 열기
            img = Image.open(image_path)

            # pytesseract로 텍스트 추출
            result = pytesseract.image_to_string(img, lang='kor')

            # 쉼표가 포함된 금액 추출
            numbers_with_commas = re.findall(r'\d{1,3}(?:,\d{3})*', result)
            numbers = [int(num.replace(',', '')) for num in numbers_with_commas]

            return max(numbers) if numbers else None
        except Exception as e:
            messagebox.showerror("에러", f"이미지 처리 중 오류 발생: {e}")
            return None

    def calculate(self):
        """
        이미지 경로와 인원 수를 받아 계산 결과를 GUI로 출력하는 메서드.
        """
        image_path = self.image_path_entry.get()
        try:
            num_people = int(self.num_people_entry.get())
            if num_people <= 0:
                messagebox.showerror("에러", "인원 수는 1명 이상이어야 합니다.")
                return

            total_amount = self.extract_total_amount_from_image(image_path)

            if total_amount is not None:
                # 1인당 금액 계산
                amount_per_person = total_amount / num_people

                # 금액 포맷팅
                formatted_total = f"{total_amount:,} 원"
                formatted_per_person = f"{amount_per_person:,.0f} 원"

                # 결과 출력
                result_text = f"총 금액: {formatted_total}\n1인당 금액: {formatted_per_person}"
                messagebox.showinfo("계산 결과", result_text)
            else:
                messagebox.showerror("에러", "유효한 금액을 추출할 수 없습니다.")
        except ValueError:
            messagebox.showerror("에러", "유효한 숫자를 입력하세요.")

    def run(self):
        """Tkinter 메인 루프 실행"""
        self.root.mainloop()
