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

# Removing the length of the suffix from the end
def remove_suffix(input_string, suffix):
    """Removing the length of the suffix from the end"""
    
    if input_string.endswith(suffix):
        return input_string[:-len(suffix)]
    else:
        raise("Invalid Input")

# Function to generate balance and due date history
def fn_generate_data(mv_setup_df, mv_txn_df, mv_balance_df, mv_due_date_history_df):
    """Function to generate balance and due date history"""

    lv_total_tenure_outstanding = 0
    lv_total_posted_txns = 0
    lv_total_due_amt = 0
    lv_total_payment = 0
    lv_total_payment_appropriated = 0
    lv_index = 0
    lv_txn_details = []
    mv_txn_details_by_bill = [] 
    lv_has_excess_payment = False
    lv_payment_excess = 0

    for lv_txn_index, lv_txn_row in mv_txn_df.iterrows():
        
        lv_setup_record_type = mv_setup_df.loc[mv_setup_df['TXN_CODE'] == lv_txn_row['TXN_TCD_CODE']]['TYPE'].values
        lv_balance_code = lv_txn_row['TXN_TCD_CODE']
        lv_posted = 0
        lv_adj_plus = 0
        lv_adj_minus = 0
        lv_waive = 0
        lv_paid = 0
        lv_payment_excess_paid = 0

        if(lv_balance_code != 'PAYMENT'):
            lv_txn_details.append(lv_txn_row)

        # print("For Txn Code "+lv_txn_row['TXN_TCD_CODE']+" Value of lv_setup_record_type is - "+str(lv_setup_record_type))
        
        if(len(lv_setup_record_type) == 0):
            if(lv_txn_row['TXN_AMT']>0):
                if lv_balance_code.endswith("ADJ_PLUS"):
                    lv_balance_code = remove_suffix(lv_balance_code, "_ADJ_PLUS")
                    lv_adj_plus = lv_txn_row['TXN_AMT']
                    lv_total_tenure_outstanding += lv_adj_plus
                    lv_total_posted_txns += lv_adj_plus
                elif lv_balance_code.endswith("ADJ_MINUS"):
                    lv_balance_code = remove_suffix(lv_balance_code, "_ADJ_MINUS")
                    lv_adj_minus = lv_txn_row['TXN_AMT']
                    lv_total_payment_appropriated += lv_adj_minus
                elif lv_balance_code.endswith("WAIVE"):
                    lv_balance_code = remove_suffix(lv_balance_code, "_WAIVE")
                    lv_waive = lv_txn_row['TXN_AMT']
                    lv_total_payment_appropriated += lv_waive
                else:
                    lv_posted = lv_txn_row['TXN_AMT']
                    lv_total_tenure_outstanding += lv_posted
                    lv_total_posted_txns += lv_posted

                if not(lv_balance_code.endswith("ADJ_MINUS")) and not(lv_balance_code.endswith("WAIVE")) and lv_payment_excess >0:
                    if(lv_payment_excess > lv_txn_row['TXN_AMT']):
                        print("Payment excess is more than txn Amount")
                        lv_payment_excess_paid = lv_txn_row['TXN_AMT']
                        lv_payment_excess = lv_payment_excess - lv_txn_row['TXN_AMT']
                    else:
                        print("Payment is less or equal to txn Amount")
                        lv_payment_excess_paid = lv_payment_excess 
                        lv_payment_excess = 0                

            elif(lv_txn_row['TXN_AMT']<0):
                lv_paid = lv_txn_row['TXN_AMT']
                lv_total_payment_appropriated += (lv_paid*-1)

            if (lv_txn_row['TXN_AMT'] != 0 and lv_balance_code != 'PAYMENT'):
                # print("Value of code is - "+lv_balance_code)
                if lv_balance_code in mv_balance_df['BALANCE_CODE'].values:
                    lv_temp_row_id = mv_balance_df.index[mv_balance_df['BALANCE_CODE'] == lv_balance_code][0]
                    mv_balance_df.at[lv_temp_row_id, 'POSTED'] += lv_posted
                    mv_balance_df.at[lv_temp_row_id, 'PAID'] += lv_paid*-1
                    mv_balance_df.at[lv_temp_row_id, 'ADJ_PLUS'] += lv_adj_plus
                    mv_balance_df.at[lv_temp_row_id, 'ADJ_MINUS'] += lv_adj_minus
                    mv_balance_df.at[lv_temp_row_id,'WAIVE'] += lv_waive
                    mv_balance_df.at[lv_temp_row_id,'PAID_WITH_EXCESS'] += lv_payment_excess_paid
                    mv_balance_df.at[lv_temp_row_id, 'OUTSTANDING'] = mv_balance_df.at[lv_temp_row_id, 'POSTED'] + mv_balance_df.at[lv_temp_row_id, 'ADJ_PLUS'] - mv_balance_df.at[lv_temp_row_id, 'ADJ_MINUS'] - mv_balance_df.at[lv_temp_row_id,'WAIVE'] - mv_balance_df.at[lv_temp_row_id, 'PAID'] - mv_balance_df.at[lv_temp_row_id,'PAID_WITH_EXCESS']
                else:
                    mv_balance_df = pd.concat([mv_balance_df, pd.DataFrame(
                                                                    {   'BALANCE_CODE': [lv_balance_code],
                                                                        'POSTED': [lv_posted],
                                                                        'PAID': [lv_paid],
                                                                        'ADJ_PLUS': [lv_adj_plus],
                                                                        'ADJ_MINUS': [lv_adj_minus],
                                                                        'WAIVE': [lv_waive],
                                                                        'PAID_WITH_EXCESS': [lv_payment_excess_paid],
                                                                        'OUTSTANDING': [lv_posted - lv_paid]
                                                                    })],
                                            ignore_index=True)

        elif(lv_setup_record_type == "BILL"):
            lv_due_generation_dt = lv_txn_row['TXN_DT']
            lv_due_amount = lv_txn_row['TXN_AMT']
            lv_total_due_amt += lv_due_amount
            mv_due_date_history_df = pd.concat([
                                                    mv_due_date_history_df,
                                                    pd.DataFrame(
                                                                    {
                                                                        'DUE_GENERATION_DATE': [lv_due_generation_dt],
                                                                        'DUE_AMOUNT': [lv_due_amount],
                                                                        'ADDITIONAL_CHARGES': [round(lv_total_tenure_outstanding - lv_due_amount,2)],
                                                                        'TOTAL_OUTSTANDING': [lv_total_tenure_outstanding],
                                                                    }
                                                    )
                                                ], ignore_index=True
                                                )
            
            temp_mv_balance_df = mv_balance_df.copy()
            temp_mv_balance_df.loc['Total']=temp_mv_balance_df.sum()
            temp_mv_balance_df.loc[temp_mv_balance_df.index[-1], 'BALANCE_CODE'] = ''

            mv_txn_details_by_bill.append({
                'DUE_GENERATION_DATE': lv_due_generation_dt,
                'TXN_DETAILS': lv_txn_details,
                'BALANCE_DETAILS': temp_mv_balance_df
            })

            lv_txn_details = []
            lv_index += 1
            lv_total_tenure_outstanding = 0
            
        elif(lv_setup_record_type == "IGNORE"):
            print("Ignore txns record - "+lv_balance_code)
        elif(lv_setup_record_type == "EXCESS"):
            lv_has_excess_payment = True
            lv_payment_excess += lv_txn_row['TXN_AMT']*-1
        elif(lv_setup_record_type == "PAYMENT"):
            lv_total_payment += lv_txn_row['TXN_AMT']
            # print('Payment - '+ str(lv_total_payment))

    mv_balance_df.loc['Total']= mv_balance_df.sum()
    mv_balance_df.loc[mv_balance_df.index[-1], 'BALANCE_CODE'] = ''
    
    return mv_balance_df,mv_due_date_history_df, mv_txn_details_by_bill, lv_total_posted_txns, lv_total_payment, lv_total_due_amt, lv_total_payment_appropriated, lv_has_excess_payment

