#!/bin/bash
set -e

# Tworze obraz z pliku Dockerfile
docker build --tag moj-obraz .

# Odpalam kontener z obrazu
# --rm = usuwam kontener jak zakończy działanie
# -p = mapuje porty host:kontener czyli port 80 bedzie laczyl sie do portu kontenera 5000
docker run --rm -p 5000:5000 moj-obraz