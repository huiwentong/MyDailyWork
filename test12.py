import os
for k, v in os.environ.items():
    if k.startswith('OCT'):
        print(k,v)