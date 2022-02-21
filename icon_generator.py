#!/usr/bin/python

from gimpfu import *
import os


def show_preview(loadfolder):
    image = pdb.gimp_image_new(80, 80, 0)
    iconlist = os.listdir(loadfolder)
    iconlist.sort()
    color = pdb.gimp_context_get_background()
    pdb.gimp_context_set_background((0.8, 0.8, 0.8, 1.0))
    
    for icon in iconlist:
        if not icon.startswith("icon_"):
            continue
        # if not icon.endswith("rest.dds"):
        #     continue
        layer = pdb.gimp_file_load_layer(image, os.path.join(loadfolder, icon))
        pdb.gimp_image_insert_layer(image, layer, None, -1)
        pdb.gimp_image_select_item(image, 2, layer)
        pdb.gimp_selection_invert(image)
        pdb.gimp_edit_bucket_fill(layer, 1, 28, 100, 0, 0, 0, 0)
    pdb.gimp_selection_none(image)
        
    num_layers = len(image.layers)
    icon_w = 40
    icon_h = 40
    cols = 4
    rows = num_layers / cols
    if num_layers % cols != 0:
        rows += 1
    w = cols * icon_w
    h = rows * icon_h
    image.resize(w, h, 5, 5)
    
    idx = 0
    for layer in reversed(image.layers):  # Layers are in reverse order
        x_trans = idx % cols * icon_w
        y_trans = idx / cols * icon_h
        layer.translate(x_trans, y_trans)
        idx += 1
    
    pdb.gimp_context_set_background((0.7, 0.7, 0.9, 1.0))
    image.flatten()
    pdb.gimp_context_set_background(color)
    display = pdb.gimp_display_new(image)


register(
    "python_fu_icon_generator",
    "Preview existing icons",
    "Preview existing icons for FAF out of lookup files",
    "BlackYps", 
    "BlackYps", 
    "2020",
    "<Toolbox>/File/Create/Icon preview",
    "",
    [(PF_STRING, "loadfolder", "location of the icons", "")],
    [],
    show_preview)

main()
