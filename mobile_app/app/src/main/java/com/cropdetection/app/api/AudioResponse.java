package com.cropdetection.app.api;

import com.google.gson.annotations.SerializedName;

public class AudioResponse {
    @SerializedName("audio_url")
    private String audioUrl;
    
    @SerializedName("audio_id")
    private String audioId;
    
    @SerializedName("success")
    private boolean success;
    
    @SerializedName("message")
    private String message;

    public String getAudioUrl() {
        return audioUrl;
    }

    public void setAudioUrl(String audioUrl) {
        this.audioUrl = audioUrl;
    }

    public String getAudioId() {
        return audioId;
    }

    public void setAudioId(String audioId) {
        this.audioId = audioId;
    }

    public boolean isSuccess() {
        return success;
    }

    public void setSuccess(boolean success) {
        this.success = success;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }
}
