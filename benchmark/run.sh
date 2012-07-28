#!/bin/sh
python -m timeit -n 1000 -r 2 -s "from create import main" 'main()'
