import streamlit as st

st.set_page_config(page_title="مكتبتي الشخصية", page_icon="📚", layout="wide")

st.title("📚 مكتبتي الرقمية الشخصية")

if 'read_books' not in st.session_state:
    st.session_state.read_books = []

if 'wishlist_books' not in st.session_state:
    st.session_state.wishlist_books = []

tab1, tab2, tab3 = st.tabs(["📖 الكتب المقروءة", "🛒 قائمة الأمنيات", "📊 الملخص السنوي"])

with tab1:
    st.header("الكتب التي قرأتها")
    with st.expander("➕ إضافة كتاب جديد قرأته"):
        with st.form("read_form"):
            title = st.text_input("عنوان الكتاب")
            author = st.text_input("المؤلف")
            rating = st.slider("التقييم (من 5)", 1, 5, 5)
            review = st.text_area("النبذة / الانطباع الشخصي")
            price = st.number_input("سعر الشراء (ر.س)", min_value=0.0)
            place = st.text_input("مكان الشراء")
            year_read = st.number_input("سنة القراءة", min_value=2000, max_value=2030, value=2026)
            
            submitted = st.form_submit_button("حفظ الكتاب")
            if submitted and title:
                st.session_state.read_books.append({
                    "title": title, "author": author, "rating": rating,
                    "review": review, "price": price, "place": place, "year": year_read
                })
                st.success("تم إضافة الكتاب لمكتبتك بنجاح!")

    st.divider()
    search_query = st.text_input("🔍 ابحث في كتبك المقروءة (العنوان أو المؤلف)...")
    
    filtered_books = st.session_state.read_books
    if search_query:
        filtered_books = [b for b in filtered_books if search_query.lower() in b["title"].lower() or search_query.lower() in b["author"].lower()]

    if not filtered_books:
        st.info("لا توجد كتب مطابقة للبحث أو أن المكتبة فارغة حالياً.")
    
    for book in filtered_books:
        st.subheader(book["title"])
        st.write(f"**المؤلف:** {book['author']} | **التقييم:** {'⭐' * book['rating']}")
        st.write(f"**النبذة:** {book['review']}")
        st.write(f"**السعر:** {book['price']} ر.س | **مكان الشراء:** {book['place']} | **سنة القراءة:** {book['year']}")
        st.divider()

with tab2:
    st.header("الكتب المراد شراؤها (قائمة الأمنيات)")
    with st.expander("➕ إضافة كتاب لقائمة الأمنيات"):
        with st.form("wish_form"):
            w_title = st.text_input("عنوان الكتاب المطلوب")
            w_author = st.text_input("المؤلف")
            w_price = st.number_input("السعر المتوقع (ر.س)", min_value=0.0)
            w_place = st.text_input("مكان توفر الكتاب / الرابط")
            w_notes = st.text_area("ملاحظات / سبب الرغبة في قراءته")
            
            w_submitted = st.form_submit_button("إضافة للأمنيات")
            if w_submitted and w_title:
                st.session_state.wishlist_books.append({
                    "title": w_title, "author": w_author, "price": w_price,
                    "place": w_place, "notes": w_notes
                })
                st.success("تمت الإضافة لقائمة الأمنيات!")

    st.divider()
    for i, book in enumerate(st.session_state.wishlist_books):
        st.subheader(book["title"])
        st.write(f"**المؤلف:** {book['author']} | **السعر المتوقع:** {book['price']} ر.س")
        st.write(f"**مكان الشراء:** {book['place']} | **ملاحظات:** {book['notes']}")
        
        if st.button(f"📖 تمت قراءته (نقل للمقروءة)", key=f"move_{i}"):
            st.session_state.read_books.append({
                "title": book["title"],
                "author": book["author"],
                "rating": 5,
                "review": book["notes"],
                "price": book["price"],
                "place": book["place"],
                "year": 2026
            })
            st.session_state.wishlist_books.pop(i)
            st.success(f"تم نقل '{book['title']}' إلى الكتب المقروءة بنجاح!")
            st.rerun()
        st.divider()

with tab3:
    st.header("📊 الملخص السنوي للكتب المقروءة")
    if not st.session_state.read_books:
        st.info("لا توجد كتب مقروءة حالياً لعرض الملخص السنوي.")
    else:
        years = sorted(list(set(b["year"] for b in st.session_state.read_books)), reverse=True)
        selected_year = st.selectbox("اختر السنة لاستعراض كتبها:", years)
        
        year_books = [b for b in st.session_state.read_books if b["year"] == selected_year]
        st.write(f"إجمالي الكتب المقروءة في سنة **{selected_year}**: **{len(year_books)}** كتب.")
        st.divider()
        
        for book in year_books:
            st.markdown(f"- **{book['title']}** لـ {book['author']} (التقييم: {'⭐' * book['rating']})")