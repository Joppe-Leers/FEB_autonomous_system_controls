# Install script for directory: /home/joppeleers/FEB_autonomous_system_controls/src/fs_msgs

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/joppeleers/FEB_autonomous_system_controls/install")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/fs_msgs/msg" TYPE FILE FILES
    "/home/joppeleers/FEB_autonomous_system_controls/src/fs_msgs/msg/ControlCommand.msg"
    "/home/joppeleers/FEB_autonomous_system_controls/src/fs_msgs/msg/FinishedSignal.msg"
    "/home/joppeleers/FEB_autonomous_system_controls/src/fs_msgs/msg/GoSignal.msg"
    "/home/joppeleers/FEB_autonomous_system_controls/src/fs_msgs/msg/Track.msg"
    "/home/joppeleers/FEB_autonomous_system_controls/src/fs_msgs/msg/Cone.msg"
    "/home/joppeleers/FEB_autonomous_system_controls/src/fs_msgs/msg/ExtraInfo.msg"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/fs_msgs/srv" TYPE FILE FILES "/home/joppeleers/FEB_autonomous_system_controls/src/fs_msgs/srv/Reset.srv")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/fs_msgs/cmake" TYPE FILE FILES "/mnt/c/Users/joppe/Documents/FEB_autonomous_system_controls/build/fs_msgs/catkin_generated/installspace/fs_msgs-msg-paths.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include" TYPE DIRECTORY FILES "/home/joppeleers/FEB_autonomous_system_controls/devel/include/fs_msgs")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/roseus/ros" TYPE DIRECTORY FILES "/home/joppeleers/FEB_autonomous_system_controls/devel/share/roseus/ros/fs_msgs")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/common-lisp/ros" TYPE DIRECTORY FILES "/home/joppeleers/FEB_autonomous_system_controls/devel/share/common-lisp/ros/fs_msgs")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/gennodejs/ros" TYPE DIRECTORY FILES "/home/joppeleers/FEB_autonomous_system_controls/devel/share/gennodejs/ros/fs_msgs")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  execute_process(COMMAND "/usr/bin/python2" -m compileall "/home/joppeleers/FEB_autonomous_system_controls/devel/lib/python2.7/dist-packages/fs_msgs")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python2.7/dist-packages" TYPE DIRECTORY FILES "/home/joppeleers/FEB_autonomous_system_controls/devel/lib/python2.7/dist-packages/fs_msgs")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/mnt/c/Users/joppe/Documents/FEB_autonomous_system_controls/build/fs_msgs/catkin_generated/installspace/fs_msgs.pc")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/fs_msgs/cmake" TYPE FILE FILES "/mnt/c/Users/joppe/Documents/FEB_autonomous_system_controls/build/fs_msgs/catkin_generated/installspace/fs_msgs-msg-extras.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/fs_msgs/cmake" TYPE FILE FILES
    "/mnt/c/Users/joppe/Documents/FEB_autonomous_system_controls/build/fs_msgs/catkin_generated/installspace/fs_msgsConfig.cmake"
    "/mnt/c/Users/joppe/Documents/FEB_autonomous_system_controls/build/fs_msgs/catkin_generated/installspace/fs_msgsConfig-version.cmake"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/fs_msgs" TYPE FILE FILES "/home/joppeleers/FEB_autonomous_system_controls/src/fs_msgs/package.xml")
endif()
