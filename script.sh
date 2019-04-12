#!/bin/bash
cd $HOME
mkdir $HOME/backup
touch $HOME/merged_1.txt
count=0
total_count=1
opion_count=0
tentative_count=0
vulgarity_count=0
pos_count=0
neu_count=0
neg_count=0
touch $HOME/example.txt
while true; do
        sleep 10s
        count=$(( count + 1 ))
        Direc=$(ls -lt | grep text.txt | tail -10 | sed -e's/  */ /g' | cut -d " " -f9)
        for item in $Direc
        do
                cd $HOME/$item
                touch $HOME/merged_$count.txt
                Files="$(ls -lt | grep part | sed -e's/  */ /g'  | cut -d " " -f9)"
                for f in $Files
                do
                        cat $HOME/$item/$f | tr '()' ' ' | sed -e's/  *//g' >> $HOME/merged_$count.txt
                done
                mv $HOME/$item $HOME/backup/$item
                cd $HOME/
        done
        run_total_count="$(cat $HOME/merged_$count.txt | awk -F, '{ sum += $4 } END { print sum }')"
        run_opinion_count="$(cat $HOME/merged_$count.txt | awk -F, '{ sum += $3 } END { print sum }')"
        run_vulgarity_count="$(cat $HOME/merged_$count.txt | awk -F, '{ sum += $2 } END { print sum }')"
        run_tentative_count="$(cat $HOME/merged_$count.txt | awk -F, '{ sum += $1 } END { print sum }')"
	run_pos_count="$(cat $HOME/merged_$count.txt | awk -F, '{ sum += $5 } END { print sum }')"
	run_neu_count="$(cat $HOME/merged_$count.txt | awk -F, '{ sum += $6 } END { print sum }')"
	run_neg_count="$(cat $HOME/merged_$count.txt | awk -F, '{ sum += $7 } END { print sum }')"
        total_count=$((total_count + run_total_count))
        opion_count=$((opion_count + run_opinion_count))
        tentative_count=$((tentative_count + run_tentative_count))
        vulgarity_count=$((vulgarity_count + run_vulgarity_count))
	pos_count=$((pos_count + run_pos_count))
	neu_count=$((neu_count + run_neu_count))
	neg_count=$((run_neg_count + neg_count))
        echo "*********************************"
        a=`echo $opion_count/$total_count*100|bc -l`
        b=`echo $vulgarity_count/$total_count*100|bc -l`
        c=`echo $tentative_count/$total_count*100|bc -l`
	d=`echo $pos_count/$total_count*100|bc -l`
	e=`echo $neu_count/$total_count*100|bc -l`
	f=`echo $neg_count/$total_count*100|bc -l`
	neg=`echo $f | cut -d "." -f1`
	neu=`echo $e | cut -d "." -f1`
	pos=`echo $d | cut -d "." -f1`
	vul=`echo $b | cut -d "." -f1`
	opi=`echo $a | cut -d "." -f1`
	echo "Opnion Perecentage: $a %"
	echo "Vulgarity Percentage:$b %"
	echo "Tentative Percentage:$c %"
	echo "Positive Percentage:$d %"
	echo "Neutral Percentage:$e %"
	echo "Negative Percentage:$f %"
	echo "$count,$neg,$neu,$pos,$vul,$opi" >> $HOME/example.txt
        echo "*********************************"	
        mv $HOME/merged_$count.txt $HOME/backup/merged_$count.txt
done

