configure_file("${CMAKE_CURRENT_SOURCE_DIR}/src/version.c.in" "${CMAKE_CURRENT_SOURCE_DIR}/src/version.c")
aux_source_directory(src UTIL_SRC)
add_library(util STATIC ${UTIL_SRC})
add_dependencies(util ex_cjson ex_lz4)
if (DEFINED GRANT_CFG_INCLUDE_DIR)
  add_definitions(-DGRANTS_CFG)
endif()
target_include_directories(
    util
    PUBLIC "${TD_SOURCE_DIR}/include/util"
    PRIVATE "${CMAKE_CURRENT_SOURCE_DIR}/inc"
    PRIVATE "${TD_SOURCE_DIR}/include/common"
    PRIVATE "${GRANT_CFG_INCLUDE_DIR}"
    PUBLIC $<TARGET_PROPERTY:ex_cjson,INC_DIR>
    PUBLIC $<TARGET_PROPERTY:ex_lz4,INC_DIR>
)
target_link_libraries(
    util
    PUBLIC os
    PUBLIC api
)
target_link_directories(util INTERFACE $<TARGET_PROPERTY:ex_cjson,LIB_DIR>)
target_link_libraries(util PRIVATE $<TARGET_PROPERTY:ex_cjson,LIB_NAME>)

target_link_directories(util INTERFACE $<TARGET_PROPERTY:ex_lz4,LIB_DIR>)
target_link_libraries(util PRIVATE $<TARGET_PROPERTY:ex_lz4,LIB_NAME>)

if(${BUILD_TEST})
    ADD_SUBDIRECTORY(test)
endif(${BUILD_TEST})

