# Building Eclipse distribution

This folder contains several files and dirs, that allow to build base Eclipse distribution and pre-install any plugins in it


## Prequisities

In order to setup your Eclipse multi-platform build envoronment, you need to split Eclipse platform builds into 3 parts: base (platform-independent part), linux and win32.

To do so, you can use one of the following methods:

### Manual splitting

If you want to manually split Eclipse distributions, follow the steps:

1. Get [Eclipse IDE](https://www.eclipse.org/downloads/packages/) of the desired version for both OS (Windows and Linux). Both packages must be the same release/version
2. Unarchive the packages
3. Use your favorite folder comparison tool (e.g. [Beyond Compare](https://en.wikipedia.org/wiki/Beyond_Compare)) to compare two IDE folders:
  1. Determine the files/folders that **varies for different OS** (including file sizes, ignore timestamps). Place them into platform-dependent directories located here (*linux/, win32/*), respecting the original hierarchy
  2. Determine the files/folders that identical for both OS. Place them into platform-independent directory (*base*)
5. If you wish to install any plugins, open the build script and edit the **PLUGIN_NAMES** list
4. Run the build script and check both distributions working properly

*Note:* mind that **plugins/** folder contain both platform-specific and platform-independent packages
*Note:* delete the **placeholder** files located in each directory

### Splitting using script

You can use the **splitter.py** script to split Eclipse distributions automatically:

1. Get [Eclipse IDE](https://www.eclipse.org/downloads/packages/) of the desired version for both OS (Windows and Linux). Both packages must be the same release/version
2. Unarchive the packages
3. Place both package folders into *eclipse/* directory, naming it **eclipse-linux** and **eclipse-win32** respectively
4. Run the build script
5. Check 3 part folders for content


## Compile

To build the Eclipse distribution, you need to run the build script:

```
python builder.py [--target=OS] [options]
```

Examples:

```
python builder.py --target=win32
```
```
python builder.py --nobuild
```

Get the help about using the script by running: `python ./builder.py --help`.

The final Eclipse distribution will be located in *eclipse-OS* folders.
