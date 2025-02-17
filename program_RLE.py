import tkinter as tk
from tkinter import StringVar

# Функція для RLE-кодування переданих даних
def rle_encode(data):
    encoded = bytearray()
    i = 0
    while i < len(data):
        run_length = 1
        while i + run_length < len(data) and data[i] == data[i + run_length] and run_length < 129:
            run_length += 1

        if run_length > 1:
            encoded.append(128 + (run_length - 2))
            encoded.append(data[i])
            i += run_length
        else:
            start = i
            while (i + 1 < len(data) and data[i] != data[i + 1]) and (i - start < 128):
                i += 1
            if i - start == 0:
                i += 1
            encoded.append(i - start - 1)
            encoded.extend(data[start:i])

    return encoded

# Функція для розпакування RLE-кодованих даних
def rle_decode(data):
    decoded = bytearray()
    i = 0
    while i < len(data):
        if i >= len(data):
            return decoded, f"Error: Unexpected end of file at position {i}"
        
        flag = data[i]
        i += 1

        if flag & 128:  # Повторювана послідовність         
            run_length = (flag & 127) + 2
            if i >= len(data):
                return decoded, f"Error: Missing byte to repeat at position {i}"
            
            if not (32 <= data[i] <= 126 or data[i] in (10, 13)):
                return decoded, f"Error: Missing byte to repeat at position {i}"
            
            decoded.extend([data[i]] * run_length)
            i += 1
        else:  # Унікальна послідовність
            if i + flag + 1 > len(data):
                return decoded, f"Error: Incorrect unique block length at position {i-1}"
            
            for byte in data[i:i + flag + 1]:
                if not (32 <= byte <= 126 or byte in (10, 13)):
                    return decoded, f"Error: Incorrect unique block length at position {i}"
            
            decoded.extend(data[i:i + flag + 1])
            i += flag + 1
    return decoded, None

def encode():
    input_file_name = input_file.get("1.0", tk.END).strip()
    output_file_name = output_file.get("1.0", tk.END).strip()
    
    with open(input_file_name, "rb") as f:
        data = f.read()
        
    result = rle_encode(data)
    print(result)
    output_file_name = output_file_name if output_file_name else input_file_name + ".rle"
    
    with open(output_file_name, "wb") as f:
        f.write(result)

    result_var.delete("1.0", tk.END)
    result_var.insert(tk.END, f"Process completed. Output file: {output_file_name}")

def decode():
    input_file_name = input_file.get("1.0", tk.END).strip()
    output_file_name = output_file.get("1.0", tk.END).strip()
    
    with open(input_file_name, "rb") as f:
        data = f.read()
        
    result = rle_decode(data)
    output_file_name = output_file_name if output_file_name else input_file_name.replace(".rle", "")
    
    with open(output_file_name, "wb") as f:
        f.write(result[0])
        
    result_var.delete("1.0", tk.END)
    if result[1] == None:
        result_var.insert(tk.END, f"Process completed. Output file: {output_file_name}")
    else:
        result_var.insert(tk.END, f"{result[1]}. Output file: {output_file_name}")

def clear():
    # Очистити поля вводу та результату
    input_file.delete(1.0, tk.END)
    output_file.delete(1.0, tk.END)
    result_var.delete(1.0, tk.END)

#-----------------------------Головне вікно-----------------------------

# Створення головного вікна
master = tk.Tk()
master.title("RLE")

# Введення для першого шістнадцяткового числа
label1 = tk.Label(master, text="Input file:")
label1.grid(row=0, column=0)

input_file = tk.Text(master, height=2, width=80)
input_file.grid(row=0, column=1)

# Введення для другого шістнадцяткового числа
label2 = tk.Label(master, text="Output file (optional):")
label2.grid(row=1, column=0)

output_file = tk.Text(master, height=2, width=80)
output_file.grid(row=1, column=1)

# Виведення результату
result_label = tk.Label(master, text="Result:")
result_label.grid(row=2, column=0)

result_var = tk.Text(master, height=2, width=80)
result_var.grid(row=2, column=1)

# Фрейм для кнопок
button_frame = tk.Frame(master)
button_frame.grid(row=3, column=0, columnspan=4, pady=10)

# Кнопки операцій
buttons = [
    ("Encode", encode),
    ("Decode", decode),
]

# Розташування кнопок у два стовпці
for i, (text, command) in enumerate(buttons):
    row, col = divmod(i, 2)
    btn = tk.Button(button_frame, text=text, command=command, width=20)
    btn.grid(row=row, column=col, padx=5, pady=5)

# Кнопка "Clear"
clear_button = tk.Button(master, text="Clear", command=clear, width=20, bg="red", fg="white")
clear_button.grid(row=4, column=0, columnspan=4, pady=10)

master.mainloop()
