# Bill Generator

## Overview
- This repository is used show generated Dues and Bills for month on month basis based on input Excel.
- Input Format: CSV
  - Setup File
    - TXN_CODE: Transaction Code
    - TYPE: 
      - IGNORE: Txn to be ignored
      - BILL: Billing Transaction Code
      - BILL_ASSOCIATE: Transaction Code Resulting to Billing Amount
      - EXCESS: Excess Payment
  - Txn File
    - TXN_ID: Transaction Sequence Number
    - TXN_POST_DT: Transaction Date
    - TXN_GL_POST_DT: General Ledger Reflection Date
    - TXN_TCD_CODE: Transaction Code
    - TXN_AMT: Transaction Amount, used +ve sign to update balance and -ve sign for reduction of balance.
- Output Format: CSV
  - Balance:
    - BALANCE_CODE: Balance Code
    - POSTED: Posted Balance
    - PAID: Paid Balance
    - OUTSTANDING: Total Outstanding Balance
  - Due Date History:
    - DUE_GENERATION_DATE: Billing Transaction Date
    - DUE_AMOUNT: Dude Amount To be Paid
    - ADDITIONAL_CHARGES: Addition Transactions posted between Due dates
    - TOTAL_OUTSTANDING: Due Amount + Additional Charges to be Paid