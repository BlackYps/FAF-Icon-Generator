# FAF Icon Generator

A Gimp plugin to automate the process of making new strategic icons for Forged Alliance Forever.

## Installation

Install the python script by dropping it in the gimp plugin folder (google how to install gimp plugins if you are unsure where it is).
You can then execute the plugin under `File -> Create -> Icon Generation`

## Usage

1. Download the images. These are the templates for the automatic icon generation. The provided examples are icons that are a little bigger.
You can also download the gimp files. They contain an additional layer that helps you with positioning the icons. It is invisible by default, but you can just enable the visibility of the layer in the right toolbar.
2. When you execute the script it asks you for the location of the png files. (If you edited the xcf files, don't forget to export them to png)
3. It also asks you for the location of the icons that you want to generate. The icons are in the textures.nx2 archive in the gamedata folder (more precisely in `/textures/ui/common/game/strategicicons/` in the archive). Extract them and specify the path in the script dialog. The script will then use the icon files to parse what icons you want it to generate. The new icons are saved in a subfolder `new`. The script will omit files that do not follow the icon naming scheme and give you a list of errors in the end.
4. By default, it generates a preview of the new icons, so you don't have to open the new files individually to check them. You do not need to save this preview. The preview uses a colored background to indicate the size of the icons. If your template images have a transparent background, the actual generated icons will also have one.
5. Put your new icons in a new folder in the gamedata folder like this : `gamedata/texturepack.nxt/textures/ui/common/game/strategicicons/`.
texturepack.nxt can be an archive, but you can also use a regular folder if you name it like this. Make sure that the folder structure is the same as in the archive where you retrieved the original icons, so the game can find it.
6. Enjoy your new icons!

If the script breaks or behaves unexpectedly, please let me know. I can't fix it if you don't tell me ;)
