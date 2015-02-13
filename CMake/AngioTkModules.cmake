# this script finds the modules in Modules/ folder 
# and include the components for each enabled module
file( GLOB modules ${AngioTk_SOURCE_DIR}/Modules/* ) 
foreach( module ${modules} )
  if( IS_DIRECTORY ${module} )
    angiotk_module_enablement( ${module} )
    if( ${BUILD_MODULE_${AngioTk_CURRENT_MODULE_NAME}} )
      angiotk_init_module_python(${AngioTk_CURRENT_MODULE_NAME})
      file( GLOB components ${AngioTk_CURRENT_MODULE_PATH}/* )
      foreach( component ${components} )
        if( IS_DIRECTORY ${component} )
          add_subdirectory( ${component} )
        endif()
      endforeach()
    endif()
  endif()
endforeach()