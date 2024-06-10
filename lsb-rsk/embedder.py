import random
from PIL import Image
from local_settings import EOF_MARKER, PROJECT_DIR


def generate_seed(key):
    seed = int.from_bytes(key.encode(), 'little')
    return seed


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


def embed_message(img, msg):
    encoded_msg = encode_message(msg)
    width, height = img.size
    pixels = img.load()
    msg_len = len(encoded_msg)
    if msg_len > width * height:
        raise ValueError("Message is too long to encode in this image.")

    for y in range(height):
        for x in range(width):
            pixels[x, y] = pixels[x, y] & ~0b1

    for i in range(msg_len):
        is_placed = False
        while not is_placed:
            rand_h = random.randint(0, height - 1)
            rand_w = random.randint(0, width - 1)
            if pixels[rand_h, rand_w] & 0b1 == 1:
                continue
            pixels[rand_w, rand_h] = encoded_msg[i] << 1 | 1
            is_placed = True
    return img


def main():
    img_file_name = 'Lenna.png'
    img_path = PROJECT_DIR.joinpath('src/images/source', img_file_name)
    img = Image.open(img_path)

    msg = input("Enter message to be encoded: ")
    key = input("Enter key: ")

    random.seed(generate_seed(key))

    encoded_img = embed_message(img, msg)

    encoded_img.save(PROJECT_DIR.joinpath('src/images/source', 'Lenna_encoded.png'))
    print("File saved successfully.")


if __name__ == '__main__':
    main()
