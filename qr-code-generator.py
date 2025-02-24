import streamlit as st
import qrcode
import cv2
import tempfile
import io  # For handling image bytes

# Function to generate QR Code
def generate_qr_code(text):
    qr = qrcode.QRCode(
        version=1, 
        error_correction=qrcode.constants.ERROR_CORRECT_L, 
        box_size=10, 
        border=4
    )
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')  # Returns a PIL Image
    return img

# Function to scan QR Code
def scan_qr_code(image_path):
    img = cv2.imread(image_path)
    detector = cv2.QRCodeDetector()
    data, _, _ = detector.detectAndDecode(img)
    return data if data else "No QR Code detected"

# Streamlit App
st.title("QR Code Generator and Scanner")

# QR Code Generator
st.header("Generate QR Code")
text_input = st.text_input("Enter text to generate QR Code:")

if st.button("Generate"):
    if text_input:
        qr_img = generate_qr_code(text_input)

        # Convert PIL Image to BytesIO
        img_bytes = io.BytesIO()
        qr_img.save(img_bytes, format="PNG")  # Save as PNG
        img_bytes.seek(0)  # Reset file pointer

        # Display the QR code
        st.image(img_bytes, caption="Generated QR Code", use_column_width=True)

        # Provide a download button
        st.download_button("Download QR Code", img_bytes, "qr_code.png", "image/png")
    else:
        st.warning("Please enter text to generate a QR code.")

# QR Code Scanner
st.header("Scan QR Code")
uploaded_file = st.file_uploader("Upload a QR Code image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
        temp_file.write(uploaded_file.getvalue())
        temp_file_path = temp_file.name
    
    scanned_data = scan_qr_code(temp_file_path)
    
    # Display uploaded image
    st.image(uploaded_file, caption="Uploaded QR Code", use_column_width=True)

    # Show scanned data
    if scanned_data == "No QR Code detected":
        st.error(scanned_data)
    else:
        st.success(f"Scanned Data: {scanned_data}")
