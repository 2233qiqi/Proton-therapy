#----------------------------------------------------------------------------
# Setup the project
#
cmake_minimum_required(VERSION 3.16...3.27)
project(B1)

#----------------------------------------------------------------------------
# Find Geant4 package, activating all available UI and Vis drivers by default
# See the documentation for a guide on how to enable/disable specific components
#
find_package(Geant4 REQUIRED ui_all vis_all)
find_package(ROOT REQUIRED COMPONENTS Core RIO)
find_package(VTK REQUIRED COMPONENTS GUISupportQt RenderingOpenGL2)
find_package(Qt5 REQUIRED COMPONENTS Widgets)
find_package(TBB REQUIRED)

#----------------------------------------------------------------------------
set(ROOT_DIR "/home/qiqi/ROOT/root")
set(ROOT_INCLUDE_DIRS "${ROOT_DIR}/include")
set(ROOT_LIBRARIES 
    -L"${ROOT_DIR}/lib"
    -lCore -lImt -lRIO -lNet -lHist -lGraf -lGraf3d -lGpad
    -lROOTVecOps -lTree -lTreePlayer -lRint -lPostscript
    -lMatrix -lPhysics -lMathCore -lThread -lMultiProc
    -lROOTDataFrame
    -Wl,-rpath,${ROOT_DIR}/lib
    -pthread -lm -ldl -rdynamic
)

#----------------------------------------------------------------------------
find_library(TBB_LIB NAMES libtbb.so.12 libtbb.so.2 REQUIRED)

#----------------------------------------------------------------------------
# Locate sources and headers for this project
# NB: headers are included so they will show up in IDEs
#
file(GLOB sources ${PROJECT_SOURCE_DIR}/src/*.cc)
file(GLOB headers ${PROJECT_SOURCE_DIR}/include/*.hh)

#----------------------------------------------------------------------------
# Add the executable, use our local headers, and link it to the Geant4 libraries
#
add_executable(main main.cc ${sources} ${headers})

#----------------------------------------------------------------------------
target_include_directories(main PRIVATE
    include
    ${Geant4_INCLUDE_DIRS}
    ${ROOT_INCLUDE_DIRS}
)

#----------------------------------------------------------------------------
target_link_libraries(main PRIVATE
    ${ROOT_LIBRARIES}
    ${Geant4_LIBRARIES}
    ${TBB_LIB}
)

#----------------------------------------------------------------------------
# Copy all scripts to the build directory, i.e. the directory in which we
# build B1. This is so that we can run the executable directly because it
# relies on these scripts being in the current working directory.
#
#set(EXAMPLEB1_SCRIPTS
# exampleB1.in
# exampleB1.out
# init_vis.mac
#  run1.mac
#run2.mac
# vis.mac
# )

foreach(_script ${EXAMPLEB1_SCRIPTS})
  configure_file(
    ${PROJECT_SOURCE_DIR}/${_script}
    ${PROJECT_BINARY_DIR}/${_script}
    COPYONLY
    )
endforeach()
