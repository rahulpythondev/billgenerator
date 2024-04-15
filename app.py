import streamlit as st
import pandas as pd
import base64

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

# Function to create a download link for the DataFrame
def fn_download_link(df, filename, title):
    """Function to create a download link for the DataFrame"""

    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # Encode DataFrame as csv
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{title}</a>'
    return href

# Main Program
def main():
    
    # -- Streamlit Settings
    st.set_page_config("Billing Generation")
    st.header("Billing Generation Agent 💁")
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
        lv_setup_csv = st.file_uploader("Setup File", type=["csv"])
        
        st.text("")
        st.text("")
        lv_txn_csv = st.file_uploader("Txn File", type=["csv"])

    # -- Generate Bill Summary
    if st.button("Generate Bill Summary"):
        if lv_setup_csv != None and lv_txn_csv != None:
            fn_display_user_messages("Processing Input Files","Success",mv_processing_message)
            
            mv_setup_df = pd.read_csv(lv_setup_csv, sep=',')
            mv_txn_df = pd.read_csv(lv_txn_csv, sep=',')

            mv_balance_df = pd.DataFrame(columns=['BALANCE_CODE','POSTED','PAID','OUTSTANDING'])
            mv_due_date_history_df = pd.DataFrame(columns=['DUE_DATE','DUE_AMOUNT','ADDITIONAL_CHARGEs','TOTAL_OUTSTANDING'])

            with st.spinner("Generating response..."):
                with st.expander("Balance Details"):
                    # -- Display Details
                    st.write(mv_balance_df)
                    st.text("")
                    st.text("")

                    # -- Download Balance Details
                    st.markdown(fn_download_link(mv_balance_df, "balance.csv", "Download Balance Details"), unsafe_allow_html=True)
                with st.expander("Due Date History"):
                    # -- Display Details
                    st.write(mv_due_date_history_df)
                    st.text("")
                    st.text("")
                    
                    # -- Download Due Date History Details
                    st.markdown(fn_download_link(mv_due_date_history_df, "due_history.csv", "Download Due Date History"), unsafe_allow_html=True)
                                
            fn_display_user_messages("File Processing Completed Successfully","Success",mv_processing_message)
        else:
            fn_display_user_messages("Upload Input Files","Error",mv_processing_message)

# Loading Main
if __name__ == "__main__":
    main()