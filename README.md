Xcode Development Tools
=

bump_buildnum.py
==
`bump_buildnum.py`: This file is used to bump the build number if any source files have changed.

Configuring
----
In order to configure `bump_buildnum.py` into your Xcode project:
- Make `bump_buildnum.py` executable
- Create a sample `buildnum.ver` file populated with version and build
- Add a "New Run Script Phase" in your target's build settings
- Call python script from phase (absolute path), passing (relative paths) buildnum.ver, source directory to search recursively, and one or more Info.plist files 

