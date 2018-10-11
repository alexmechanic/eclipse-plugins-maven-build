# Building Eclipse plugins

This folder contains several files and dirs, that allow to build Eclipse plugins using Maven in offline mode


## Project structure

The current folder should be the root directory for all the plugins you wish to build.
Some files and folders present are:

- **parent** (maven root project with sample settings)
- **repo**
  - dependency-repository (maven support repository containing build artifacts)
- **apache-maven-3.5.0** (maven distribution)
  - base-repo (minimal build repository)


## Prequisities

Unfortunately, you might need to modify the build script a bit in order to adapt it to your plugins' workspace.

* Modify **Cleanup()** function if you need to delete plugins' build directories after the build (examples included)
* Modify **PublishPlugins()** function, replacing the target repository directory of your build (this project is configured to build the plugins repository to ease the installation of plugins into Eclipse)


## Build

To build your plugins using Maven, you need to run the build script:

```
python builder.py [-q]
```

Get the help about using the script by running: `python builder.py --help`.

Compiled plugins repository will be located in *Bin/* folder.


## Offline build

The build script is meant to build Eclipse plugins in offline mode.

First, you need to setup the Maven offline envoronment:

### Setup Plugins dependencies

1. Using the Eclipse IDE, set all your plugins project open
2. Select **File - Export...** menu option
2. Select **Plug-in Development - Target Definition**
3. Select target directory, where to place the resulting repository (use some temporary folder)
4. Locate the created repository folder and move the **artifacts.jar** file to *repo/dependency-repository/* overwriting the old one
5. The **content.jar** file is needed to be downloaded from original Eclipse repository, e.g.:
```
./eclipse -nosplash -verbose -application org.eclipse.equinox.p2.metadata.repository.mirrorApplication -source http://download.eclipse.org/releases/oxygen -destination file:/absolute-path-to-temp-dir/
```
This is a quick-time step. Find the **content.jar** file in the target directory (it contains the information about all Eclipse packages). Move the file to *repo/dependency-repository/* overwriting the old one.

### Setup Maven local repository

1. In the *parent* project, in **pom.xml** file temporarly replace *deps* repository URL with : `http://download.eclipse.org/releases/oxygen` (or switch the commented line with the active, URL may differ depending on the release)
2. Manually unarchive Maven **apache-maven-3.5.0.tar.gz** distribution package, delete the *base-repo* directory (if exists)
3. In the **builder.py** build script comment out **PrepareMaven()** call, delete the `-o` argument from the Maven run command (*MVN_BUILD_CMD*) and run the script
4. While building, the Maven repository will be downloaded into *apache-maven-3.5.0/base-repo* directory
5. After the build succeeds, archive the Maven folder, replacing the previous package. No more Maven distribution modification is needed.
6. Add the `-o` flag back to the Maven run command in builder script (*MVN_BUILD_CMD*), switch the repository URL back in the **parent/pom.xml** configuration script
7. Run the build script again and check the build for any errors

*Note:* any time you modify your plugins' dependencies, you need to check the Maven build for errors in case the dependencies repository (*repo/dependency-repository/*) needs to be updated with newely added plugin dependencies. In case of this issue, repeat the steps, described in **Setup Plugins dependencies** section.


## Installing plugins into Eclipse

To install the built plugins, you can use two methods:

1. Using the Eclipse IDE: Select **Help - Install New Software...** menu option and follow instructions. This method will not be covered in this guide.
2. Using terminal commands:

  - Linux
```
./eclipse -nosplash -application org.eclipse.equinox.p2.director -repository file:///path-to-plugins-repo/ -installIU FULL_PLUGIN_NAME
```

  - Windows
```
eclipsec.exe -nosplash -application org.eclipse.equinox.p2.director -repository file:Disc:\path-to-plugins-repo\ -installIU FULL_PLUGIN_NAME
```

## Q/A

### I do not need to delete the plugins' build artifacts after the build and/or unarchive Maven distribution every time I start the build.

* To disable deleting build artifacts, comment out the **Cleanup()** call in the build script.
* To disable Maven distribution manipulations, comment out the **PrepareMaven()** call in the build script.

### I need to make a complete clone of the priginal Eclipse repository (e.g. from http://download.eclipse.org/releases/oxygen). How do I do that?

1. First, clone the metadata:
```
./eclipse -nosplash -verbose -application org.eclipse.equinox.p2.metadata.repository.mirrorApplication -source http://download.eclipse.org/releases/oxygen -destination file:/absolute-path-to-desired-dir/
```
This is a quick-time step.

2. Second, clone the artifacts:
```
./eclipse -nosplash -verbose -application org.eclipse.equinox.p2.artifact.repository.mirrorApplication -source http://download.eclipse.org/releases/oxygen -destination file:/absolute-path-to-desired-dir/
```
This step will take time as the command downloads lots of Eclipse packages (actually, all of the available).

3. The full Eclipse repository is located in your desired directory. This might be useful in some cases, e.g. you need to build **any** Eclipse plugins on a machine with no Internet connection.
