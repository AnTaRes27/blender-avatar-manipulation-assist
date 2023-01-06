# Antares's Avatar Manipulation Assist

I made this tool to help me with odds and ends of avatar making in blender. Designed not as a standalone tool, but as another niche tool you'd add to your toolbelt.

## what AAMA does so far:
 - insert various organisational shapekeys: spacers, category and subcategory shapekeys
 - shapekey organisational manipulators: move blocks of shapekeys to somewhere else on the list. supports python regex to select shapekeys to move
 - generates breathing shapekeys for clothings given a base model that already has breathing shapekeys
 - renames mesh datablocks to their corresponding mesh object (for datablocks with only one owner though)
 - duplicates an object's vertex groups with desired affix (useful for when you're doing metarig stuff)
 - removes zero weight vertex groups
 - transfers all vertex groups weights into selected object

## installation
honestly, as it stands right now, this tool isnt meant for the general public and still in heavy development and may or may not be completed. that said, just download the zip and install like you would any other addon...... just make sure you're not using your only copy of the blend file with this. when i tested with my stuff it didnt really, yknow, destroy my files but i cant say the same for you. just..... be careful. you've been warned

## roadmap
 - generate shapekeys to hide clothes
 - whiskers attachers

 ## changelog

 v0.2.0
 - added housekeeping functions TODO?
 - added vertgroup manip functions (filtered!) TODO?

 v0.1.0
 - initial release