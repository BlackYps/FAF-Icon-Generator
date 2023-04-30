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
        if not icon.endswith("rest.dds"):
            continue
        layer = pdb.gimp_file_load_layer(image, os.path.join(loadfolder, icon))
        pdb.gimp_image_insert_layer(image, layer, None, -1)
        pdb.gimp_image_select_item(image, 2, layer)
        pdb.gimp_selection_invert(image)
        pdb.gimp_edit_bucket_fill(layer, 1, 28, 100, 0, 0, 0, 0)
    pdb.gimp_selection_none(image)

    num_layers = len(image.layers)
    icon_w = 30
    icon_h = 28
    cols = 8
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


def autoresize(image, layer, icondistance, tech, shape, selected):
    # The dimensions have to be multiples of 4 or the engine mangles the icons
    pdb.gimp_image_select_item(image, 2, layer)
    pdb.gimp_image_select_rectangle(image, 3, 0, 0, icondistance, icondistance)
    _, x1, y1, x2, y2 = pdb.gimp_selection_bounds(image)
    new_w = x2 - x1
    new_h = y2 - y1
    offset_x = -x1
    offset_y = -y1
    if new_w % 4 == 1 or new_w % 4 == 2:
        offset_x += 1
    if new_h % 4 == 1 or new_h % 4 == 2:
        offset_y += 1
    if new_w % 4 > 0:
        new_w += 4 - (new_w % 4)
    if new_h % 4 > 0:
        new_h += 4 - (new_h % 4)

    # This will likely need to be changed when the shape sizes change
    if not selected and tech > 1 and shape in ["fighter", "ship", "sub"]:
        offset_y += 1
    # Center the images with tech markers
    if tech > 1:
        new_h += 4
        offset_y += 3
    pdb.gimp_image_resize(image, new_w, new_h, offset_x, offset_y)


def plugin_main(loadfolder, imagefolder, preview):
    shapes = ['bomber', 'bot', 'commander', 'experimental', 'factory', 'factoryhq', 'fighter', 'gunship', 'land',
              'ship', 'structure', 'sub', 'subcommander']
    symbols = ['air', 'antiair', 'antiartillery', 'antimissile', 'antinavy', 'antishield', 'armored', 'artillery',
               'bomb', 'counterintel', 'directfire', 'energy', 'energy_storage', 'engineer', 'generic', 'intel', 'land',
               'mass', 'missile', 'naval', 'shield', 'sniper', 'transport', 'wall']
    types = ["over", "rest", "selected", "selectedover"]
    image = pdb.file_png_load(os.path.join(imagefolder, "techmarkers.png"),
                              os.path.join(imagefolder, "techmarkers.png"))
    shapelayer = pdb.gimp_file_load_layer(image, os.path.join(imagefolder, "shapes.png"))
    pdb.gimp_image_insert_layer(image, shapelayer, None, -1)
    symbollayer = pdb.gimp_file_load_layer(image, os.path.join(imagefolder, "symbols.png"))
    pdb.gimp_image_insert_layer(image, symbollayer, None, -1)
    iconlist = os.listdir(loadfolder)
    iconlist.sort()
    errors = ""
    skipped_files = 0
    icondistance = 40
    pdb.gimp_image_resize(image, icondistance, icondistance, 0, 0)

    for icon in iconlist:
        # Parse filenames
        if not icon.startswith("icon_"):
            skipped_files += 1
            continue
        try:
            name, extension = icon.split(".")
            elements = name.split("_")
            if "energy_storage" in name:
                elements[2] = "energy_storage"
                del elements[3]
            if "subcommander" in name:
                elements.insert(2, "generic")
            if elements[1].endswith(("1", "2", "3")):
                shape = elements[1][0:-1]
                tech = int(elements[1][-1])
            else:
                shape = elements[1]
                tech = 0
            symbol = elements[2]
            type = elements[3]
        except IndexError:
            errors += "Unexpected number of underscores: Cannot parse file " + icon + "\n"
        else:
            # Save a copy so we don't have to reset the translate and resize operations
            save_img = pdb.gimp_image_duplicate(image)

            # Move layers to get the desired icon
            distance = icondistance * -1
            if shape == "structure" or shape == "sub":
                techmarker_offset = 1
            elif shape == "land":
                techmarker_offset = 1
            else:
                techmarker_offset = 0
            selected = False
            if type == "selected" or type == "selectedover":
                techmarker_offset += 1
                selected = True
            try:
                pdb.gimp_layer_translate(save_img.layers[2], 0, tech * distance + techmarker_offset)  # Techlayer
                if symbol == "wall":  # Handle inconsistent naming of walls
                    pdb.gimp_layer_translate(save_img.layers[1], types.index(type) * distance, 13 * distance)  # Shapelayer
                    pdb.gimp_layer_translate(save_img.layers[0], 0, symbols.index("generic") * distance)  # Symbollayer
                else:
                    pdb.gimp_layer_translate(save_img.layers[1], types.index(type) * distance, shapes.index(shape) * distance)  # Shapelayer
                    pdb.gimp_layer_translate(save_img.layers[0], 0, symbols.index(symbol) * distance)  # Symbollayer
            except ValueError:
                errors += "ValueError: Cannot parse file " + icon + "\n"
            else:
                if type == "over" or type == "selectedover":
                    pdb.gimp_drawable_invert(save_img.layers[0], 0)

                layer = pdb.gimp_image_merge_visible_layers(save_img, CLIP_TO_IMAGE)
                autoresize(save_img, layer, icondistance, tech, shape, selected)
                layer = pdb.gimp_image_merge_visible_layers(save_img, CLIP_TO_IMAGE)
                outputfolder = os.path.join(loadfolder, "new")
                if not os.path.exists(outputfolder):
                    os.makedirs(outputfolder)
                outputname = os.path.join(outputfolder, name + ".dds")
                # DXT1 Compression has high compression ratio and only one bit for alpha. This is exactly what we want
                pdb.file_dds_save(save_img, layer, outputname, outputname, 1, 0, 0, 0, -1, 0, 0, 0, 0, 2.2, 0, 0, 0.5)
                pdb.gimp_image_delete(save_img)
    if len(errors) > 0:
        pdb.gimp_message(
            "The following errors occured:\n" + errors + str(skipped_files) + " additional files/folders were skipped")
    elif skipped_files > 0:
        pdb.gimp_message(str(skipped_files) + " files/folders were skipped")
    if preview:
        pdb.gimp_progress_set_text("generating preview file")
        show_preview(outputfolder)


register(
    "python_fu_icon_generator",
    "generate new icons for FAF",
    "generates new icons for FAF out of lookup files",
    "BlackYps",
    "BlackYps",
    "2020",
    "<Toolbox>/File/Create/Icon Generation",
    "",
    [(PF_STRING, "loadfolder", "location of the icons", ""),
     (PF_STRING, "imagefolder", "location of the lookup images", ""),
     (PF_BOOL, "preview", "show me a preview after generation", 1)],
    [],
    plugin_main)

main()
