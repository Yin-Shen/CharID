for i in `ls chr*_ap_filter.txt|sort -V`
do
     echo "File name is: $i";
     cat $i >> whole_ocr_loop_ap_filter.bed;
     rm $i;
done

