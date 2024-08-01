# This is my AI Online Compiler this works with the help of the Gemini AI 

import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Online Compiler", layout="centered")

# This is the css for the page components like text area or buttons etc..
st.markdown(
    """
    <style>
    .stTextInput textarea, .stTextArea textarea {
        height: 400px !important;
        font-family: "Courier New", Courier, monospace;
        background-color: black;
        color: #f1f1f1;
        border : 5px ridge blue;
    }
    .stButton button {
        background-color: blue;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 10px 24px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 40px;
        margin: 4px 2px;
        cursor: pointer;
        transition-duration: 0.4s;
    }
    .stButton button:hover {
        background-color: white;
        color: black;
        font-size: 40px;
        border: 2px solid #4CAF50;
    }
    .error {
        color: red;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🌐 Online Compiler")

#defining the function call to pass the parameters / arguments to get the output of the given code as per the prefered programming language

def online_compiler(language, code):
    """Generates a Roadmap based on given parameter.

    Args:
        language: Type Language you preferred
        code: Code you want to compile

    Returns:
        Output of the code you want to compile
    """
    try:
        # This is the gemini API key
        genai.configure(api_key="AIzaSyDWZkP2r17QA3Q_zWxbv70LoEsXYufLeY0")

        # Create the model
        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }
        
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
            system_instruction="You are an expert in compiling the code of any programming language. Your responses should contain only the output of the code, whether it is an error or the correct output, without any additional text.",
        )

        # this is the prompt to get the actual desired output for the user
        prompt = f"Please compile the following {language} code and return only the output: {code}"

        # Generate the response
        response = model.generate_content(prompt)
        output_text = response.text.strip()
        return output_text

    except Exception as e:
        print(f"An error occurred: {e}")
        return str(e)

# Layout to select the particular  programming language

language_options = ["Python", "Java", "JavaScript", "C", "C++", "Dart"]
default_code_samples = {
    "Python": "print('Hello, World!')",
    "Java": "public class Main {\n public static void main(String[] args) {\n System.out.println('Hello, World!');\n }\n}",
    "JavaScript": "console.log('Hello, World!');",
    "C": "#include <stdio.h>\nint main() {\n printf('Hello, World!');\n return 0;\n }",
    "C++": "#include <iostream>\nint main() {\n std::cout << 'Hello, World!'; return 0;\n }",
    "Dart": "void main() {\n print('Hello, World!');\n }"
}

language = st.selectbox("Choose Programming Language", language_options)

st.header("Enter your code")

code = st.text_area(" ", value=default_code_samples[language])

if st.button("Run", key="run_button"):
    output = online_compiler(language, code)
    if "An error occurred" in output:
        st.header("Output:", anchor=None)
        st.text_area(" ", value=output, height=400, key="output_area", class_="error")
    else:
        st.header("Output:", anchor=None)
        st.text_area(" ", value=output, height=400, key="output_area")
