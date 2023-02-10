add_executable(lz4_test "")
target_sources(lz4_test
    PRIVATE
    "main.c"
)
depend_lz4(lz4_test)
