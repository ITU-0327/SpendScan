from image_processor import ImageProcessor
import pytesseract
import re
import json


def preprocess_image(image_path):
    image = ImageProcessor(image_path)
    image.resize()
    # image.show_image('Original receipts_training')
    # text = pytesseract.image_to_string(image)
    # print('Original receipts_training:\n' + text + '\n\n')

    image.denoise()
    image.show_image('Denoise receipts_training')
    # text = pytesseract.image_to_string(image)
    # print('Denoise receipts_training:\n' + text + '\n\n')

    # image.adaptive()
    # image.show_image('Adaptive receipts_training')
    # text = pytesseract.image_to_string(image)
    # print('Adaptive receipts_training:\n' + text + '\n\n')

    return image


def extract_text_from_image(image_path):
    processed_image = preprocess_image(image_path)
    text = pytesseract.image_to_string(processed_image.image, config='--psm 6 -l eng')
    return text


image_path = r"receipts_training\Woolworths 4.jpg"
text = extract_text_from_image(image_path)
print(text)


def extract_items(text):
    item_pattern = re.compile(r'^(?:[^a-zA-Z]+)?([a-zA-Z].+?)\s+(\d+[\.,]\d{2})')

    items = []
    for line in text.split('\n'):
        match = item_pattern.search(line)
        if match:
            item_name = match.group(1).strip()
            item_name = re.sub(r'(\d+)9\b', r'\1g', item_name)
            # Convert comma to period for price
            item_price = match.group(2).replace(',', '.')
            items.append({'name': item_name, 'price': item_price})

    return items


def parse_receipt(text):
    lines = text.split('\n')

    # Store Name & Info
    store_name = re.sub(r'[^a-zA-Z\s]', '', lines[0]).strip() if len(lines) > 0 else None
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
data = json.dumps(parsed_data, indent=3)
print("Data: \n", data)