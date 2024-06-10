from PIL import Image
from local_settings import EOF_MARKER, PROJECT_DIR


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


def main():
    img_file_name = 'Lenna.png'
    img_path = PROJECT_DIR.joinpath('src/images/source', img_file_name)
    img = Image.open(img_path)

    msg = input("Enter message to be encoded: ")

    encoded_img = embed_message(img, msg)

    encoded_img.save(PROJECT_DIR.joinpath('src/images/source', 'Lenna_encoded.png'))




if __name__ == '__main__':
    main()
