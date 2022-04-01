
workingFolder=$PWD

cd ./MLfootballPrediction/spiders

scrapy crawl nextMatches  -a parameter1=$1

cd $workingFolder

var=$(date +'%d-%m-%Y')

if [ ! -d "$var" ]; then
  # Control will enter here if $DIRECTORY exists.
  mkdir ${var}
fi

cd ${var}
mkdir $1

mv ../games.csv $1


