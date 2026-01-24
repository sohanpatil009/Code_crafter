package com.cropdetection.app.api;

import com.google.gson.annotations.SerializedName;

public class DiseaseResult {
    @SerializedName("disease_name")
    private String diseaseName;
    
    @SerializedName("confidence")
    private float confidence;
    
    @SerializedName("description")
    private String description;
    
    @SerializedName("treatment")
    private String treatment;
    
    @SerializedName("audio_url")
    private String audioUrl;
    
    @SerializedName("language")
    private String language;

    // Constructor
    public DiseaseResult() {
    }

    public DiseaseResult(String diseaseName, float confidence, String description, String treatment) {
        this.diseaseName = diseaseName;
        this.confidence = confidence;
        this.description = description;
        this.treatment = treatment;
    }

    // Getters and Setters
    public String getDiseaseName() {
        return diseaseName;
    }

    public void setDiseaseName(String diseaseName) {
        this.diseaseName = diseaseName;
    }

    public float getConfidence() {
        return confidence;
    }

    public void setConfidence(float confidence) {
        this.confidence = confidence;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public String getTreatment() {
        return treatment;
    }

    public void setTreatment(String treatment) {
        this.treatment = treatment;
    }

    public String getAudioUrl() {
        return audioUrl;
    }

    public void setAudioUrl(String audioUrl) {
        this.audioUrl = audioUrl;
    }

    public String getLanguage() {
        return language;
    }

    public void setLanguage(String language) {
        this.language = language;
    }

    public String getConfidencePercentage() {
        return String.format("%.1f%%", confidence * 100);
    }
}
