import streamlit as st

# --- Page Setup ---
st.set_page_config(page_title="Online Store", layout="wide")

# --- Styling ---
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
        border: 6px solid white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Title and Notices ---
st.title("Welcome to the Online Store")
st.markdown("<h1 style='color:red; text-align:center;'>🚫 NO REFUNDS 🚫</h1>", unsafe_allow_html=True)

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

# --- Product Data ---
products = {
    "Chicken Noodle Snacks": {
        "price": 17,
        "img": "https://images.cdn.saveonfoods.com/detail/00074410700799.jpg",
        "description": "Tasty and convenient chicken noodle snacks."
    },
    "Dr Pepper": {
        "price": 37,
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cc/Dr_Pepper_Dose_2024.jpg/250px-Dr_Pepper_Dose_2024.jpg",
        "description": "Refreshing soda drink."
    },
    "Snack & Drink Bundle": {
        "price": 50,
        "img": None,
        "description": "1 Chicken Noodle Snack + 1 Dr Pepper bundle deal."
    }
}

# --- Session State Initialization ---
if "cart" not in st.session_state:
    st.session_state.cart = []
if "ratings" not in st.session_state:
    st.session_state.ratings = []
if "show_rating" not in st.session_state:
    st.session_state.show_rating = False
if "buyer_name" not in st.session_state:
    st.session_state.buyer_name = ""
if "buyer_notes" not in st.session_state:
    st.session_state.buyer_notes = ""

# --- Sidebar (Cart) ---
st.sidebar.header("Your Cart")
st.sidebar.subheader("Buyer Information")
st.session_state.buyer_name = st.sidebar.text_input("Your Name", value=st.session_state.buyer_name)
st.session_state.buyer_notes = st.sidebar.text_area("Any special instructions?", value=st.session_state.buyer_notes)

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

    if not st.session_state.buyer_name.strip():
        st.sidebar.warning("Please enter your name before completing purchase.")
    elif st.sidebar.button("Complete Purchase"):
        st.sidebar.success("🎉 Order saved! Please pay with cash upon delivery.")
        st.session_state.cart = []
        st.session_state.show_rating = True

# --- Product Display ---
st.header("Products")
product_names = list(products.keys())
products_per_row = 2  # fixed layout

for i in range(0, len(product_names), products_per_row):
    cols = st.columns(products_per_row)
    for j, product_name in enumerate(product_names[i:i + products_per_row]):
        product = products[product_name]
        with cols[j]:
            st.subheader(product_name)
            if product_name == "Snack & Drink Bundle":
                col1, col2 = st.columns(2)
                with col1:
                    st.image(products["Chicken Noodle Snacks"]["img"], width=150)
                with col2:
                    st.image(products["Dr Pepper"]["img"], width=150)
            else:
                st.image(product["img"], width=200)
            st.write(product["description"])
            st.write(f"Price: NT${product['price']}")
            quantity = st.number_input(f"Quantity for {product_name}", min_value=1, max_value=20, value=1, key=f"qty_{product_name}")
            if st.button(f"Add {product_name} to Cart", key=f"add_{product_name}"):
                for _ in range(quantity):
                    st.session_state.cart.append({"name": product_name, "price": product["price"]})
                st.success(f"✅ Added {quantity} x {product_name} to cart!")

# --- Rating Section ---
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
