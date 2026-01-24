package com.cropdetection.app.api;

import com.google.gson.annotations.SerializedName;
import java.util.List;

public class LanguagesResponse {
    @SerializedName("languages")
    private List<Language> languages;

    public List<Language> getLanguages() {
        return languages;
    }

    public void setLanguages(List<Language> languages) {
        this.languages = languages;
    }

    public static class Language {
        @SerializedName("code")
        private String code;
        
        @SerializedName("name")
        private String name;
        
        @SerializedName("native_name")
        private String nativeName;

        public String getCode() {
            return code;
        }

        public void setCode(String code) {
            this.code = code;
        }

        public String getName() {
            return name;
        }

        public void setName(String name) {
            this.name = name;
        }

        public String getNativeName() {
            return nativeName;
        }

        public void setNativeName(String nativeName) {
            this.nativeName = nativeName;
        }
    }
}
