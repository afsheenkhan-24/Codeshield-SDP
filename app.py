from pages.dashboard import Dashboard
from pages.settings import Settings
import streamlit as st
import pages.analysis
from pages.rules import SecurityConcerns

def Complexity():

    st.markdown("""
        <style>
        .card {
            background-color: #f8f9fa;
            border: 1px solid #e0e0e0;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            height: 180px;
            margin-bottom: 20px;
        }
        .title {
            font-size: 15px;
            color: #666;
            margin-bottom: 10px;
            font-weight: bold;
        }
        .value {
            font-size: 32px;
            font-weight: bold;
            color: #333;
        }
        .critical-label {
            padding: 2px 8px;
            border-radius: 5px;
            font-size: 12px;
            display: inline-block;
            margin-top: 10px;
            font-weight: bold;
        }
        .red-flags {
            color: #000000;
        }

        /* Red Flag Section from your image */

        .red-flag-header {
            background-color: #ffffff;    /* White background */
            color: #666666;               /* Grey text */
            padding: 15px 20px;           /* Spacing inside the box */
            border-radius: 12px;          /* Curved edges */
            font-weight: bold;
            font-size: 18px;
            border: 1px solid #eeeeee;    /* Subtle border for definition */
            margin-bottom: 20px;          /* Space between header and first card */
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        }
        .red-flag-card {
            background-color: #f4f4f4;
            border-left: 6px solid #888;
            padding: 12px 20px;
            margin-bottom: 12px;
            border-radius: 4px;
        }
        .red-flag-title {
            font-weight: bold;
            color: #222;
            font-size: 16px;
            margin-bottom: 4px;
        }
        .red-flag-desc {
            color: #555;
            font-size: 13px;
        }
        </style>
    """, unsafe_allow_html=True)


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
            if tdi > 50:
                tdi_label = "Critical"
                label_bg = "#ffdce0"  
                label_text_color = "#af080d"  
            else:
                tdi_label = "Fine"
                label_bg = "#dcfce7"  # Soft Green
                label_text_color = "#166534"

            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f'<div class="card"><div class="title">Technical Depth Index (TDI)</div><div class="value">{tdi}</div><div class="critical-label" style="background-color: {label_bg}; color: {label_text_color};">{tdi_label}</div></div>', unsafe_allow_html=True)
            with col2:
                st.markdown(f'<div class="card"><div class="title">Cyclomatic Complexity</div><div class="value">{cc}</div><div class="nodes-edges">Nodes(N): {nodes}<br>Edges (E): {edges}</div></div>', unsafe_allow_html=True)
            with col3:
                st.markdown(f'<div class="card"><div class="title">Vulnerability Density</div><div class="value">{vd}</div><div class="red-flags">No.of.Red Flags: {red_flags}</div></div>', unsafe_allow_html=True)


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