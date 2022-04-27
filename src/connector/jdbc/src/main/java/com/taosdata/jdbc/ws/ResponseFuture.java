package com.taosdata.jdbc.ws;

import com.taosdata.jdbc.ws.entity.Response;

import java.util.concurrent.CompletableFuture;

public class ResponseFuture implements Comparable<ResponseFuture> {
    private final String action;
    private final Long id;
    private final CompletableFuture<Response> future;
    private final long timestamp;

    public ResponseFuture(String action, Long id, CompletableFuture<Response> future) {
        this.action = action;
        this.id = id;
        this.future = future;
        timestamp = System.nanoTime();
    }

    public String getAction() {
        return action;
    }

    public Long getId() {
        return id;
    }

    public CompletableFuture<Response> getFuture() {
        return future;
    }

    long getTimestamp() {
        return timestamp;
    }

    @Override
    public int compareTo(ResponseFuture rf) {
        long r = this.timestamp - rf.timestamp;
        if (r > 0) return 1;
        if (r < 0) return -1;
        return 0;
    }
}
