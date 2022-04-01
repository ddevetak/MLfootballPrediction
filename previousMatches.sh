

workingFolder=$PWD

cd ./MLfootballPrediction/spiders

scrapy crawl previousMatches -a parameter1=$1

cd $workingFolder

var=$(date +'%d-%m-%Y')

if [ ! -d "$var" ]; then
  # Control will enter here if $DIRECTORY exists.
  mkdir ${var}
fi

cd ${var}
mkdir $1

mv ../finalData.csv $1


