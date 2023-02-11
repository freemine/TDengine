aux_source_directory(src TRANSPORT_SRC)
add_library(transport STATIC ${TRANSPORT_SRC})
add_dependencies(transport ex_libuv os)

target_include_directories(
    transport
    PUBLIC "${TD_SOURCE_DIR}/include/libs/transport"
    PRIVATE "${CMAKE_CURRENT_SOURCE_DIR}/inc"
    PUBLIC $<TARGET_PROPERTY:ex_libuv,INC_DIR>
)

target_link_libraries(
    transport
    PUBLIC os
    PUBLIC util
    PUBLIC common
)
target_link_directories(transport INTERFACE $<TARGET_PROPERTY:ex_libuv,LIB_DIR>)
target_link_libraries(transport PRIVATE $<TARGET_PROPERTY:ex_libuv,LIB_NAME>)

if (${BUILD_WITH_UV_TRANS})
if (${BUILD_WITH_UV})
  ## target_link_libraries(
  ##   transport
  ## )
  add_definitions(-DUSE_UV)
endif(${BUILD_WITH_UV})
endif(${BUILD_WITH_UV_TRANS})

if (${BUILD_TEST})
  add_subdirectory(test)
endif(${BUILD_TEST})





