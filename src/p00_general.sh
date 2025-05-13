for year in {1990..2024}; do #2021..2024
		for mon in {1..12}; do # 1..12
				python p00_download_ERA5.py $year $mon
		done
done
echo "DONE!"
