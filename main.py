from pathlib import Path
from PIL import Image

PROJECT_DIR = Path(__file__).resolve().parent


def encode_message(msg):
    """
    Encodes a message to base64
    :param msg: String to be encoded
    :return: Encoded message as list of 2 bits
    """
    msg_bits = ''.join(format(ord(char), '08b') for char in msg)
    enc_msg = [int(msg_bits[i:i+2]) for i in range(0, len(msg_bits), 2)]
    return enc_msg


def decode_message(bits):
    encode_length = 2
    byte_size = 8
    item_count_per_char = byte_size//encode_length
    bit_str = ''.join([str(b) for b in bits])
    msg = ''
    for i in range(0, encode_length, 8):
        byte = bit_str[i: i + 8]
        if len(byte) == 8:
            print(int(byte))
            msg += chr(int(byte))
    return msg


def embed_message(img, msg):
    encoded_msg = encode_message(msg)
    height, width = img.size
    pixels = img.load()
    for h in range(height):
        is_msg_limit_reached = False
        for w in range(width):
            current_index = h * width + w
            pixel = pixels[h, w]
            pixel = (pixel & ~0b11) | encoded_msg[current_index]
            pixels[h, w] = pixel
            if current_index + 1 == len(encoded_msg):
                is_msg_limit_reached = True
                break
        if is_msg_limit_reached:
            break
    return img


def extract_message(img):
    pixels = img.load()
    height, width = img.size
    bits = []

    for h in range(height):
        for w in range(width):
            pixel = pixels[h, w]
            bits.append(pixel & ~0b11)

    return decode_message(bits)


def main():
    img_file_name = 'Lenna.png'
    img_path = PROJECT_DIR.joinpath('src/images/source', img_file_name)
    img = Image.open(img_path)

    msg = 'Hello World!'  # TODO: Make this input

    encoded_img = embed_message(img, msg)

    # encoded_img.show()

    print(extract_message(encoded_img))


if __name__ == '__main__':
    main()
