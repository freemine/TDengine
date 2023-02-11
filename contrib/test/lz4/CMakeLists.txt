add_executable(lz4_test "")
add_dependencies(lz4_test ex_lz4)
target_sources(lz4_test
    PRIVATE "main.c"
)
target_include_directories(lz4_test PRIVATE $<TARGET_PROPERTY:ex_lz4,INC_DIR>)
target_link_directories(lz4_test PRIVATE $<TARGET_PROPERTY:ex_lz4,LIB_DIR>)
target_link_libraries(lz4_test PRIVATE $<TARGET_PROPERTY:ex_lz4,LIB_NAME>)

