import streamlit as st
import openai
import time

st.set_page_config(page_title="Documentation SQL", page_icon="🗃️")


# Set OpenAI API key (stored securely in .streamlit/secrets.toml)
openai.api_key = st.secrets["OpenAI_key"]

def sidebar():
    """
    Displays the login and OpenAI API key input in the sidebar.
    """
    st.sidebar.title("🔑 Acesso")

    # Login form
    with st.sidebar.expander("Login com credenciais"):
        if st.session_state.get("logged_in", False):
            st.sidebar.success("Você está logado!")
            if st.sidebar.button("Sair"):
                st.session_state["logged_in"] = False
                st.session_state["openai_key"] = None
                st.sidebar.info("Você saiu da conta. Faça login novamente, se necessário.")
                st.rerun()
        else:
            username = st.text_input("Usuário:", placeholder="Digite seu usuário", key="username")
            password = st.text_input("Senha:", placeholder="Digite sua senha", type="password", key="password")
            if st.button("Entrar", key="login_button"):
                if username == st.secrets["Login"] and password == st.secrets["Password"]:
                    st.session_state["logged_in"] = True
                    st.session_state["openai_key"] = st.secrets["OpenAI_key"]
                    st.sidebar.success("Login realizado com sucesso!")
                    time.sleep(2)
                    st.rerun()
                else:
                    st.sidebar.error("Usuário ou senha incorretos.")
    
    st.sidebar.subheader('Details')
    st.sidebar.write("***Why this page has a login?***")
    st.sidebar.markdown("As you can see in the code, this page is for documentation of SQL base files from any database.")

def analyze_sql(sql_code, language):
    """Analyze SQL code and generate documentation."""
    prompt = f"""
You are a database expert. Analyze the following SQL trigger or procedure and create detailed documentation about its functionality, parameters, and flow. Translate the documentation to {language}.

SQL Code:
{sql_code}
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert in SQL documentation."},
            {"role": "user", "content": prompt}
        ]
    )
    return response["choices"][0]["message"]["content"]

def main():
    st.title("Database Trigger and Procedure Documentation")
    st.write("Upload a SQL file containing triggers or procedures, and get detailed documentation.")

    # File uploader
    uploaded_file = st.file_uploader("Upload SQL file", type=["sql"])

    # Language selection
    language = st.selectbox(
        "Select documentation language", ["English", "Portuguese", "Spanish", "German"]
    )

    if uploaded_file is not None:
        # Read SQL file content
        sql_code = uploaded_file.read().decode("utf-8")

        # Display SQL code (optional)
        with st.expander("View uploaded SQL code"):
            st.code(sql_code, language="sql")

        # Analyze and generate documentation
        if st.button("Generate Documentation"):
            # return print(st.secrets["OpenAI_key"])
            with st.spinner("Analyzing and generating documentation..."):
                try:
                    documentation = analyze_sql(sql_code, language)
                    st.success("Documentation generated successfully!")

                    # Display documentation
                    st.subheader("Generated Documentation")
                    st.write(documentation)

                    # Download option
                    st.download_button(
                        "Download Documentation", documentation, file_name="documentation.txt"
                    )
                except Exception as e:
                    st.error(f"Error generating documentation: {e}")

if __name__ == "__main__":
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    sidebar()

    if st.session_state["logged_in"]:
        main()
