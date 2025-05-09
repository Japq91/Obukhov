for year in {1990..2024}; do #2021..2024
		for mon in {1..12}; do # 1..12
				python descarga_inst.py $year $mon
				#python descarga_2_inst.py $year $mon
				#python descarga_acum.py $year $mon
		done
done
echo "DONE!"
