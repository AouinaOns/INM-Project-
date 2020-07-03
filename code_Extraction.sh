#!/bin/sh

input="kalya-id.csv"
while IFS= read -r pmid
do
    url="https://www.ncbi.nlm.nih.gov/pubmed/?term=$pmid&report=xml&format=text"
    wget $url -O $pmid.tmp
    cat $pmid.tmp | sed "s/&lt;/</g" | sed "s/&gt;/>/g" > $pmid.xml
    rm $pmid.tmp
done < "$input"