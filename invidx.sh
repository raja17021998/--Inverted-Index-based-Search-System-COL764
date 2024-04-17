
if [ $# -ne 4 ]; then
    echo "Usage: $0 [coll-path] [indexfile] {0|1} {0|1}"
    exit 1
fi

collPath="$1"
indexFile="$2"
compression="$3"
tokenizer="$4"

python invidx_cons.py $collPath $indexFile $compression $tokenizer

