Xcode Development Tools
=

bump_buildnum.py
==
`bump_buildnum.py`: This file is used to bump the build number if any source files have changed. In projects with multiple targets, this script can keep all versions and build numbers in sync.

Configuring
----
In order to configure `bump_buildnum.py` into your Xcode project:
- Create a sample `buildnum.ver` file populated with version and build
- Create a Settings.json file defining:
  - `version_file` defining path to buildnum.ver
  - `source_directories` array defining source code directories. The script will search these recursively and increment build numbers if they contain modified files.
  - `info_plist_files` array defining `Info.plist` files for each target to update.
- Add a "New Run Script Phase" in your target's build settings
- Call python script from phase (absolute path), passing (relative paths) buildnum.ver, source directory to search recursively, and one or more Info.plist files 

