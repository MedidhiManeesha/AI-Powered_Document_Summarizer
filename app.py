# #core packages
# import streamlit as st
# import radon.raw as rr
# import radon.metrics as rm
# import radon.complexity as rc
# from app_utils import get_reserved_word_frequency
# from wordcloud import WordCloud
# import matplotlib.pyplot as plt
# import altair as alt
# import plotly.express as px
# import pandas as pd
# import parse

# def convert_to_df(mydict):
#     return pd.DataFrame(list(mydict.items()), columns=["Keywords", "Counts"])

# def plot_wordcloud(docx):
#     my_wordcloud = WordCloud().generate(docx)
#     fig = plt.figure()
#     plt.imshow(my_wordcloud, interpolation = "bilinear")
#     plt.axis("off")
#     st.pyplot(fig)

# def main():
#     st.title("Static Code Analysis App")

#     #forms
#     with st.form(key="myform"):
#         raw_code = st.text_area("Enter Code Here", height=250)
#         submit_button = st.form_submit_button(label="Analyze")

#     #Tabs
#     tab1, tab2, tab3, tab4 = st.tabs(["Code Analysis", "Reserved", "Identifiers", "AST"])
#     results = get_reserved_word_frequency(raw_code)

#     with tab1:
#         st.subheader("Code Analysis")
#         if submit_button:
#             with st.expander("Original Code"):
#                 st.code(raw_code)
#             st.subheader("Raw SCA Metrics")
#             basic_analysis = rr.analyze(raw_code)
#             st.write(basic_analysis)

#             #maintainability index
#             mi_results = rm.mi_visit(raw_code, True)

#             #cyclomatic complexity
#             cc_results = rc.cc_visit(raw_code)

#             # Halstead : bugs, effort, operand
#             hal_results = rm.h_visit(raw_code)

#             #Column layout
#             col1, col2 = st.columns(2)
#             col1.metric(label="Maintainability Index", value=mi_results)
#             col2.metric(label="Cyclomatic complexity", value= f"{cc_results[0]}")

#             with st.expander("Halstead Metrics"):
#                 st.write(hal_results[0])
    
#     with tab2:
#         if submit_button:
#             st.subheader("Reserved")
#             # st.write(results)
#             results_as_df = convert_to_df(results["reserved"])
#             #plot with altair
#             my_chart = alt.Chart(results_as_df).mark_bar().encode(x="Keywords", y="Counts", color="Keywords")
#             st.altair_chart(my_chart, use_container_width=True)
#             t1, t2, t3 = st.tabs(["CodeCloud", "WordFreq", "PieChart"])

#             with t1:
#                 plot_wordcloud(raw_code)
#             with t2:
#                 st.dataframe(results_as_df)
#             with t3:
#                 fig2 = px.pie(values=results["reserved"].values(),names=results["reserved"].keys())
#                 st.plotly_chart(fig2)
            
    

#     with tab3:
#         if submit_button:
#             st.subheader("Identifiers")
#             #st.write(results["identifiers"])
#             results_as_df = convert_to_df(results["identifiers"])
#             #plot with altair
#             my_chart = alt.Chart(results_as_df).mark_bar().encode(x="Keywords", y="Counts", color="Keywords")
#             st.altair_chart(my_chart, use_container_width=True)
            
#             plot_wordcloud(raw_code)
    
#     with tab4:
#         if submit_button:
#             st.subheader("AST")
#             ast_results = parse.make_ast(raw_code)
#             st.json(ast_results)


# if __name__ == '__main__':
#     main()

# core packages
import streamlit as st
import radon.raw as rr
import radon.metrics as rm
import radon.complexity as rc
from app_utils import get_reserved_word_frequency
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import altair as alt
import plotly.express as px
import pandas as pd
import parse

# --------------------- Custom Styling ---------------------
def add_custom_styles():
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #f0f2f6;
        }
        div.stButton > button:first-child {
            background-color: #4CAF50;
            color: white;
            height: 3em;
            width: 15em;
            border-radius:10px;
            border:2px solid #4CAF50;
            font-size: 18px;
            font-weight: bold;
            margin: auto;
            display: block;
        }
        textarea {
            background-color: #e8f0fe !important; /* Light blue background */
            border: 2px solid #90caf9 !important; /* Border color */
            color: #000000 !important; /* Text color */
            font-size: 16px !important;
            border-radius: 8px !important;
        }
        
        </style>
        """,
        unsafe_allow_html=True
    )

def custom_title():
    st.markdown(
        "<h1 style='text-align: center; color: #4B8BBE;'> Static Code Analyzer App</h1>",
        unsafe_allow_html=True
    )

# --------------------- Utility Functions ---------------------
def convert_to_df(mydict):
    return pd.DataFrame(list(mydict.items()), columns=["Keywords", "Counts"])

def plot_wordcloud(docx):
    my_wordcloud = WordCloud().generate(docx)
    fig = plt.figure()
    plt.imshow(my_wordcloud, interpolation="bilinear")
    plt.axis("off")
    st.pyplot(fig)

# --------------------- Main App ---------------------
def main():
    add_custom_styles()
    custom_title()

    with st.form(key="myform"):
        raw_code = st.text_area("Enter Code Here", height=300)
        submit_button = st.form_submit_button(label="Analyze")

    tab1, tab2, tab3, tab4 = st.tabs(["Code Analysis", "Reserved", "Identifiers", "AST"])
    results = get_reserved_word_frequency(raw_code)

    with tab1:
        st.subheader("🔎 Code Analysis")
        if submit_button:
            with st.expander("📜 Original Code"):
                st.code(raw_code)
            st.subheader("📊 Raw SCA Metrics")
            basic_analysis = rr.analyze(raw_code)
            st.write(basic_analysis)

            mi_results = rm.mi_visit(raw_code, True)
            cc_results = rc.cc_visit(raw_code)
            hal_results = rm.h_visit(raw_code)

            col1, col2 = st.columns(2)
            col1.metric(label="Maintainability Index", value=mi_results)
            col2.metric(label="Cyclomatic complexity", value=f"{cc_results[0]}")

            with st.expander("🧮 Halstead Metrics"):
                st.write(hal_results[0])

    with tab2:
        if submit_button:
            st.subheader("📚 Reserved Keywords")
            results_as_df = convert_to_df(results["reserved"])
            my_chart = alt.Chart(results_as_df).mark_bar().encode(
                x="Keywords", y="Counts", color="Keywords"
            )
            st.altair_chart(my_chart, use_container_width=True)

            t1, t2, t3 = st.tabs(["🌥️ WordCloud", "📋 Word Frequency", "🥧 Pie Chart"])

            with t1:
                plot_wordcloud(raw_code)
            with t2:
                st.dataframe(results_as_df)
            with t3:
                fig2 = px.pie(values=results["reserved"].values(), names=results["reserved"].keys())
                st.plotly_chart(fig2)

    with tab3:
        if submit_button:
            st.subheader("🆔 Identifiers")
            results_as_df = convert_to_df(results["identifiers"])
            my_chart = alt.Chart(results_as_df).mark_bar().encode(
                x="Keywords", y="Counts", color="Keywords"
            )
            st.altair_chart(my_chart, use_container_width=True)
            plot_wordcloud(raw_code)

    with tab4:
        if submit_button:
            st.subheader("🛠️ AST (Abstract Syntax Tree)")
            ast_results = parse.make_ast(raw_code)
            st.json(ast_results)

# --------------------- Runner ---------------------
if __name__ == '__main__':
    main()
