#!/bin/bash
dir=$PWD
cd ${dir}/python
python3 main.py g d\' < ${dir}/lilyp/cello/cello1007.ly>${dir}/lilyp/guitar/guitar1007.ly
cd ${dir}/lilyp
lilypond BWV1007Prelude.ly
mv BWV1007Prelude.pdf ${dir}/pdf/
cd ${dir}
diff lilyp/guitar/old/guitar1007.ly lilyp/guitar/guitar1007.ly
