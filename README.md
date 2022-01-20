# Evolutionary harmonization
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/taidopurason/evolutionary-harmonization/blob/main/evolutionary_harmonization_colab.ipynb)


This code can generate a chord progression to any piece of melody. 
User has to input the melody, key and the alphabet of chords that are suitable to that key.


## Requirements
```
mingus==0.6.1
LilyPond (if you want to generate sheet music)
```


## Usage

One simple way to use this code is to follow the provided notebook and change the variables `test_chords`, `test_melody`, `key`, `alphabet` to generate the chords for different pieces of music. There you can also see an example of producing sheet music.  

In the `test_music_evolution.py` file is where the main running of the algorithm takes place.
The `evolution.py` file has the `HarmonyGene` class and `genetic_algorithm` function that performs the natural selection process.
The function `write_composition` in `mingus_test.py` creates an object which is suitable for `mingus` and produces a `.midi` file.

*See the poster for more in detail description of the algorithm.*



