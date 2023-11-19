latexmk -pdf

for file in *.pdf
do
  file=${file%%.*}
  pdfcrop ${file} ${file}_crop.pdf
done

for file in *crop.pdf
do
  file2=${file%%_crop.pdf}
  pdf2svg $file ${file2}.svg
done

find . -type f -not \( -name '*.svg' -or -name '*.tex' -or -name '*.sh' -or -name '*.png' \) -delete