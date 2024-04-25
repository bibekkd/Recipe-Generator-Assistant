import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel('gemini-pro')


def get_gemini_response(input_text, input_prompt):
    response = model.generate_content([input_text, input_prompt])
    return response.text


st.set_page_config(page_title='Recipe To Ingredients', page_icon='icon_r2i.png')
if "Chat_history" not in st.session_state:
    st.session_state["Chat_history"] = []
with open('style.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.header('Recipe in, Ingredients Out 😎')
st.sidebar.success("Select a page")
st.write('----')
st.image('bg_img_r2i.png')
st.subheader("Craft Your Perfect Meal Plan Instantly!🧑‍🍳")
st.write('----')
input_prompt = """
You are expert in Cooking so whenever user write a meal name tell the user how to cook the meal mentioning the 
ingredients amounts to cook the meal and instructions to cook the meal and also mention which nutrients the meal have.If user write 
anything other than food/meal name , show error message  "No such Food Exists, Please try right one! and no input text is given don't generate anything"
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
input_text = st.text_area("**Write Your Favourite Recipe Here :)**", key='input_text')
submit = st.button("**Generate**")
chat_history_key = st.button("**Chat History**")
st.write('----')
if len(input_text) > 0 and submit:
    with st.spinner("**Crafting Your Beloved Recipe...😋**"):
        response = get_gemini_response(input_text=input_text, input_prompt=input_prompt)
        st.subheader("Let's whip up something yummy!😍")
        st.write(response)
        st.write("**Tell How Well Our App is! We are very excited to Know 🙃**")
        rating = st.slider('**Rate our app:**', 1, 5, 1)
        st.write(f'You rated the app {rating} out of 5.')
        if rating:
            st.write("Very Very Thanks for your review! 😍")
elif len(input_text) <= 0 and submit:
    st.write("**Write Your Favorite Recipe!🤤**")

if chat_history_key:
    if st.session_state["Chat_history"] != None:
        for chat in st.session_state["Chat_history"]:
            st.write(f"**You:** {chat['user']}")
            st.write(f"**Plan to Plate Assistant:** {chat['response']}")