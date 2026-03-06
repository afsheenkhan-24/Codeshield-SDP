from pages.dashboard import Dashboard
from pages.settings import Settings
import streamlit as st
import pages.analysis
from pages.rules import SecurityConcerns

def Complexity():
    st.title("Code Analysis and Security Tool")
    if 'analysis_done' not in st.session_state:
        st.session_state.analysis_done = False

    tab1, tab2, tab3 = st.tabs(["Upload", "Paste Code", "Result"]) 

    with tab1:
        uploaded_file = st.file_uploader("Choose a .py file", type=[".py"])
        if uploaded_file is not None:
            st.session_state.file_content = uploaded_file.read().decode("utf-8")
            st.text_area("File Preview", value=st.session_state.file_content, height=200, disabled=True)
            if st.button("Run Analysis", key="run_upload", type="primary"):
                scanner = SecurityConcerns()
                st.session_state.analysis_done = True
                st.success("Analysis complete! Head to the Results tab.")

    with tab2:
        code_input = st.text_area("Paste Python code here", height=200, key="code_input")
        
        if st.button("Run Analysis", key="run_paste", type="primary"):
            if code_input:
                st.session_state.file_content=code_input
                st.session_state.analysis_done = True
                st.success("Analysis complete! Head to the Results tab.")
            else:
                st.warning("Please paste some code first.") 
    
    with tab3:
        if not st.session_state.analysis_done:
            st.info("No analysis data available. Please upload or paste code in the previous tabs first.")
        else:
            results = scanner.run_all_rules(st.session_state.file_content, uploaded_file)
            LOC = sum(1 for line in st.session_state.file_content.splitlines() if line.strip() and not line.strip().startswith("#"))


            
            nodes_and_edges = pages.analysis.calculate_nodes_and_edges(st.session_state.file_content)
            cc = pages.analysis.calculate_complexity(nodes_and_edges)
            nodes, edges = nodes_and_edges[0], nodes_and_edges[1]
            red_flags = len(results)
            if LOC>0:
                vd = (red_flags/LOC) * 1000


            tdi = (cc+vd)/2
            if tdi>50:
                tdi_label = "Critical"
            else:
                tdi_label = "Fine"

            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f'<div class="card"><div class="title">Technical Depth Index (TDI)</div><div class="value">{tdi}</div><div class="critical-label">{tdi_label}</div></div>', unsafe_allow_html=True)
            with col2:
                st.markdown(f'<div class="card"><div class="title">Cyclomatic Complexity</div><div class="value">{cc}</div><div class="nodes-edges">Nodes(N): {nodes}<br>Edges (E): {edges}</div></div>', unsafe_allow_html=True)
            with col3:
                st.markdown(f'<div class="card"><div class="title">Vulnerability Density</div><div class="value">{vd}</div><div class="red-flags">No.of.Red Flags: {red_flags}</div></div>', unsafe_allow_html=True)



            st.markdown('<div class="red-flag-container">', unsafe_allow_html=True)
            st.markdown('<div class="red-flag-header">Identified Security Red Flags</div>', unsafe_allow_html=True)
            
            if red_flags > 0:
                for report in results:                    
                    st.markdown(f"""
                        <div class="red-flag-card">
                            <div class="red-flag-title">{report["rule_title"]}</div>
                            <div class="red-flag-desc">{report['description']}</div>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown('<div class="red-flag-empty">No security vulnerabilities identified.</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

            if st.button("Generate Report"):
                pass

pg = st.navigation([Dashboard, Complexity, Settings])
pg.run()