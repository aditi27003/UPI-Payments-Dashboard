import pandas as pd, re
from datetime import datetime
MON={m:i+1 for i,m in enumerate(['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])}
def ym(s):
    y,m=s.split('-'); return datetime(int(y),MON[m],1)
num=lambda s: float(str(s).replace(',',''))
# Monthly
rows=[]
for l in open('raw/monthly_raw.txt'):
    fy,mon,b,v,c=[x.strip() for x in l.strip().split('|')]
    d=datetime.strptime(mon,'%B-%Y')
    rows.append(dict(Date=d,FinancialYear='FY'+fy,BanksLive=int(b),Volume_Mn=num(v),Value_Cr=num(c)))
m=pd.DataFrame(rows).sort_values('Date').reset_index(drop=True)
m['AvgTicket_Rs']=(m.Value_Cr*1e7/(m.Volume_Mn*1e6)).where(m.Volume_Mn>0).round(0)
# Apps
amap={'phone pe':'PhonePe','phonepe':'PhonePe','paytm payments bank app':'Paytm','paytm (ocl)':'Paytm','paytm (ocl )':'Paytm','paytm':'Paytm',
 'fam':'FamApp by Trio','fampay':'FamApp by Trio','fampay ppi':'FamApp by Trio','fampay by trio':'FamApp by Trio','fam pay by trio':'FamApp by Trio','fam app by trio':'FamApp by Trio','famapp by trio':'FamApp by Trio',
 'whatsapp':'WhatsApp','cred':'CRED'}
cat={'PhonePe':'Big Tech / Fintech','Google Pay':'Big Tech / Fintech','Paytm':'Big Tech / Fintech','Amazon Pay':'Big Tech / Fintech','WhatsApp':'Big Tech / Fintech',
 'Navi':'New-age Fintech','super.money':'New-age Fintech','CRED':'New-age Fintech','FamApp by Trio':'New-age Fintech','BHIM':'Government (NPCI)','Others':'Others'}
a=[]
for l in open('raw/apps_raw.txt'):
    p,n,v,c=l.strip().split('|'); n=amap.get(n.strip().lower(),n.strip())
    a.append(dict(Date=ym(p),App=n,Volume_Mn=float(v),Value_Cr=float(c)))
a=pd.DataFrame(a).groupby(['Date','App'],as_index=False).sum()
a['Category']=a.App.map(cat).fillna('Bank Apps')
a['Value_Cr']=a.Value_Cr.round(0)
# P2P/P2M
p=[]
for l in open('raw/p2p_raw.txt'):
    d,pv,pc,mv,mc=l.strip().split('|'); d=ym(d)
    p+= [dict(Date=d,TxnType='P2P (Person to Person)',Volume_Mn=float(pv),Value_Cr=float(pc)),
         dict(Date=d,TxnType='P2M (Person to Merchant)',Volume_Mn=float(mv),Value_Cr=float(mc))]
p=pd.DataFrame(p)
# Banks
b=[]
for l in open('raw/banks_raw.txt'):
    d,r,n,v,c=l.strip().split('|'); n=re.sub(r'\s+',' ',n).strip()
    n={'Karnataka Bank':'Karnataka Bank Ltd.','Bank Of India':'Bank of India','Tri O Tech Solutions Private Limited':'Tri O Tech Solutions (FamApp)'}.get(n,n)
    t='Public Sector' if n in ['State Bank of India','Bank of Baroda','Union Bank of India','Punjab National Bank','Canara Bank','Indian Bank','Bank of India','Indian Overseas Bank','Central Bank of India','UCO Bank','Bank of Maharashtra'] else \
      'Payments Bank / PPI' if re.search('Payments Bank|Tri O',n) else 'Private Sector'
    b.append(dict(Date=ym(d),Rank=int(r),Bank=n,BankType=t,Volume_Mn=float(v),Value_Cr=float(c)))
b=pd.DataFrame(b)
# States
s=[]
for l in open('raw/states_raw.txt'):
    d,n,v,c=l.strip().split('|')
    s.append(dict(Date=ym(d),State=n.title().replace(' And ',' and ').replace('&','&'),Volume_Mn=float(v),Value_Cr=float(c)))
s=pd.DataFrame(s)
# MCC
c=[]
for l in open('raw/mcc_raw.txt'):
    t,code,desc,v,val=l.strip().split('|')
    c.append(dict(Date=datetime(2026,8,1),Tier={'High':'High transacting','Medium':'Medium transacting','Other':'Other'}[t],MCC=code,Category=desc,Volume_Mn=float(v),Value_Cr=float(val)))
c=pd.DataFrame(c)
# Date dim
dd=pd.DataFrame({'Date':pd.date_range('2016-04-01','2026-12-01',freq='MS')})
dd['Year']=dd.Date.dt.year; dd['MonthNo']=dd.Date.dt.month; dd['Month']=dd.Date.dt.strftime('%b')
dd['MonthYear']=dd.Date.dt.strftime('%b %Y'); dd['YearMonthKey']=dd.Year*100+dd.MonthNo
dd['FY']=dd.Date.apply(lambda x: f"FY{x.year}-{str(x.year+1)[2:]}" if x.month>=4 else f"FY{x.year-1}-{str(x.year)[2:]}")
dd['FYQuarter']=dd.MonthNo.map(lambda x:'Q1' if x in(4,5,6) else 'Q2' if x in(7,8,9) else 'Q3' if x in(10,11,12) else 'Q4')
m['FinancialYear']=m.FinancialYear.str.replace(r'FY(\d{4})-(\d{2})(\d{2})',r'FY\1-\3',regex=True)
src=pd.DataFrame({'Item':['Source','Monthly totals','App-wise','P2P vs P2M','Banks','States','Merchant categories','Units','Notes','Compiled on'],
 'Detail':['NPCI (National Payments Corporation of India) – npci.org.in',
 'UPI Product Statistics, Apr 2016 – Sep 2026','UPI Ecosystem Statistics > UPI Applications, Apr 2022 – Aug 2026 (top 12 apps per month + Others)',
 'UPI Ecosystem Statistics > P2P and P2M, Apr 2022 – Aug 2026','Top 50 Member Vol & Val (top 25 shown) – Aug 2024, Aug 2025, Aug 2026',
 'UPI Statewise Statistics – Aug 2025 vs Aug 2026 (district rows summed to state)','Merchant Category Classification – Aug 2026 (P2M only)',
 'Volume in million transactions; Value in ₹ crore (1 crore = 10 million rupees)',
 'Paytm Payments Bank App and Paytm (OCL) merged as "Paytm"; FamPay variants merged as "FamApp by Trio". "Unclassified" state = transactions NPCI could not map to a state.',
 '5 Oct 2026']})
with pd.ExcelWriter('UPI_Data.xlsx',engine='openpyxl',datetime_format='yyyy-mm-dd') as w:
    for name,df in [('Monthly_Totals',m),('App_Share',a),('P2P_P2M',p),('Top_Banks',b),('States',s),('Merchant_Categories',c),('Date_Table',dd),('About',src)]:
        df.to_excel(w,sheet_name=name,index=False)
# checks
chk=a.groupby('Date').Volume_Mn.sum().to_frame('apps').join(m.set_index('Date').Volume_Mn)
chk['ratio']=chk.apps/chk.Volume_Mn
print(chk.ratio.describe())
pc=p.groupby('Date').Volume_Mn.sum().to_frame('pp').join(m.set_index('Date').Volume_Mn); print((pc.pp-pc.Volume_Mn).abs().max())
print(sorted(a.App.unique()))
print(m.tail(3)); print(len(m),len(a),len(p),len(b),len(s),len(c))
