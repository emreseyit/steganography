import random
from PIL import Image
from local_settings import EOF_MARKER, PROJECT_DIR


def generate_seed(key):
    seed = int.from_bytes(key.encode(), 'little')
    return seed


def decode_message(img, key):
    """
    Decodes a message from an image
    :param img: PIL Image object
    :param key: String key to generate the random sequence
    :return: Decoded message
    """
    width, height = img.size
    pixels = img.load()
    random.seed(generate_seed(key))

    positions = []
    for _ in range(width * height):
        rand_h = random.randint(0, height - 1)
        rand_w = random.randint(0, width - 1)
        positions.append((rand_w, rand_h))

    decoded_bits = ""
    for x, y in positions:
        if pixels[x, y] & 0b1 == 1:
            bit_pair = (pixels[x, y] >> 1) & 0b11
            decoded_bits += f"{bit_pair:02b}"

            if len(decoded_bits) % 8 == 0:
                byte = decoded_bits[-8:]
                if chr(int(byte, 2)) == EOF_MARKER:
                    break

    # Convert bits to characters
    message = ""
    for i in range(0, len(decoded_bits) - 8, 8):  # Exclude the last 8 bits (EOF marker)
        message += chr(int(decoded_bits[i:i + 8], 2))

    return message


def main():
    img_file_name = 'Lenna_encoded.png'
    img_path = PROJECT_DIR.joinpath('src/images/source', img_file_name)
    img = Image.open(img_path)

    key = input("Enter key to decode the message: ")
    message = decode_message(img, key)
    print("Decoded message:", message)


if __name__ == '__main__':
    main()
