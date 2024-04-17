if [ "$#" -ne 4 ]; then
    echo "Usage: $0 [queryfile] [resultfile] [indexfile] [dictfile]"
    exit 1
fi

queryfile="$1"
resultfile="$2"
indexfile="$3"
dictfile="$4"

python tf_idf_search.py $queryfile $resultfile $indexfile $dictfile