# DAX Measures

All measures used in the dashboard, grouped by table.

## Monthly_Totals

### UPI Volume (Bn)
```dax
DIVIDE(SUM(Monthly_Totals[Volume_Mn]),1000)
```

### UPI Value (₹ Lakh Cr)
```dax
DIVIDE(SUM(Monthly_Totals[Value_Cr]),100000)
```

### Avg Ticket Size (₹)
```dax
DIVIDE(SUM(Monthly_Totals[Value_Cr])*10000000, SUM(Monthly_Totals[Volume_Mn])*1000000)
```

### Latest Month
```dax
FORMAT(MAX(Monthly_Totals[Date]),"MMM yyyy")
```

### Monthly Txns (Bn)
```dax
VAR d = CALCULATE(MAX(Monthly_Totals[Date]))
RETURN CALCULATE(SUM(Monthly_Totals[Volume_Mn]), ALL(Date_Table), ALL(Monthly_Totals), Monthly_Totals[Date] = d)/1000
```

### Monthly Value (₹ Lakh Cr)
```dax
VAR d = CALCULATE(MAX(Monthly_Totals[Date]))
RETURN CALCULATE(SUM(Monthly_Totals[Value_Cr]), ALL(Date_Table), ALL(Monthly_Totals), Monthly_Totals[Date] = d)/100000
```

### YoY Volume Growth %
```dax
VAR d = CALCULATE(MAX(Monthly_Totals[Date]))
VAR c = CALCULATE(SUM(Monthly_Totals[Volume_Mn]), ALL(Date_Table), ALL(Monthly_Totals), Monthly_Totals[Date] = d)
VAR p = CALCULATE(SUM(Monthly_Totals[Volume_Mn]), ALL(Date_Table), ALL(Monthly_Totals), Monthly_Totals[Date] = EDATE(d,-12))
RETURN DIVIDE(c-p,p)
```

### YoY Value Growth %
```dax
VAR d = CALCULATE(MAX(Monthly_Totals[Date]))
VAR c = CALCULATE(SUM(Monthly_Totals[Value_Cr]), ALL(Date_Table), ALL(Monthly_Totals), Monthly_Totals[Date] = d)
VAR p = CALCULATE(SUM(Monthly_Totals[Value_Cr]), ALL(Date_Table), ALL(Monthly_Totals), Monthly_Totals[Date] = EDATE(d,-12))
RETURN DIVIDE(c-p,p)
```

### Banks Live on UPI
```dax
VAR d = CALCULATE(MAX(Monthly_Totals[Date]))
RETURN CALCULATE(MAX(Monthly_Totals[BanksLive]), ALL(Date_Table), ALL(Monthly_Totals), Monthly_Totals[Date] = d)
```

### Latest Avg Ticket (₹)
```dax
VAR d = CALCULATE(MAX(Monthly_Totals[Date]))
RETURN CALCULATE([Avg Ticket Size (₹)], ALL(Date_Table), ALL(Monthly_Totals), Monthly_Totals[Date] = d)
```

## App_Share

### App Volume (Mn)
```dax
SUM(App_Share[Volume_Mn])
```

### App Volume Share %
```dax
DIVIDE(SUM(App_Share[Volume_Mn]), CALCULATE(SUM(App_Share[Volume_Mn]), ALL(App_Share[App], App_Share[Category])))
```

### App Value Share %
```dax
DIVIDE(SUM(App_Share[Value_Cr]), CALCULATE(SUM(App_Share[Value_Cr]), ALL(App_Share[App], App_Share[Category])))
```

### Key App Share %
```dax
IF(SELECTEDVALUE(App_Share[App]) IN {"PhonePe","Google Pay","Paytm","Navi","super.money","BHIM"}, [App Volume Share %])
```

### Latest App Volume (Mn)
```dax
VAR d = CALCULATE(MAX(App_Share[Date]), ALL(App_Share[App], App_Share[Category]))
RETURN CALCULATE(SUM(App_Share[Volume_Mn]), App_Share[Date] = d)
```

### Latest App Share %
```dax
VAR d = CALCULATE(MAX(App_Share[Date]), ALL(App_Share[App], App_Share[Category]))
RETURN DIVIDE(CALCULATE(SUM(App_Share[Volume_Mn]), App_Share[Date] = d), CALCULATE(SUM(App_Share[Volume_Mn]), ALL(App_Share[App], App_Share[Category]), App_Share[Date] = d))
```

### App YoY Growth %
```dax
VAR d = CALCULATE(MAX(App_Share[Date]), ALL(App_Share[App], App_Share[Category]))
VAR c = CALCULATE(SUM(App_Share[Volume_Mn]), ALL(Date_Table), App_Share[Date] = d)
VAR p = CALCULATE(SUM(App_Share[Volume_Mn]), ALL(Date_Table), App_Share[Date] = EDATE(d,-12))
RETURN DIVIDE(c-p,p)
```

### PhonePe + GPay Share %
```dax
VAR d = CALCULATE(MAX(App_Share[Date]), ALL(App_Share[App], App_Share[Category]))
RETURN DIVIDE(CALCULATE(SUM(App_Share[Volume_Mn]), App_Share[App] IN {"PhonePe","Google Pay"}, App_Share[Date] = d), CALCULATE(SUM(App_Share[Volume_Mn]), ALL(App_Share[App], App_Share[Category]), App_Share[Date] = d))
```

