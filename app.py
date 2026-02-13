from dashboard import Dashboard
from settings import Settings
import streamlit as st
from analysis import calculate_complexity

def Complexity():
    st.title("Code Analysis and Security Tool")

    tab1, tab2, tab3 = st.tabs(["Upload", "Paste Code", "Result"]) 

    with tab1:
        uploaded_file = st.file_uploader("Choose a .py file", type=[".py"])
        if uploaded_file is not None:
            file_content = uploaded_file.read().decode("utf-8")
            st.text_area("File Preview", value=file_content, height=200, disabled=True)
            if st.button("Run Analysis", key="run_upload", type="primary"):
                st.session_state.analysis_done = True
                st.success("Analysis complete! Head to the Results tab.")

    with tab2:
        code_input = st.text_area("Paste Python code here", height=200, key="code_input")
        if st.button("Run Analysis", key="run_paste", type="primary"):
            if code_input:
                st.session_state.analysis_done = True
                st.success("Analysis complete! Head to the Results tab.")
            else:
                st.warning("Please paste some code first.") 

    with tab3:
        if st.session_state.analysis_done:
            code_to_analyze = ""
            if uploaded_file is not None:
                code_to_analyze = file_content
            elif code_input:
                code_to_analyze = code_input
            
            complexity_score = calculate_complexity(code_to_analyze)
            st.subheader("Analysis Results")
            st.write(f"Code Complexity Score: {complexity_score}")
        else:
            st.info("Please run an analysis in the previous tabs to see results.")
            

pg = st.navigation([Dashboard, Complexity, Settings])
pg.run()

