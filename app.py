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

# Function to generate balance and due date history
def fn_generate_data(mv_setup_df, mv_txn_df, mv_balance_df, mv_due_date_history_df):
    """Function to generate balance and due date history"""

    for lv_txn_index, lv_txn_row in mv_txn_df.iterrows():
        lv_setup_record_type = mv_setup_df.loc[mv_setup_df['TXN_CODE'] == lv_txn_row['TXN_TCD_CODE']]['TYPE'].values
        
        lv_balance_code = lv_txn_row['TXN_TCD_CODE']
        lv_posted = 0
        lv_paid = 0

        # print("For Txn Code "+lv_txn_row['TXN_TCD_CODE']+" Value of lv_setup_record_type is - "+str(lv_setup_record_type))
        
        if(len(lv_setup_record_type) == 0):
            if(lv_txn_row['TXN_AMT']>0):
                # print("Add to Posted")
                lv_posted = lv_txn_row['TXN_AMT']
            elif(lv_txn_row['TXN_AMT']<0):
                # print("Add to Paid")
                lv_paid = lv_txn_row['TXN_AMT']

            if lv_balance_code in mv_balance_df['BALANCE_CODE'].values:
                lv_temp_row_id = mv_balance_df.index[mv_balance_df['BALANCE_CODE'] == lv_balance_code][0]
                mv_balance_df.at[lv_temp_row_id, 'POSTED'] += lv_posted
                mv_balance_df.at[lv_temp_row_id, 'PAID'] += lv_paid*-1
                mv_balance_df.at[lv_temp_row_id, 'OUTSTANDING'] = mv_balance_df.at[lv_temp_row_id, 'POSTED'] - mv_balance_df.at[lv_temp_row_id, 'PAID']
            else:
                mv_balance_df = pd.concat([mv_balance_df, pd.DataFrame(
                                                                {   'BALANCE_CODE': [lv_balance_code],
                                                                    'POSTED': [lv_posted],
                                                                    'PAID': [lv_paid],
                                                                    'OUTSTANDING': [lv_posted - lv_paid]
                                                                })],
                                           ignore_index=True)

        elif(lv_setup_record_type == "BILL"):
            print("Bill")
        elif(lv_setup_record_type == "IGNORE"):
            print("Ignore")
        elif(lv_setup_record_type == "BILL_ASSOCIATE"):
            print("Bill Associate")
        elif(lv_setup_record_type == "EXCESS"):
            print("Excess")

    return mv_balance_df,mv_due_date_history_df

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
            mv_due_date_history_df = pd.DataFrame(columns=['DUE_DATE','DUE_AMOUNT','ADDITIONAL_CHARGES','TOTAL_OUTSTANDING'])

            with st.spinner("Generating response..."):

                mv_balance_df, mv_due_date_history_df = fn_generate_data(mv_setup_df, mv_txn_df, mv_balance_df, mv_due_date_history_df)

                with st.expander("Balance Details"):
                    # -- Display Details
                    st.write(mv_balance_df)
                    # st.text("")

                    # -- Download Balance Details
                    # st.markdown(fn_download_link(mv_balance_df, "balance.csv", "Download Balance Details"), unsafe_allow_html=True)
                with st.expander("Due Date History"):
                    # -- Display Details
                    st.write(mv_due_date_history_df)
                    # st.text("")
                    
                    # -- Download Due Date History Details
                    # st.markdown(fn_download_link(mv_due_date_history_df, "due_history.csv", "Download Due Date History"), unsafe_allow_html=True)
                                
            fn_display_user_messages("File Processing Completed Successfully","Success",mv_processing_message)
        else:
            fn_display_user_messages("Upload Input Files","Error",mv_processing_message)

# Loading Main
if __name__ == "__main__":
    main()