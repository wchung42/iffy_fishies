# IffyFishies
### This is a project contribution in support of #TeamSeas.  

## Description
IffyFishies is my contribution to the #TeamSeas campaign by Mark Rober and Mr.Beast. In this project, I code 30 million randomly generated fish for the 30 million dollar goal of the campaign. 

## Installation
1. Download the latest release [here]
2. Unzip the file with [7zip] or your program of choice
3. Launch `iffyfishies.exe`

[here]: https://github.com/wchung42/iffy_fishies/releases
[7zip]: https://www.7-zip.org/

## Notes on usage
* **_Note_: All images default to a transparent background unless the background color is changed.**
* Image mode
  * Generates individual fish images that are 1000px by 1000px.
  * `Save original` will save the image with no transformations.
  * `Save transformed` will save the image after rotation and flip (_if applicable_).
  * `Save resized` will save the image after rotation, flip, resize (_if applicable_).
  * _Note: transformations are all randomized_
* Collage mode
  * `Create collage` with no input entry will create a collage of `50` random fish with random transformations, placed randomly on the image.
  * `Add fish` will add the specified number of fish. Adds `no input` or `0` is given.
* Live mode
  * Fish are generated every `30 seconds` and based on recent new donations. Size of fish are determined by the donation amount.
  * Images are automatically saved every `30 seconds`.
  * Images are saved to the `images` directory in the `iffyfishies` directory.
  * Requires an internet connection, otherwise the program raises a connection error.
