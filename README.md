# clustersplaining
Helps explain clustering with colors

#### Notes

For best results, use Python 3, Python 2.7 has some integer division problems that affect how the images are rendered. 

#### Installation

This code depends on my data mining library `hew`

```shell
git clone https://github.com/JeffreyMFarley/hew.git
cd hew
python3 setup.py install

cd ..
git clone https://github.com/JeffreyMFarley/clustersplaining.git
```

#### Using this codebase

```shell
# Generate the base palette image
python3 display_swatches.py

# Generate an 8 color palette
python3 build_clusters.py

# See all the available options
python3 build_clusters.py --help

```
