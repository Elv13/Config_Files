# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.7

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/lepagee/config_files/tui/lib

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/lepagee/config_files/tui/lib/build

# Include any dependencies generated for this target.
include CMakeFiles/bdbg.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/bdbg.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/bdbg.dir/flags.make

CMakeFiles/bdbg.dir/card.o: CMakeFiles/bdbg.dir/flags.make
CMakeFiles/bdbg.dir/card.o: ../card.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/lepagee/config_files/tui/lib/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/bdbg.dir/card.o"
	/usr/bin/c++   $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/bdbg.dir/card.o -c /home/lepagee/config_files/tui/lib/card.cpp

CMakeFiles/bdbg.dir/card.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/bdbg.dir/card.i"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/lepagee/config_files/tui/lib/card.cpp > CMakeFiles/bdbg.dir/card.i

CMakeFiles/bdbg.dir/card.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/bdbg.dir/card.s"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/lepagee/config_files/tui/lib/card.cpp -o CMakeFiles/bdbg.dir/card.s

CMakeFiles/bdbg.dir/card.o.requires:

.PHONY : CMakeFiles/bdbg.dir/card.o.requires

CMakeFiles/bdbg.dir/card.o.provides: CMakeFiles/bdbg.dir/card.o.requires
	$(MAKE) -f CMakeFiles/bdbg.dir/build.make CMakeFiles/bdbg.dir/card.o.provides.build
.PHONY : CMakeFiles/bdbg.dir/card.o.provides

CMakeFiles/bdbg.dir/card.o.provides.build: CMakeFiles/bdbg.dir/card.o


CMakeFiles/bdbg.dir/main.o: CMakeFiles/bdbg.dir/flags.make
CMakeFiles/bdbg.dir/main.o: ../main.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/lepagee/config_files/tui/lib/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Building CXX object CMakeFiles/bdbg.dir/main.o"
	/usr/bin/c++   $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/bdbg.dir/main.o -c /home/lepagee/config_files/tui/lib/main.cpp

CMakeFiles/bdbg.dir/main.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/bdbg.dir/main.i"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/lepagee/config_files/tui/lib/main.cpp > CMakeFiles/bdbg.dir/main.i

CMakeFiles/bdbg.dir/main.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/bdbg.dir/main.s"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/lepagee/config_files/tui/lib/main.cpp -o CMakeFiles/bdbg.dir/main.s

CMakeFiles/bdbg.dir/main.o.requires:

.PHONY : CMakeFiles/bdbg.dir/main.o.requires

CMakeFiles/bdbg.dir/main.o.provides: CMakeFiles/bdbg.dir/main.o.requires
	$(MAKE) -f CMakeFiles/bdbg.dir/build.make CMakeFiles/bdbg.dir/main.o.provides.build
.PHONY : CMakeFiles/bdbg.dir/main.o.provides

CMakeFiles/bdbg.dir/main.o.provides.build: CMakeFiles/bdbg.dir/main.o


# Object files for target bdbg
bdbg_OBJECTS = \
"CMakeFiles/bdbg.dir/card.o" \
"CMakeFiles/bdbg.dir/main.o"

# External object files for target bdbg
bdbg_EXTERNAL_OBJECTS =

bdbg: CMakeFiles/bdbg.dir/card.o
bdbg: CMakeFiles/bdbg.dir/main.o
bdbg: CMakeFiles/bdbg.dir/build.make
bdbg: CMakeFiles/bdbg.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/lepagee/config_files/tui/lib/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_3) "Linking CXX executable bdbg"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/bdbg.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/bdbg.dir/build: bdbg

.PHONY : CMakeFiles/bdbg.dir/build

CMakeFiles/bdbg.dir/requires: CMakeFiles/bdbg.dir/card.o.requires
CMakeFiles/bdbg.dir/requires: CMakeFiles/bdbg.dir/main.o.requires

.PHONY : CMakeFiles/bdbg.dir/requires

CMakeFiles/bdbg.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/bdbg.dir/cmake_clean.cmake
.PHONY : CMakeFiles/bdbg.dir/clean

CMakeFiles/bdbg.dir/depend:
	cd /home/lepagee/config_files/tui/lib/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/lepagee/config_files/tui/lib /home/lepagee/config_files/tui/lib /home/lepagee/config_files/tui/lib/build /home/lepagee/config_files/tui/lib/build /home/lepagee/config_files/tui/lib/build/CMakeFiles/bdbg.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/bdbg.dir/depend