## P2P_P2M

### Txn Volume (Bn)
```dax
DIVIDE(SUM(P2P_P2M[Volume_Mn]),1000)
```

### P2M Share of Volume %
```dax
DIVIDE(CALCULATE(SUM(P2P_P2M[Volume_Mn]), P2P_P2M[TxnType] = "P2M (Person to Merchant)"), CALCULATE(SUM(P2P_P2M[Volume_Mn]), ALL(P2P_P2M[TxnType])))
```

### Avg Ticket by Type (₹)
```dax
DIVIDE(SUM(P2P_P2M[Value_Cr])*10000000, SUM(P2P_P2M[Volume_Mn])*1000000)
```

## Top_Banks

### Bank Volume Latest (Mn)
```dax
VAR d = CALCULATE(MAX(Top_Banks[Date]), ALL(Top_Banks))
RETURN CALCULATE(SUM(Top_Banks[Volume_Mn]), ALL(Date_Table), Top_Banks[Date] = d)
```

### Bank Value Latest (₹ Cr)
```dax
VAR d = CALCULATE(MAX(Top_Banks[Date]), ALL(Top_Banks))
RETURN CALCULATE(SUM(Top_Banks[Value_Cr]), ALL(Date_Table), Top_Banks[Date] = d)
```

### Bank YoY Growth %
```dax
VAR d = CALCULATE(MAX(Top_Banks[Date]), ALL(Top_Banks))
VAR c = CALCULATE(SUM(Top_Banks[Volume_Mn]), ALL(Date_Table), Top_Banks[Date] = d)
VAR p = CALCULATE(SUM(Top_Banks[Volume_Mn]), ALL(Date_Table), Top_Banks[Date] = EDATE(d,-12))
RETURN IF(NOT ISBLANK(p), DIVIDE(c-p,p))
```

### Bank Share of UPI %
```dax
VAR d = CALCULATE(MAX(Top_Banks[Date]), ALL(Top_Banks))
RETURN DIVIDE(CALCULATE(SUM(Top_Banks[Volume_Mn]), ALL(Date_Table), Top_Banks[Date] = d), CALCULATE(SUM(Monthly_Totals[Volume_Mn]), ALL(Date_Table), ALL(Monthly_Totals), Monthly_Totals[Date] = d))
```

### Bank Avg Ticket (₹)
```dax
VAR d = CALCULATE(MAX(Top_Banks[Date]), ALL(Top_Banks))
RETURN DIVIDE(CALCULATE(SUM(Top_Banks[Value_Cr]), ALL(Date_Table), Top_Banks[Date] = d)*10000000, CALCULATE(SUM(Top_Banks[Volume_Mn]), ALL(Date_Table), Top_Banks[Date] = d)*1000000)
```

## States

### State Volume Latest (Mn)
```dax
VAR d = CALCULATE(MAX(States[Date]), ALL(States))
RETURN IF(SELECTEDVALUE(States[State]) = "Unclassified", BLANK(), CALCULATE(SUM(States[Volume_Mn]), ALL(Date_Table), States[Date] = d))
```

### State YoY Growth %
```dax
VAR d = CALCULATE(MAX(States[Date]), ALL(States))
VAR c = CALCULATE(SUM(States[Volume_Mn]), ALL(Date_Table), States[Date] = d)
VAR p = CALCULATE(SUM(States[Volume_Mn]), ALL(Date_Table), States[Date] = EDATE(d,-12))
RETURN IF(SELECTEDVALUE(States[State]) = "Unclassified", BLANK(), DIVIDE(c-p,p))
```

### State Share (Mapped) %
```dax
VAR d = CALCULATE(MAX(States[Date]), ALL(States))
RETURN IF(SELECTEDVALUE(States[State]) = "Unclassified", BLANK(), DIVIDE(CALCULATE(SUM(States[Volume_Mn]), ALL(Date_Table), States[Date] = d), CALCULATE(SUM(States[Volume_Mn]), ALL(Date_Table), ALL(States[State]), States[State] <> "Unclassified", States[Date] = d)))
```

### State Avg Ticket (₹)
```dax
VAR d = CALCULATE(MAX(States[Date]), ALL(States))
RETURN IF(SELECTEDVALUE(States[State]) = "Unclassified", BLANK(), DIVIDE(CALCULATE(SUM(States[Value_Cr]), ALL(Date_Table), States[Date] = d)*10000000, CALCULATE(SUM(States[Volume_Mn]), ALL(Date_Table), States[Date] = d)*1000000))
```

## Merchant_Categories

### Merchant Volume (Mn)
```dax
IF(SELECTEDVALUE(Merchant_Categories[MCC]) = "0000", BLANK(), SUM(Merchant_Categories[Volume_Mn]))
```

### Merchant Avg Ticket (₹)
```dax
IF(SELECTEDVALUE(Merchant_Categories[MCC]) = "0000", BLANK(), DIVIDE(SUM(Merchant_Categories[Value_Cr])*10000000, SUM(Merchant_Categories[Volume_Mn])*1000000))
```
