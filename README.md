# Bill Generator

## Overview
- This repository is used show generated Dues and Bills for month on month basis based on input Excel.
- Input Format: CSV
  - Setup File
    - TXN_CODE: Transaction Code
    - TYPE: 
      - IGNORE: Txn to be ignored
      - BILL: Billing Transaction Code
      - EXCESS: Excess Payment
  - Txn File
    - TXN_ID: Transaction Sequence Number
    - TXN_POST_DT: Transaction Date
    - TXN_GL_POST_DT: General Ledger Reflection Date
    - TXN_TCD_CODE: Transaction Code
    - TXN_AMT: Transaction Amount, used +ve sign to update balance and -ve sign for reduction of balance.
- Output Format: CSV
  - Balance:
    - Balance: Balance Code
    - Posted: Posted Balance
    - Paid: Paid Balance
    - Outstanding: Total Outstanding Balance
  - Due Date History:
    - Date: Billing Transaction Date
    - Due Amount: Dude Amount To be Paid
    - Additional Charges: Addition Transactions posted between Due dates
    - Total Outstanding: Due Amount + Additional Charges to be Paid