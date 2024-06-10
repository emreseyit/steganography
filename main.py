from pathlib import Path
from PIL import Image

PROJECT_DIR = Path(__file__).resolve().parent

EOF_MARKER = "\0"


def encode_message(msg):
    """
    Encodes a message to binary
    :param msg: String to be encoded
    :return: Encoded message as list of 2 bits
    """
    msg += EOF_MARKER  # Append EOF marker to the message
    msg_bits = ''.join(format(ord(char), '08b') for char in msg)
    enc_msg = [int(msg_bits[i:i + 2], 2) for i in range(0, len(msg_bits), 2)]
    return enc_msg


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


def embed_message(img, msg):
    encoded_msg = encode_message(msg)
    width, height = img.size
    pixels = img.load()
    msg_len = len(encoded_msg)
    if msg_len > width * height:
        raise ValueError("Message is too long to encode in this image.")

    index = 0
    for h in range(height):
        if index >= msg_len:
            break
        for w in range(width):
            if index >= msg_len:
                break
            pixel = pixels[w, h]
            pixel = (pixel & ~0b11) | encoded_msg[index]
            pixels[w, h] = pixel
            index += 1
    return img


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
    img_file_name = 'Lenna.png'
    img_path = PROJECT_DIR.joinpath('src/images/source', img_file_name)
    img = Image.open(img_path)

    msg = 'Hello World!'  # TODO: Make this input

    encoded_img = embed_message(img, msg)

    encoded_img.save(PROJECT_DIR.joinpath('src/images/source', 'Lenna_encoded.png'))

    print(extract_message(encoded_img))


if __name__ == '__main__':
    main()
