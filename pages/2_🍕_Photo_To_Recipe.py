import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
from PIL import Image


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_gemini_response(input_prompt, image):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input_prompt, image[0]])
    return response.text


def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()

        images_parts = [
            {
                "mime_type" : uploaded_file.type,
                "data": bytes_data
            }
        ]
        return images_parts
    else:
        raise FileNotFoundError("No file uploaded, so far :(")


st.set_page_config(page_title="Photo to Recipe", page_icon='icon_p2r.png')

with open('style.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.header("Unlocking Recipes Through Images 🤟")
st.sidebar.success("Select a page")
st.write('----')
st.image('bg_img_p2r.png')
st.subheader("Craft Your Ideal Meal Plan, Instantly!🤤")
st.write('----')
uploaded_file = st.file_uploader("**Choose an Food Image...**", type=['jpg', 'jpeg', 'png'])
image = ""

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)

submit = st.button("**Tell How to Make This Recipe**")
st.write('----')
input_prompt = """
You are an expert in Cooking where you need to identify the meal in the image and also tell how to cook this meal 
mentioning ingredients needed with amount, instructions to cook the meal and also tell what nutrients have it this meal.
In the below format:
                Mutton Kosha
  Ingredients:
        1 kg mutton, cut into medium-sized pieces
        2 onions, sliced
        4 cloves garlic, minced
        1 inch ginger, minced
        1 teaspoon red chili powder
        1 teaspoon coriander powder
        1 teaspoon cumin powder
        1 teaspoon turmeric powder
        1/2 teaspoon garam masala
        1/4 cup yogurt
        1 cup water
        2 tablespoons oil
        Salt to taste
  Instructions:
        In a large bowl, combine the mutton with the sliced onions, minced garlic, and ginger.
        Add the red chili powder, coriander powder, cumin powder, turmeric powder, and garam masala to the bowl. Mix well.
        Pour the yogurt over the mutton and mix again.
        Add enough water to cover the mutton.
        Cover the bowl and refrigerate for at least 4 hours or overnight.
        Heat the oil in a large pot over medium heat.
        Drain the mutton marinade and add the mutton to the pot.
        Cook the mutton, stirring occasionally, until it is browned on all sides.
        Add the marinade to the pot and bring to a boil.
        Reduce heat to low, cover, and simmer for 1-1.5 hours or until the mutton is tender.
        Season with salt to taste.
        Serve the mutton kosha hot with rice, roti, or naan.
  Nutrients:
        Protein: Mutton is a rich source of protein, which is essential for building and repairing tissues.
        Iron: Mutton contains a good amount of iron, which is important for transporting oxygen throughout the body.
        Zinc: Mutton is also a good source of zinc, which is important for immune function and skin health.
        Vitamin B12: Mutton is a good source of vitamin B12, which is important for nerve function and red blood cell production.
        
        all headings like food name, Ingredients, Instructions, Nutrients are in h2 heading format
    """

if submit:
    with st.spinner("**Cooking up Your Favorite Recipe...😋**"):
        image_data = input_image_setup(uploaded_file)
        response = get_gemini_response(input_prompt, image_data)
        st.header("Let's create something delicious together!")
        st.write(response)
        st.session_state["Chat_history"].append({"user": image_data, "response": response})
        # Add a slider for ratings
        st.write("**Tell How Well Our App is! We are very excited to Know 🙃**")
        rating = st.slider('**Rate our app:**', 1, 5, 1)
        st.write(f'You rated the app {rating} out of 5.')
        if rating:
            st.write("Very Very Thanks for your review! 😍")
