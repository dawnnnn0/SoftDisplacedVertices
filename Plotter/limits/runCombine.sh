dn=$(basename ${1})

if [[ ! -d limit_$dn ]]; then
  mkdir limit_$dn
else
  echo "Dir limit_$dn already exists! Results might be overwritten."
fi

for fn in $1/*_datacard.txt
do
  bfn="$(basename -- $fn)"
  echo "run combine: ${bfn}"
  combine -M AsymptoticLimits $1/${bfn} > limit_$dn/limit_${bfn}
done
