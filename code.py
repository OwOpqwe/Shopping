
import streamlit as st
import smtplib
from email.mime.text import MIMEText

st.set_page_config(page_title="Online Store", layout="wide")

st.markdown(
    """
    <style>
    .stApp {
        background-color: #000000;
        color: #ffffff;
    }
    div.stButton > button {
        background-color: #000000;
        color: #ffffff;
        border: 1px solid #ffffff;
    }
    div.stButton > button:hover {
        background-color: #28a745 !important;
        color: white !important;
    }
    .element-container img {
        border-radius: 15px;
        border: 4px solid white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Welcome to the Online Store")
st.markdown("<h1 style='color:red; text-align:center;'>🚫 NO REFUNDS 🚫</h1>", unsafe_allow_html=True)

OWNER_EMAIL = "charlie2011.ting@gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465
SMTP_USER = "youremail@gmail.com"
SMTP_PASSWORD = "your_app_password"

products = {
    "Chicken Noodle Snacks": {
        "price": 17,
        "img": "https://example.com/chicken_noodle_snack.jpg",
        "description": "Tasty and convenient chicken noodle snacks."
    },
    "Dr Pepper": {
        "price": 37,
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cc/Dr_Pepper_Dose_2024.jpg/250px-Dr_Pepper_Dose_2024.jpg",
        "description": "Refreshing soda drink."
    },
    "Snack & Drink Bundle": {
        "price": 50,
        "img": "https://example.com/bundle.jpg",
        "description": "1 Chicken Noodle Snack + 1 Dr Pepper bundle deal."
    }
}

if "cart" not in st.session_state:
    st.session_state.cart = []
if "ratings" not in st.session_state:
    st.session_state.ratings = []
if "show_rating" not in st.session_state:
    st.session_state.show_rating = False
if "buyer_name" not in st.session_state:
    st.session_state.buyer_name = ""
if "buyer_email" not in st.session_state:
    st.session_state.buyer_email = ""
if "buyer_notes" not in st.session_state:
    st.session_state.buyer_notes = ""

def send_order_email(cart, total, buyer_name, buyer_email, buyer_notes):
    order_details = "\n".join([f"- {item['name']} (NT${item['price']})" for item in cart])
    notes_text = f"\n\nBuyer Notes:\n{buyer_notes}" if buyer_notes.strip() else ""
    owner_msg = MIMEText(f"New order received!\n\nBuyer: {buyer_name}\nEmail: {buyer_email}\n\nOrder Details:\n{order_details}\n\nTotal: NT${total}{notes_text}")
    owner_msg["Subject"] = f"New Order from {buyer_name}"
    owner_msg["From"] = SMTP_USER
    owner_msg["To"] = OWNER_EMAIL
    buyer_msg = MIMEText(f"Hi {buyer_name},\n\nThank you for your purchase!\n\nYour Order:\n{order_details}\n\nTotal: NT${total}{notes_text}\n\nPlease prepare cash upon delivery or pickup.\n\n🚫 NO REFUNDS 🚫")
    buyer_msg["Subject"] = "Your Order Confirmation"
    buyer_msg["From"] = SMTP_USER
    buyer_msg["To"] = buyer_email
    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(owner_msg)
            server.send_message(buyer_msg)
        st.success("✅ Order emails sent successfully!")
    except Exception as e:
        st.error(f"Failed to send emails: {e}")

st.sidebar.header("Your Cart")
st.sidebar.subheader("Buyer Information")
st.session_state.buyer_name = st.sidebar.text_input("Your Name", value=st.session_state.buyer_name)
st.session_state.buyer_email = st.sidebar.text_input("Your Email", value=st.session_state.buyer_email)
st.session_state.buyer_notes = st.sidebar.text_area("Any special instructions?", value=st.session_state.buyer_notes)
products_per_row = st.sidebar.slider("Products per row (set 1 for mobile)", min_value=1, max_value=4, value=2)

if not st.session_state.cart:
    st.sidebar.info("Your cart is empty.")
else:
    total = sum(item["price"] for item in st.session_state.cart)
    for i, item in enumerate(st.session_state.cart):
        st.sidebar.write(f"- {item['name']} (NT${item['price']})")
        if st.sidebar.button(f"Remove {i+1}", key=f"remove_{i}"):
            st.session_state.cart.pop(i)
            st.experimental_rerun()
    st.sidebar.write(f"**Total: NT${total}**")
    if not st.session_state.buyer_name.strip() or not st.session_state.buyer_email.strip():
        st.sidebar.warning("Please enter your name and email before completing purchase.")
    elif st.sidebar.button("Complete Purchase"):
        send_order_email(st.session_state.cart, total, st.session_state.buyer_name, st.session_state.buyer_email, st.session_state.buyer_notes)
        st.sidebar.success("🎉 Order sent successfully!")
        st.session_state.cart = []
        st.session_state.show_rating = True

st.header("Products")

st.markdown(
    """
    <div style="
        background-color: #ffeb3b; 
        color: black; 
        padding: 15px; 
        border: 2px solid white; 
        border-radius: 10px; 
        text-align: center; 
        font-size: 24px; 
        font-weight: bold;
        margin-bottom: 20px;">
        💵 Cash Only — No Card Payments
    </div>
    """,
    unsafe_allow_html=True
)

product_names = list(products.keys())

for i in range(0, len(product_names), products_per_row):
    cols = st.columns(products_per_row)
    for j, product_name in enumerate(product_names[i:i+products_per_row]):
        product = products[product_name]
        with cols[j]:
            st.subheader(product_name)
            st.image(product["img"], width=200)
            st.write(product["description"])
            st.write(f"Price: NT${product['price']}")
            if st.button(f"Add {product_name} to Cart", key=f"add_{product_name}"):
                st.session_state.cart.append({"name": product_name, "price": product["price"]})
                st.success(f"✅ Added {product_name} to cart!")

if st.session_state.show_rating:
    with st.expander("Rate Our Store"):
        rating = st.slider("Please rate your shopping experience (1–5 stars):", 1, 5, 5)
        if st.button("Submit Rating"):
            st.session_state.ratings.append(rating)
            st.success(f"Thank you for rating us {rating}⭐!")
            st.session_state.show_rating = False

if st.session_state.ratings:
    avg = sum(st.session_state.ratings) / len(st.session_state.ratings)
    st.sidebar.info(f"⭐ Average Rating: {avg:.1f}/5 ({len(st.session_state.ratings)} ratings)")