# Main Program
def main():
    
    # -- Streamlit Settings
    st.set_page_config("Billing Summarizer")
    st.header("Billing Summarizer 💁")
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

            mv_balance_df = pd.DataFrame(columns=['BALANCE_CODE','POSTED','PAID','ADJ_PLUS','ADJ_MINUS','WAIVE','PAID_WITH_EXCESS','OUTSTANDING'])
            mv_due_date_history_df = pd.DataFrame(columns=['DUE_GENERATION_DATE','DUE_AMOUNT','ADDITIONAL_CHARGES','TOTAL_OUTSTANDING'])

            with st.spinner("Generating response..."):

                mv_balance_df, mv_due_date_history_df, mv_txn_details_by_bill, lv_total_posted_txns, lv_total_payment, lv_total_due_amt, lv_total_payment_appropriated, lv_has_excess_payment = fn_generate_data(mv_setup_df, mv_txn_df, mv_balance_df, mv_due_date_history_df)

                with st.container(border=True):
                    if not lv_has_excess_payment:
                        st.markdown(
                                        f"""
                                        #### Summary:
                                        - Total Txns Posted are **{round(lv_total_posted_txns,2)}**.
                                        - Total Due Amounts are **{round(lv_total_due_amt,2)}**.
                                        - Total Payment received **{round(lv_total_payment,2)}**.
                                        - Total Payment appropriated **{round(lv_total_payment_appropriated,2)}**.
                                        - Difference of Payments **{round(round(lv_total_payment,2) - round(lv_total_payment_appropriated,2),2)}**.
                                        - Estimated Payoff Amount **{round(round(lv_total_posted_txns,2) - round(lv_total_payment,2),2)}**.
                                        """
                                    )
                    else:
                        st.markdown(
                                        f"""
                                        #### Summary:
                                        - Total Txns Posted are **{round(lv_total_posted_txns,2)}**.
                                        - Total Due Amounts are **{round(lv_total_due_amt,2)}**.
                                        - Total Payment received **{round(lv_total_payment,2)}**.
                                        - Total Payment appropriated **{round(lv_total_payment_appropriated,2)}**.
                                        - Difference of Payments **{round(round(lv_total_payment,2) - round(lv_total_payment_appropriated,2),2)}**.
                                        - Estimated Payoff Amount **{round(round(lv_total_posted_txns,2) - round(lv_total_payment,2),2)}**.
                                        - Account has Excess Payment Transaction.
                                        """
                                    )

                with st.expander("Balance Details"):
                    st.dataframe(mv_balance_df, use_container_width=True)

                with st.expander("Due Date History"):
                    st.dataframe(mv_due_date_history_df, use_container_width=True)
                
                with st.container(border=True):
                    st.subheader("Txn & Balance details By Due Date")
                    st.text("")
                    st.text("")
                    
                    for row in mv_txn_details_by_bill:
                        with st.expander("Due Dt - "+str(row['DUE_GENERATION_DATE'])):
                            st.dataframe(row['BALANCE_DETAILS'], use_container_width=True)
                            st.dataframe(row['TXN_DETAILS'], use_container_width=True)
                                
            fn_display_user_messages("File Processing Completed Successfully","Success",mv_processing_message)
        else:
            fn_display_user_messages("Upload Input Files","Error",mv_processing_message)

# Loading Main
if __name__ == "__main__":
    main()