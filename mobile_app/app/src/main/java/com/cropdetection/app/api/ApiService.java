package com.cropdetection.app.api;

import okhttp3.MultipartBody;
import okhttp3.RequestBody;
import retrofit2.Call;
import retrofit2.http.GET;
import retrofit2.http.Multipart;
import retrofit2.http.POST;
import retrofit2.http.Part;
import retrofit2.http.Query;

public interface ApiService {
    
    @Multipart
    @POST("api/predict")
    Call<DiseaseResult> predictDisease(
            @Part MultipartBody.Part image,
            @Part("language") RequestBody language
    );
    
    @POST("api/tts/generate")
    Call<AudioResponse> generateAudio(
            @Query("text") String text,
            @Query("language") String language
    );
    
    @GET("api/languages")
    Call<LanguagesResponse> getSupportedLanguages();
}
