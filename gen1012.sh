cd ./python
python3 main.py d d < ../lilyp/cello/cello1012.ly>../lilyp/guitar/guitar1012.ly
cd ../lilyp
lilypond BWV1012Prelude.ly
mv BWV1012Prelude.pdf ../pdf/
cd ../
diff lilyp/guitar/old/guitar1012.ly lilyp/guitar/guitar1012.ly
