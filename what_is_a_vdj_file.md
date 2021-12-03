# What's a .vdj file?

[VisiData](https://www.visidata.org/) has the ability to interactively explore data sets and then [save](https://www.visidata.org/docs/save-restore/) your command history for replay later.

A `.vdj` file is a VisiData command log saved in [JSON Lines](https://jsonlines.org/) format.

_These_ `.vdj` files come from me doing a bunch of random crap in VisiData until I get something
useful, saving the log, then pruning nonsense lines as much as I can without losing the happy
ending.

Ideally they can be replayed using `--play` and `--batch` and the last line of the replay log will
show the challenge answer. Overriding the config file and VisiData directory lessen the risk of
replays getting tripped up by any user-specific plugins or options.
