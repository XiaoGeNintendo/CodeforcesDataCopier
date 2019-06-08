# CodeforcesDataCopier
Small Program to copy one account's submission to another on Codeforces
# Why?
When you have many accounts, and you want to merge them, you can copy the submissions.
# How?
1. install python3 
2. input `pip install robobrowser` in command line
3. input your handle & password in usr.txt
4. run the program
5. input the handle you want to copy from
6. input the filter. 
7. input 'y'
8. wait and end. (if there are too many submissions to copy, the quota of codeforces may be reached. In this situation wait for 5 minutes and retry)
# Filter Example
1. Only Copy id>=53000000 `sub["id"]>=53000000`
2. Only copy 1173A/B/C/D/E/F... `sub["contestId"]==1173`
3. Only copy AC code `sub["verdict"]=="OK"`
4. Obtain two conditions `sub["contestId"]==1173 and sub["verdict"]=="OK"`
for more, please view the API of Codeforces and the source code of the program.
