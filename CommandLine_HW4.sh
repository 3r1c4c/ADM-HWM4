#!/bin/sh

q1="Which location has the maximum number of purchases been made?"

variable=$(cut -f5 -d, bank_transactions.csv | sort | uniq -c | sort -k1 -n  | tail -1)

echo -e "\n1. $q1 ${variable[0]:0:7} purchases made in ${variable[0]:8:13}"

q2="In the dataset provided, did females spend more than males, or vice versa?"

output=$(cut -f4,9 -d, bank_transactions.csv |awk 'NR!=1'| awk -F, '$1!=""'| awk -F, '{col[$1]+=$2} END {for (i in col) print i" = "col[i]}' | sort -g)

echo -e "\n2. $q2 \n" 
echo -e "\t ${output[0]:0:15}     ${output[0]:16:15}   →  Males spended more \n"

q3="Report the customer with the highest average transaction amount in the dataset:"

result=$(cut -f2,9 -d, bank_transactions.csv | awk -F, '{col[$1]+=$2; count[$1]++} END {for (x in col) print x, col[x]/count[x]}' | sort -g -k2 | tail -1)

echo -e "3. $q3 \n
    CustomerID : ${result[0]:0:8} with average transaction amount = ${result[0]:9:11} \n "







