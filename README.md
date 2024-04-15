# Bill Generator

## Overview
- This repository is used show generated Dues and Bills for month on month basis based on input Excel.
- Input Format: CSV
  - Setup File
    - Txn Code: Transaction Code
    - Type: 
      - Ignore: Txn to be ignored
      - Bill: Billing Transaction Code
  - Txn File
    - Txn Date: Transaction Date
    - GL Date: General Ledger Reflection Date
    - Txn Code: Transaction Code
    - Txn Amt: Transaction Amount, used +ve sign to update balance and -ve sign for reduction of balance.
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