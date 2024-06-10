from local_settings import EOF_MARKER, PROJECT_DIR
from PIL import Image


def decode_message(bits):
    encode_length = 2
    byte_size = 8
    bit_str = ''.join([format(b, '02b') for b in bits])
    msg = ''
    for i in range(0, len(bit_str), byte_size):
        byte = bit_str[i: i + byte_size]
        if len(byte) == byte_size:
            char = chr(int(byte, 2))
            if char == EOF_MARKER:
                break
            msg += char
    return msg


def extract_message(img):
    pixels = img.load()
    width, height = img.size
    bits = []

    for h in range(height):
        for w in range(width):
            pixel = pixels[w, h]
            bits.append(pixel & 0b11)

    return decode_message(bits)


def main():
    img = None
    while not img:
        try:
            img_file_name = input('Enter image file name: ') + "_encoded"
            file_extension = "." + (input('Enter image file extension (default: png): ') or "png")
            img_path = PROJECT_DIR.joinpath('src/images/source', img_file_name + file_extension)
            img = Image.open(img_path)
        except:
            print('Invalid image file name. Please try again.')

    print(extract_message(img))


if __name__ == '__main__':
    main()
