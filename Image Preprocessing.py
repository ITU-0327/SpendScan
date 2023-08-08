import cv2
import pytesseract
import re


def denoise(image):
    return cv2.fastNlMeansDenoising(image, None, 10, 7, 21)


def adaptive(image):
    return cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)


def resize(image):
    height, width = image.shape
    new_width = 1000
    aspect_ratio = width / height
    new_height = int(new_width / aspect_ratio)
    return cv2.resize(image, (new_width, new_height))


def preprocess_image(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    image = resize(image)
    cv2.imshow('Original Image', image)
    # text = pytesseract.image_to_string(image)
    # print('Original Image:\n' + text + '\n\n')

    image = denoise(image)
    cv2.imshow('Denoise Image', image)
    # text = pytesseract.image_to_string(image)
    # print('Denoise Image:\n' + text + '\n\n')

    # image = adaptive(image)
    # cv2.imshow('Adaptive Image', image)
    # text = pytesseract.image_to_string(image)
    # print('Adaptive Image:\n' + text + '\n\n')

    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return image


def extract_text_from_image(image_path):
    image = preprocess_image(image_path)
    text = pytesseract.image_to_string(image, config='--psm 6 -l eng')
    return text


image_path = r"Image\Woolworths 4.jpg"
text = extract_text_from_image(image_path)
print(text)


def extract_items(text):
    item_pattern = re.compile(r'(?:#|\*|\)|\}|[^a-zA-Z0-9])*([\w\s]+)\s+(\d+[\.,]\d{2})')

    items = []
    for line in text.split('\n'):
        match = item_pattern.search(line)
        if match:
            item_name = match.group(1).strip()
            # Convert comma to period for price
            item_price = match.group(2).replace(',', '.')
            items.append({'name': item_name, 'price': item_price})

    return items


def parse_receipt(text):
    lines = text.split('\n')

    # Store Name & Info
    store_name = lines[0] if len(lines) > 0 else None
    store_info = ' '.join(lines[1:4]) if len(lines) > 3 else None

    items = extract_items(text)

    # Subtotal, Cash, and Change
    subtotal = re.search(r'SUBTOTAL\s+(\$\d+\.\d{2})', text)
    subtotal = subtotal.group(1) if subtotal else None

    cash = re.search(r'Cash\s+(\$\d+\.\d{2})', text)
    cash = cash.group(1) if cash else None

    change = re.search(r'Change\s+(\$\d+\.\d{2})', text)
    change = change.group(1) if change else None

    # GST
    gst = re.search(r'TOTAL includes GST\s+(\$\d+\.\d{2})', text)
    gst = gst.group(1) if gst else None

    return {
        'store_name': store_name,
        'store_info': store_info,
        'items': items,
        'subtotal': subtotal,
        'cash': cash,
        'change': change,
        'gst': gst
    }


parsed_data = parse_receipt(text)
print("Data: \n", parsed_data)
