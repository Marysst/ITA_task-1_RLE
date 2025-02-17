# Не спортворенний рядок  \x81a\x80b\x03cdef\x81c\x80a\x00e\x00f

# Файл input-3.txt.rle загубили символ с, замість \x81c\ маємо \x81\
with open('input-3.txt.rle', 'wb') as f: f.write(bytearray(b'\x81a\x80b\x03cdef\x81\x80a\x00e\x00f'))

# Файл input-4.txt.rle загубили символ с, замість \x03cdef\ маємо \x03cde\
with open('input-4.txt.rle', 'wb') as f: f.write(bytearray(b'\x81a\x80b\x03cde\x81c\x80a\x00e\x00f'))
