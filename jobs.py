import streamlit as st
import pandas as pd

# Display user Error, Warning or Success Message
def fn_display_user_messages(lv_text, lv_type, mv_processing_message):
    """Display user Info, Error, Warning or Success Message"""
    
    if lv_type == "Success":
        with mv_processing_message.container(): 
            st.success(lv_text)
    elif lv_type == "Error":
        with mv_processing_message.container(): 
            st.error(lv_text)
    elif lv_type == "Warning":
        with mv_processing_message.container(): 
            st.warning(lv_text)
    else:
        with mv_processing_message.container(): 
            st.info(lv_text)

# Main Program
def main():
    
    # -- Streamlit Settings
    st.set_page_config("Job Analyzer")
    st.header("Job Analyzer 💁")
    st.text("")
    st.text("")
    st.text("")

    # -- Display Processing Details
    mv_processing_message = st.empty()
    st.text("")
    st.text("")

    # -- Input Upload
    with st.sidebar:
        st.header("Upload Files")

        st.text("")
        lv_job_details_xlsx = st.file_uploader("Batch Execution Details", type=["xlsx"])
    
    # -- Generate Job Summary
    if st.button("Generate Job Summary"):
        try:
            if lv_job_details_xlsx == None:
                raise Exception('Upload Job Details')
            else:
                lv_pd_job_details = pd.read_excel(lv_job_details_xlsx, index_col=0)
                
                st.dataframe(lv_pd_job_details.head(10),use_container_width=True)
        except Exception as e:
            fn_display_user_messages("Error Details: - "+str(e),"Error",mv_processing_message)


# Loading Main
if __name__ == "__main__":
    main()