import streamlit as st

# --- Page Setup ---
st.set_page_config(page_title="Simple Shop", layout="wide")
st.title("🛍️ Welcome to the Streamlit Shop")

# --- Initialize session state ---
if "products" not in st.session_state:
    st.session_state.products = []
if "cart" not in st.session_state:
    st.session_state.cart = []
if "username" not in st.session_state:
    st.session_state.username = ""
if "ratings" not in st.session_state:
    st.session_state.ratings = []
if "show_rating" not in st.session_state:
    st.session_state.show_rating = False

# --- Fix older products ---
for p in st.session_state.products:
    if "owner" not in p:
        p["owner"] = "Unknown"

# --- Login / Username Input ---
if not st.session_state.username:
    st.session_state.username = st.text_input("Enter your name to continue:", key="username_input")
    if not st.session_state.username:
        st.stop()

# --- Sidebar User Info & Logout ---
st.sidebar.write(f"👤 Logged in as: **{st.session_state.username}**")
if st.sidebar.button("🚪 Logout"):
    # Reset session state variables safely
    st.session_state.username = ""
    st.session_state.cart = []
    st.session_state.show_rating = False

# --- Sidebar Navigation ---
page = st.sidebar.radio(
    "Navigation",
    ["🏠 Home", "🛒 Cart", "➕ Add Product", "📦 My Products"]
)

# --- Home Page ---
if page == "🏠 Home":
    st.header("Available Products")
    if not st.session_state.products:
        st.info("No products available yet. Add some in the 'Add Product' page.")
    else:
        for i, product in enumerate(st.session_state.products):
            with st.container():
                st.subheader(product.get("name", "Unnamed Product"))
                st.write(product.get("description", "No description available."))
                st.write(f"💲 Price: ${product.get('price', 0.0):.2f}")
                st.write(f"📦 In Stock: {product.get('stock', 0)}")
                owner = product.get("owner", "Unknown Seller")
                st.caption(f"🧑‍💼 Seller: {owner}")

                # Remove button for owner
                if owner == st.session_state.username:
                    if st.button(f"🗑️ Remove {product.get('name','')}", key=f"remove_home_{i}"):
                        st.session_state.products.pop(i)
                        st.success(f"Removed '{product.get('name','')}' from shop.")
                
                # Add to cart / Out of Stock
                elif product.get("stock", 0) > 0:
                    if st.button(f"Add {product.get('name','item')} to Cart", key=f"cart_{i}"):
                        st.session_state.cart.append(product)
                        product["stock"] = product.get("stock", 0) - 1
                        st.success(f"Added {product.get('name','item')} to cart!")
                else:
                    st.error("❌ Out of Stock")

# --- Cart Page ---
elif page == "🛒 Cart":
    st.header("Your Shopping Cart")
    
    if not st.session_state.cart:
        st.info("Your cart is empty.")
    else:
        total = sum(item.get("price", 0.0) for item in st.session_state.cart)
        for item in st.session_state.cart:
            st.write(f"- {item.get('name','Unnamed Product')} (${item.get('price',0.0):.2f})")
        st.write(f"**Total: ${total:.2f}**")
        
        # Complete purchase button
        if st.button("✅ Complete Purchase"):
            st.success("Purchase completed! Thank you for your order.")
            st.session_state.cart = []
            st.session_state.show_rating = True  # Show rating after purchase

# --- Rating Expander (Pyodide-safe) ---
if st.session_state.show_rating:
    with st.expander("🎉 Rate Our App!"):
        st.write("Please rate the app (1–5 stars):")
        rating = st.slider("Your Rating", 1, 5, 5)
        if st.button("Submit Rating", key="submit_rating"):
            st.session_state.ratings.append(rating)
            st.success(f"Thank you for rating the app {rating}⭐!")
            st.session_state.show_rating = False

# --- Add Product Page ---
elif page == "➕ Add Product":
    st.header("Add a New Product")
    name = st.text_input("Product Name")
    description = st.text_area("Product Description")
    price = st.number_input("Product Price", min_value=0.0, step=0.01)
    stock = st.number_input("Stock Quantity", min_value=0, step=1)
    if st.button("Add Product"):
        if name and price > 0:
            st.session_state.products.append({
                "name": name,
                "description": description,
                "price": price,
                "stock": stock,
                "owner": st.session_state.username
            })
            st.success(f"Product '{name}' added successfully!")
        else:
            st.error("Please enter a valid name and price.")

# --- My Products Page ---
elif page == "📦 My Products":
    st.header("My Products")
    my_products = [p for p in st.session_state.products if p.get("owner") == st.session_state.username]
    if not my_products:
        st.info("You haven't added any products yet.")
    else:
        for i, product in enumerate(my_products):
            st.subheader(product.get("name", "Unnamed Product"))
            st.write(product.get("description", "No description available."))
            st.write(f"💲 Price: ${product.get('price', 0.0):.2f}")
            st.write(f"📦 Stock: {product.get('stock',0)}")

            # Restock
            restock = st.number_input(
                f"Add stock for {product.get('name','item')}",
                min_value=0, step=1,
                key=f"restock_{product.get('name','')}"
            )
            if st.button(f"Restock {product.get('name','item')}", key=f"btn_{product.get('name','')}"):
                product["stock"] = product.get("stock",0) + restock
                st.success(f"Added {restock} more units to {product.get('name','item')}.")

            # Remove product
            if st.button(f"🗑️ Remove {product.get('name','')}", key=f"remove_my_{i}"):
                index_in_main = next((j for j,p_main in enumerate(st.session_state.products) if p_main==product), None)
                if index_in_main is not None:
                    st.session_state.products.pop(index_in_main)
                    st.success(f"Removed '{product.get('name','')}' from your products.")
