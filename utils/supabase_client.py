import base64
import streamlit as st
from supabase import create_client, Client

@st.cache_resource
def get_supabase_client() -> Client:
    url = st.secrets["SUPABASE_URL"] 
    key = st.secrets["SUPABASE_KEY"] 
    return create_client(url, key)

supabase: Client = get_supabase_client()

def insert_code(code_title: str, code_type: str, loc: int, code_file_bytes: bytes = None, pasted_code_text: str = None):
    data = {
        "codeTitle": code_title,
        "codeType": code_type,
        "linesOfCode": loc,
        "pastedCode": pasted_code_text,
    }

    if code_file_bytes:
        encoded_file = base64.b64encode(code_file_bytes).decode('utf-8')
        data["codeFile"] = encoded_file

    try:
        response = supabase.table("Codes").insert(data).execute()
        return response
    except Exception as e:
        st.error(f"Database insertion error: {e}")
        return None
    
def insert_result(code_id: int, complexity_score: int, vulnerability_density: int,
                  tdi_score: int, risk_classification: str, needs_refactoring: bool) -> int | None:
    
    data = {
        "codeId": code_id,
        "complexityScore": complexity_score,
        "vulnerabilityDensity": vulnerability_density,
        "tdiScore": tdi_score,
        "riskClassification": risk_classification,
        "needsRefactoring": needs_refactoring,
    }
    try:
        response = supabase.table("Results").insert(data).execute()
        return response.data[0]["resultId"]
    except Exception as e:
        st.error(f"Error saving results: {e}")
        return None
 
 
def insert_complexity(result_id: int, edges: int, nodes: int,
                      connected_components: int, decision_points: int) -> None:
    
    data = {
        "resultsId": result_id,
        "edges": edges,
        "nodes": nodes,
        "connectedComponents": connected_components,
        "decisionPoints": decision_points,
    }
    try:
        supabase.table("Complexities").insert(data).execute()
    except Exception as e:
        st.error(f"Error saving complexity: {e}")
 
 
def insert_flag(result_id: int, rule_id: int, line_number: int) -> None:
    
    data = {
        "resultId": result_id,
        "ruleId": rule_id,
        "lineNumber": line_number,
    }
    try:
        supabase.table("Flags").insert(data).execute()
    except Exception as e:
        st.error(f"Error saving flag: {e}")
 
 
def get_or_create_rule(rule_name: str, rule_descr: str) -> int | None:

    try:
        existing = (
            supabase.table("Rules")
            .select("ruleId")
            .eq("ruleName", rule_name)
            .limit(1)
            .execute()
        )
        if existing.data:
            return existing.data[0]["ruleId"]
 
        response = supabase.table("Rules").insert({
            "ruleName": rule_name,
            "ruleDescr": rule_descr,
        }).execute()
        return response.data[0]["ruleId"]
    except Exception as e:
        st.error(f"Error fetching/creating rule: {e}")
        return None